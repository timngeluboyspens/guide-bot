# guide_bot/routes.py
from flask import Blueprint, abort, jsonify, render_template, redirect, send_file, url_for, flash, request, session
import markdown
from app import db
from dotenv import load_dotenv
import os
from langchain_core.documents import Document as ChatDocument
from werkzeug.utils import secure_filename
from app.models import Document
from app.bot import *
import logging
import uuid

load_dotenv()
api_bp = Blueprint('api', __name__, url_prefix='/api')

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

logging.basicConfig(level=logging.INFO)

# VIEW DOCUMENT/S
@api_bp.route('/documents', methods=['GET'])
@api_bp.route('/documents/<int:id>', methods=['GET'])
def view(id=None):
    if id:
        document = Document.query.get_or_404(id)
        logging.info(f"Viewing document with ID {id}")
        return jsonify(document.to_dict())
    else:
        documents = Document.query.all()
        logging.info("Viewing all documents")        
        return jsonify([document.to_dict() for document in documents])
    
# CREATE DOCUMENT
@api_bp.route('/documents', methods=['POST'])
def create():    
    file = request.files.get('file')
    title = secure_filename(file.filename)
    
    if not file:
        return {"error": "Title are required."}, 400
    
    new_document = Document(title=title, file=file.read())
    db.session.add(new_document)
    db.session.commit()
    
    return jsonify(new_document.to_dict()), 201

# UPDATE DOCUMENT
@api_bp.route('/documents/<int:id>', methods=['PUT'])
def update(id):
    document = Document.query.get_or_404(id)
    
    file = request.files.get('file')
    
    if file:
        document.file = file.read()
        document.title = secure_filename(file.filename)
    
    db.session.commit()
    
    return jsonify(document.to_dict()), 200

# DELETE DOCUMENT
@api_bp.route('/documents/<int:id>', methods=['DELETE'])
def delete(id):
    document = Document.query.get_or_404(id)
    db.session.delete(document)
    db.session.commit()
    return {"message": "Document deleted successfully."}

@api_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')
    if not user_input:
        return {"error": "User input is required."}, 400

    # Jika sesi belum ada, inisialisasi session history dan generated
    if 'history' not in session:
        session['history'] = []
        session['past_questions'] = []
        session['generated'] = ["Selamat datang di GuideBot!"]

    vector_store = load_vector_store(embeddings)    
    if vector_store:
        chain = create_conversational_chain(vector_store)
    else:
        return {"message": "No information available yet."}

    # Set sesi sebagai permanen agar menggunakan timeout
    session.permanent = True

    # Proses chat seperti biasa
    session['history'], output, source_documents = conversation_chat(user_input, chain, session['history'])
    output = markdown.markdown(output)
    session['generated'].append(output)

    return {
        "response": output,
    }

@api_bp.route('/reload-vector-db', methods=['GET'])
def reload_vector_db():
    global embeddings
    
    vector_store = load_vector_store(embeddings)
    # Load all documents from the SQL database
    documents = Document.query.all()
    document_ids = [document.id for document in documents]      
    metadatas = vector_store.get()['metadatas']
    metadatas_document_id = [metadata["document_id"] for metadata in metadatas]
    
    for document in documents:
        # Check if document already exists in the vector store
        if document.id in metadatas_document_id:
            print(f"Document {document.id} already exists in the vector store.")
            continue

        # Check if document.file is not None
        if document.file is None:
            print(f"Document {document.id} has no file.")
            continue

        #  Save the document to a temporary file         
        file_path = os.path.join('data', secure_filename(document.title))
        with open(file_path, 'wb') as f:
            f.write(document.file)
        
        # Extract text based on file type
        all_text = extract_text_from_file(file_path)
        
        if not all_text.strip():
            print(f"Failed to extract text from document {document.title}")
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
            print(f"Menambahkan dokumen dengan judul {document.title} dan id vector {document_obj.metadata['id']}")

        os.remove(file_path)

    metadatas = vector_store.get()['metadatas']

    # Delete vector which document_id not in document_ids
    for metadata in metadatas:
        if metadata['document_id'] not in document_ids:
            vector_store.delete([metadata['id']])
            print(f"Menghapus dokumen dengan judul {metadata['title']} dan id {metadata['id']}")

    return {"message": "Vector store reloaded."}






