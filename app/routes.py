# guide_bot/routes.py
from flask import Blueprint, Response, abort, jsonify, render_template, redirect, send_file, url_for, flash, request, session
import markdown
from app import db
from dotenv import load_dotenv
import os
from langchain_core.documents import Document as ChatDocument
from werkzeug.utils import secure_filename
from app.models import Document, Conversations, Messages, Sender
from app.bot import *
from app.docs import api_docs
import logging
import uuid
from flasgger import swag_from
import cv2

load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

logging.basicConfig(level=logging.INFO)

api_bp = Blueprint('api', __name__, url_prefix='/api')
document_bp = Blueprint('document', __name__, url_prefix='/api/documents')
conversations_bp = Blueprint('conversations', __name__, url_prefix='/api/conversations')

# VIEW DOCUMENT/S
@document_bp.route('/', methods=['GET'])
@document_bp.route('/<string:id>', methods=['GET'])
@swag_from(api_docs['view_documents'])
def view(id=None):
    try:
        logging.info(f"Viewing document with ID {id}")
        if id:
            document = Document.query.get_or_404(id)
            logging.info(f"Viewing document with ID {id}")
            return jsonify(document.to_dict()), 200
        else:
            documents = Document.query.all()
            logging.info("Viewing all documents")
            return jsonify([document.to_dict() for document in documents]), 200
    except Exception as e:
        logging.error(f"Error viewing document(s): {str(e)}")
        return jsonify({"error": "An error occurred while fetching the documents"}), 500

# CREATE DOCUMENT
@document_bp.route('/', methods=['POST'])
@swag_from(api_docs['create_document'])
def create():    
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "File is required"}), 400
        
        title = secure_filename(file.filename)
        if not title:
            return jsonify({"error": "File name is invalid"}), 400
        
        filepath = os.path.normpath(os.path.join('data', title))

        if not os.path.exists('data'):
            os.makedirs('data', exist_ok=True)

        with open(filepath, 'wb') as f:
            f.write(file.read())

        new_document = Document(title=title, path=filepath)
        db.session.add(new_document)
        db.session.commit()
        
        logging.info(f"Created document with title: {title}")
        return jsonify(new_document.to_dict()), 201
    except Exception as e:
        logging.error(f"Error creating document: {str(e)}")
        return jsonify({"error": "An error occurred while creating the document"}), 500

# UPDATE DOCUMENT
@document_bp.route('/<string:id>', methods=['PUT'])
@swag_from(api_docs['update_document'])
def update(id):
    try:
        document = Document.query.get_or_404(id)
        
        file = request.files.get('file')
        if file:
            document.title = secure_filename(file.filename)
            document.path = os.path.normpath(os.path.join('data', document.title))
            
            if not os.path.exists('data'):
                os.makedirs('data', exist_ok=True)
            
            with open(document.path, 'wb') as f:
                f.write(file.read())                
        
        db.session.commit()
        logging.info(f"Updated document with ID: {id}")
        return jsonify(document.to_dict()), 200
    except Exception as e:
        logging.error(f"Error updating document with ID {id}: {str(e)}")
        return jsonify({"error": f"An error occurred while updating document with ID {id}"}), 500

# DELETE DOCUMENT
@document_bp.route('/<string:id>', methods=['DELETE'])
@swag_from(api_docs['delete_document'])
def delete(id):
    try:
        document = Document.query.get_or_404(id)
        db.session.delete(document)
        db.session.commit()
        
        if os.path.exists(document.path):
            os.remove(document.path)

        logging.info(f"Deleted document with ID: {id}")
        return {"message": "Document deleted successfully"}, 200
    except Exception as e:
        logging.error(f"Error deleting document with ID {id}: {str(e)}")
        return jsonify({"error": f"An error occurred while deleting document with ID {id}"}), 500

# RELOAD VECTOR DB
@document_bp.route('/reload-vector-db', methods=['GET'])
@swag_from(api_docs['reload_vector_db'])
def reload_vector_db():
    try:
        global embeddings
        vector_store = load_vector_store(embeddings)
        documents = Document.query.all()
        document_ids = [document.id for document in documents]      
        metadatas = vector_store.get()['metadatas']
        metadatas_document_id = [metadata["document_id"] for metadata in metadatas]

        # Add new documents to vector store
        for document in documents:
            if document.id in metadatas_document_id:
                logging.info(f"Document {document.id} already exists in the vector store.")
                continue
            if not document.path:
                logging.info(f"Document {document.id} has no path.")
                continue

            if not os.path.exists('data'):
                os.makedirs('data')

            all_text = extract_text_from_file(document.path)
            if not all_text.strip():
                logging.warning(f"Failed to extract text from document {document.title}")
                continue

            splitted_text = split_documents(all_text)
            for text in splitted_text:            
                document_obj = ChatDocument(
                    page_content= text,
                    metadata = {
                        "id": str(uuid.uuid4()),
                        "title": document.title,
                        "document_id": document.id,                        
                    }
                )
                vector_store.add_documents(
                    documents=[document_obj], 
                    ids=[document_obj.metadata['id']]
                )
                logging.info(f"Added document {document.title} with vector ID {document_obj.metadata['id']}")
        
        # Remove files in the data directory
        # for file in os.listdir('data'):
        #     os.remove(os.path.join('data', file))

        # Remove vectors that no longer exist in the SQL database
        for metadata in metadatas:
            if metadata['document_id'] not in document_ids:
                vector_store.delete([metadata['id']])
                logging.info(f"Deleted vector for document {metadata['title']} with vector ID {metadata['id']}")

        return {"message": "Vector store reloaded."}, 200

    except Exception as e:
        logging.error(f"Error reloading vector store: {str(e)}")
        return jsonify({"error": "An error occurred while reloading the vector store"}), 500

# VIEW CONVERSATION/S
@conversations_bp.route('/', methods=['GET'])
@conversations_bp.route('/<string:conversation_id>', methods=['GET'])
@swag_from(api_docs['view_conversations'])
def view(conversation_id=None):
    try:
        headers = request.headers       
        user_id = headers.get('Authorization')
        if not user_id:
            return {"error": "User ID is required."}, 400
        
        if conversation_id:
            conversation = Conversations.query.get_or_404(conversation_id)
            if conversation.user_id != user_id:
                return {"error": "User ID mismatch."}, 400
            messages = Messages.query.filter_by(conversation_id=conversation_id).all()
            logging.info(f"Viewing conversation with ID {conversation_id}")
            return jsonify([message.to_dict() for message in messages]), 200
        else:
            conversations = Conversations.query.filter_by(user_id=user_id)
            logging.info("Viewing all conversations")
            return jsonify([conversation.to_dict() for conversation in conversations]), 200
    except Exception as e:
        logging.error(f"Error viewing conversation(s): {str(e)}")
        return jsonify({"error": "An error occurred while fetching the conversations"}), 500

# CREATE CONVERSATION
@conversations_bp.route('/', methods=['POST'])
@swag_from(api_docs['create_conversation'])
def create():
    try:          
        headers = request.headers       
        user_id = headers['Authorization']
        if not user_id:
            return {"error": "User ID is required."}, 400
        
        title = request.json.get('title')
        if not title:
            return {"error": "Conversation title is required."}, 400

        new_conversation = Conversations(user_id=user_id,title=title)
        db.session.add(new_conversation)
        db.session.commit()
        logging.info(f"Created conversation with title: {title}")
        return jsonify(new_conversation.to_dict()), 201

    except Exception as e:
        logging.error(f"Error creating conversation: {str(e)}")
        return jsonify({"error": "An error occurred while creating the conversation"}), 500
    
# UPDATE CONVERSATION
@conversations_bp.route('/<string:conversation_id>', methods=['UPDATE'])
@swag_from(api_docs['update_conversation'])
def update(conversation_id):
    try:
        headers = request.headers       
        user_id = headers['Authorization']
        if not user_id:
            return {"error": "User ID is required."}, 400
        
        conversation = Conversations.query.get_or_404(conversation_id)

        if conversation.user_id != user_id:
            return {"error": "User ID mismatch."}, 400
        
        title = request.json.get('title')
        if title:
            conversation.title = title
        
        db.session.commit()
        logging.info(f"Updated conversation with ID: {conversation_id}")
        return jsonify(conversation.to_dict()), 200
    except Exception as e:
        logging.error(f"Error updating conversation with ID {conversation_id}: {str(e)}")
        return jsonify({"error": f"An error occurred while updating conversation with ID {conversation_id}"}), 500
    
# DELETE CONVERSATION
@conversations_bp.route('/<string:conversation_id>', methods=['DELETE'])
@swag_from(api_docs['delete_conversation'])
def delete(conversation_id):
    try:
        headers = request.headers
        user_id = headers['Authorization']
        if not user_id:
            return {"error": "User ID is required."}, 400
        
        conversation = Conversations.query.get_or_404(conversation_id)
        
        if conversation.user_id != user_id:
            return {"error": "User ID mismatch."}, 400
        
        db.session.delete(conversation)
        db.session.commit()
        logging.info(f"Deleted conversation with ID: {conversation_id}")
        return {"message": "Conversation deleted successfully"}, 200
    except Exception as e:
        logging.error(f"Error deleting conversation with ID {conversation_id}: {str(e)}")
        return jsonify({"error": f"An error occurred while deleting conversation with ID {conversation_id}"}), 500
    
# CHATBOT
@conversations_bp.route('/<string:conversation_id>', methods=['POST'])
@swag_from(api_docs['chat'])
def chat(conversation_id):
    try:
        headers = request.headers
        user_session = headers['Authorization']
        if not user_session:
            return {"error": "User session is required."}, 400
        
        conversation = Conversations.query.get_or_404(conversation_id)        
        if not conversation:
            return {"error": "Conversation not found."}, 404
        
        if user_session != conversation.user_id:
            return {"error": "User session mismatch."}, 400                

        user_input = request.json.get('user_input')
        if not user_input:
            return {"error": "User input is required."}, 400
        
        input_message = Messages(conversation_id=conversation_id, message=user_input, sender=Sender.USER)
        db.session.add(input_message)
        db.session.commit()

        # Initialize session if not already initialized
        if 'history' not in session:
            session['history'] = []

        vector_store = load_vector_store(embeddings)
        if not vector_store:
            return {"error": "No information available yet."}, 400

        # Create conversation chain and process user input
        chain = create_conversational_chain(vector_store)
        if len(session.get('history')) > 10:
            session['history'].pop(0)
        session['history'], output, source_documents = conversation_chat(user_input, chain, session['history'])
        output_message = Messages(conversation_id=conversation_id, message=output, sender=Sender.BOT)
        db.session.add(output_message)
        db.session.commit()
        output = markdown.markdown(output)
        return {"response": output}, 200

    except Exception as e:
        logging.error(f"Error in chatbot: {str(e)}")
        return jsonify({"error": "An error occurred during the chat process"}), 500