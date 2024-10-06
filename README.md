# Document Management and Chatbot API

This project provides a simple API to manage documents, manage conversations, and interact with a chatbot. It is built using Langchain, HuggingFace, Flask and Flask-SQLAlchemy with vector embeddings stored in a Chroma database.

## Features
- View, create, update, and delete documents.
- View, create, update, and delete conversations.
- Chatbot interaction.
- Reload vector store from document database.

## Prerequisites

Make sure you have the following installed:
- Python 3.10+
- `pip`
- `virtualenv`

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-repo/document-chatbot-api.git
cd document-chatbot-api
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup environment variables
Create a `.env` file in the root directory and add your configuration:

```
SECRET_KEY=s
DATABASE_URL=
GROQ_API_KEY=
HUGGINGFACEHUB_API_TOKEN=
GOOGLE_API_KEY=
```

### 6. Installation System Dependencies
To ensure the proper functionality of our application, the following dependencies need to be installed on your system:

[libmagic](https://man7.org/linux/man-pages/man3/libmagic.3.html) - A library used for detecting file types.
[poppler](https://poppler.freedesktop.org/) - A PDF rendering library.
[libreoffice](https://www.libreoffice.org/discover/libreoffice/) - A powerful office suite.
[pandoc](https://pandoc.org/) - A universal document converter.
[tesseract](https://github.com/tesseract-ocr/tesseract) - An OCR (Optical Character Recognition) engine.

#### Installation Instructions for Linux Users
If you're using a Linux-based system, you can easily install all of these packages by running our provided shell script.

1. Download the script install_packages.sh.
2. Make the script executable by running the following command:
```bash
sudo chmod +x install_packages.sh
```
3. Then, run the script to install all required packages:
```bash
sudo ./install_packages.sh
```
This script will automatically handle the installation of all necessary packages on your system.


### 7. Initialize the database
Run the following command to create the database and apply migrations:

```bash
flask db init
flask db upgrade
flask db upgrade
```

### 8. Start the Flask server
To start the development server, run:

```bash
flask run
```

The API will be available at `http://localhost:5000`.

## API Documentation

The project uses **Flasgger** for API documentation. You can access the interactive API docs by navigating to:

```
http://localhost:5000/apidocs/
```

## Endpoints

### `/api/documents`
- `GET /documents`: View all documents.
- `GET /documents/{id}`: View a specific document.
- `POST /documents`: Create a new document (multipart form data).
- `PUT /documents/{id}`: Update an existing document.
- `DELETE /documents/{id}`: Delete a document by its ID.

### `/api/chat`
- `POST /chat`: Send a message to the chatbot.

### `/api/reload-vector-db`
- `GET /reload-vector-db`: Reload the vector store with updated documents.
