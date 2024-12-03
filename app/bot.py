import os
import pandas as pd
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace, HuggingFaceEmbeddings, HuggingFaceEndpoint, HuggingFacePipeline
from unstructured.partition.auto import partition
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

# Extracting text from uploaded file
def extract_text_from_file(file_path):  
    elements = partition(filename=file_path)
    return "\n\n".join([str(el) for el in elements])

# Function to return the welcome message
def get_welcome_message():
    return """🌿 <b>Selamat datang di Bambu Bot!</b>
Asisten digital Anda untuk semua informasi dan layanan di Kelurahan Keputih.

Saya siap membantu Anda dengan cepat dan mudah! Berikut adalah perintah yang dapat Anda gunakan:

/kependudukan: Informasi tentang layanan kependudukan.
/non_kependudukan: Informasi tentang layanan non-kependudukan.
/lainnya: Panduan pendaftaran akun di website resmi Kota Surabaya.
/profile: Profil Kelurahan Keputih.

❓ <b>Butuh bantuan lainnya?</b> Anda juga dapat langsung mengetik pertanyaan Anda, dan saya akan membantu menjawabnya!"""

# Returns the profile information of Kelurahan Keputih
def get_profile_info():
    return """📍 <b>Profil Kelurahan Keputih</b>

• <b>Nama Lurah:</b> Achmad Fida Fajar Febriansyah, S.H., M.H.
• <b>Kontak:</b> +62 31 5931253
• <b>Alamat & Lokasi:</b>
    Jalan Keputih Tegal Timur No.23,
    RT.005/RW.02, Keputih, Kec. Sukolilo,
    Surabaya, Jawa Timur 60111
    '<a href="https://www.google.com/maps?saddr=Current+Location&daddr=-7.295555121878993,112.80208110809326">Lihat di Google Maps</a>

🏢 <b>Butuh informasi lebih lanjut?</b>
Silakan kunjungi kantor kami selama jam kerja. Kami siap melayani Anda!"""

# Generates a message listing questions based on the given category from the DataFrame
def generate_questions_message(df, category, page=1, items_per_page=10):
    # Generate the header section of the message
    def _create_header(category):
        header = f"📋 <b>Daftar Layanan {category.capitalize()}</b>\n"
        
        if category != 'lainnya':
            header += f"Berikut adalah beberapa layanan terkait {category} yang tersedia:\n"
        else:
            header += "Berikut adalah beberapa layanan lainnya yang tersedia:\n"
        
        return header

    # Generate the numbered list of questions
    def _generate_questions_list(filtered_questions, category, page, items_per_page):
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        questions = []
        for i, (_, question) in enumerate(
            filtered_questions[start_idx:end_idx].items(), 
            start=start_idx + 1
        ):
            questions.append(f"/{category}_{i}: {question}")
        
        return "\n".join(questions)

    #Generate the footer section of the message
    def _create_footer(page, total_pages, category):
        navigation = []
        
        if total_pages > 1:
            navigation.append("\n<b>Navigasi Halaman:</b>")
            if page > 1:
                navigation.append(
                    f"Ketik /{category}_p_{page - 1} untuk halaman sebelumnya."
                )
            if page < total_pages:
                navigation.append(
                    f"Ketik /{category}_p_{page + 1} untuk halaman berikutnya."
                )
            
        navigation.append(
            "\n<b>Ingin informasi lainnya?</b> "
            "Anda juga dapat langsung mengetik pertanyaan Anda! 😊"
        )
        
        return "\n".join(navigation)

    DISPLAY_CATEGORY = category
    CATEGORY = 'others' if category == 'lainnya' else category
    
    # Filter and calculate pagination
    filtered_questions = df[df['type'] == CATEGORY]['Pertanyaan']
    total_items = len(filtered_questions)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    # Validate page number
    if not 1 <= page <= total_pages:
        return "Halaman tidak valid. Silakan pilih halaman yang tersedia."
    
    # Generate header
    header = _create_header(DISPLAY_CATEGORY)
    
    # Generate questions list
    questions_list = _generate_questions_list(
        filtered_questions, 
        DISPLAY_CATEGORY, 
        page, 
        items_per_page
    )
    
    # Generate footer
    footer = _create_footer(page, total_pages, DISPLAY_CATEGORY)
    
    # Combine all components
    return f"{header}\n{questions_list}\n{footer}"

# Retrieves an answer based on the specified category and index from the DataFrame.
def generate_answer(df, category, index):
    answers = None
    if category == 'lainnya':
        answers = df[df['type'] == 'others']['Jawaban']
    else:
        answers = df[df['type'] == category]['Jawaban']

    max_length = len(answers) if answers is not None else 0
    return (
        answers.iloc[index] 
        if answers is not None and index < max_length 
        else 'Maaf, perintah yang Anda ajukan tidak valid.'
    )

# Function to handle conversation with the chatbot
def conversation_chat(query, chain, history):
    logging.info(f"Received query: {query}")
    result = chain.invoke({"input": query, "chat_history": history})
    
    answer = result.get("answer", "Maaf, saya tidak tahu jawabannya.")
    history.append(("human", query))
    history.append(("ai", answer))
    logging.info(f"Answer generated: {answer}")

    # Assuming result contains relevant document metadata, such as filenames
    if "context" in result and result["context"]:
        logging.info("Source documents retrieved.")
        return history, answer, result["context"]
    
    logging.warning("No source documents found.")
    return history, answer, None

# Function to create the conversational chain
def create_conversational_chain(vector_store):
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold", 
        search_kwargs={"k": 1, 'score_threshold': 0.1}
    )

    # LLAMA GROQ initialization
    llm = ChatGroq(
        groq_api_key=os.getenv('GROQ_API_KEY'), 
        model_name='llama3-70b-8192'
    )

    # Contextualize question prompt (in Bahasa Indonesia)
    contextualize_q_system_prompt = (
        "Berdasarkan riwayat percakapan dan pertanyaan terbaru dari pengguna "
        "yang mungkin merujuk pada konteks dalam riwayat percakapan, "
        "formulasikan pertanyaan yang dapat dipahami tanpa perlu melihat riwayat percakapan. "
        "Jangan menjawab pertanyaan tersebut, hanya reformulasikan jika perlu, "
        "dan jika tidak perlu perubahan, kembalikan seperti semula."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")  # Replace {input} correctly to handle the user's query
        ]
    )

    # Create a history-aware retriever to contextualize the query based on chat history
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # Question-answering system prompt
    qa_system_prompt = (
        "Anda adalah Chatbot yang sangat membantu di lingkungan Kelurahan Keputih. Nama Anda adalah BambuBot."
        "Anda dinamakan BambuBot karena di Kelurahan Keputih terdapat hutan bambu yang ikonik dan menjadi ciri khas."
        "Gunakan potongan konteks berikut untuk menjawab pertanyaan. Jika Anda tidak tahu jawabannya, "
        "katakan 'Maaf, saya tidak tahu jawabannya'."
        "\n\n\"{context}\""
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")  # This is where the user's query will be inserted
        ]
    )

    # Create a document chain for answering questions using retrieved context
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # Combine the history-aware retriever with the question-answer chain
    rag_chain = create_retrieval_chain(
        history_aware_retriever, question_answer_chain
    )

    return rag_chain

# Function to save uploaded file to the server
def save_uploaded_file(uploaded_file):
    save_dir = 'data'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, uploaded_file.filename)
    uploaded_file.save(file_path)
    return file_path

# Loads data from static CSV files
def load_static_data(category, path = './app/static/data'):
    if (category == 'menu'):
        path += '/menu'
    elif (category == 'context'):
        path += '/context'
    else:
        return None
    
    # Load and process 'kependudukan' data
    kependudukan = pd.read_csv(f'{path}/kependudukan.csv')
    kependudukan.dropna(inplace=True)
    kependudukan['type'] = 'kependudukan'
    
    # Load and process 'non-kependudukan' data
    non_kependudukan = pd.read_csv(f'{path}/non-kependudukan.csv')
    non_kependudukan.dropna(inplace=True)
    non_kependudukan['type'] = 'non_kependudukan'
    
    # Load and process 'others' data
    others = pd.read_csv(f"{path}/others.csv")
    others.dropna(inplace=True)
    others['type'] = 'others'
    
    return pd.concat([kependudukan, non_kependudukan, others], ignore_index=True)

# Function to load all saved files from the server
def load_saved_files():
    save_dir = 'data'
    if not os.path.exists(save_dir):
        return []
    return [os.path.join(save_dir, f) for f in os.listdir(save_dir)]

# Function to split documents into smaller chunks
def split_documents(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_text(text)

def load_vector_store(embeddings):    
    vector_store = Chroma(
        collection_name="chatbot",
        embedding_function=embeddings or HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'}), 
        persist_directory="vector_store"
    )
    return vector_store

def load_static_vector_store(embeddings):
    # Load context data
    context_data = load_static_data('context')
        
    # Convert the DataFrame to a list of documents
    documents = []
    for index, row in context_data.iterrows():
        doc = Document(id=(1 + index), page_content=row['jawaban'], metadata={
            "category": row['kategori'], 
            "sub_category": row['sub_kategori'], 
            "object": row['objek'],
            "service_source": row['media_layanan'],                
        })
        documents.append(doc)

    vector_store = Chroma.from_documents(
        collection_name="chatbot",
        documents=documents,
        embedding=embeddings,
        persist_directory="vector_store"
    )

    return vector_store