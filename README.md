# Document Management and Chatbot API

This project provides a simple API to manage documents and interact with a chatbot using Langchain and a vector store. It is built using Flask and Flask-SQLAlchemy with vector embeddings stored in a Chroma database.

## Features
- View, create, update, and delete documents.
- Chatbot interaction using Langchain.
- Reload vector store from document database.

## Prerequisites

Make sure you have the following installed:
- Python 3.8+
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
FLASK_APP=app.py
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=your_secret_key
GOOGLE_API_KEY=your_google_api_key
```

### 6. Initialize the database
Run the following command to create the database and apply migrations:

```bash
flask db upgrade
```

### 7. Start the Flask server
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