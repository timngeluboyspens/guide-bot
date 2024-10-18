import os
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from app.bot import create_conversational_chain, conversation_chat, load_vector_store 

class TelegramBot:
    def __init__(self, token: str, username: str):
        self.TOKEN: Final = token
        self.BOT_USERNAME: Final = username
        # self.app = Application.builder().token(self.TOKEN).build()
        self.app = ApplicationBuilder().token(self.TOKEN).build()
        
        # Load embeddings and vector store
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
        self.vector_store = load_vector_store(self.embeddings)

        # Create the conversational chain
        self.conversational_chain = create_conversational_chain(self.vector_store)

        # Initialize memory for history
        self.history = []

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hello! Thanks for chatting with me. I am your bot!')

    def handle_response(self, query: str) -> str:
        # Use the conversational chain to handle the query
        history, answer, _ = conversation_chat(query, self.conversational_chain, self.history)
        self.history = history  # Update the bot's memory with the new history
        return answer

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = update.message.text

        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

        if message_type == 'group':
            if self.BOT_USERNAME in text:
                new_text: str = text.replace(self.BOT_USERNAME, '').strip()
                response: str = self.handle_response(new_text)
            else:
                return
        else:
            response: str = self.handle_response(text)

        print('Bot:', response)
        await update.message.reply_text(response)

    async def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')

    def add_handlers(self):
        # Tambahkan handler untuk perintah
        self.app.add_handler(CommandHandler("start", self.start_command))

        # Tambahkan handler untuk pesan teks
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))

        # Tambahkan error handler
        self.app.add_error_handler(self.handle_error)

    def run(self):
        # Mulai bot dengan polling
        self.add_handlers()
        print('Polling...')
        self.app.run_polling(poll_interval=5)

    def stop(self):
        self.app.shutdown()

if __name__ == '__main__':
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    BOT_USERNAME = "@bambubot"

    bot = TelegramBot(TOKEN, BOT_USERNAME)
    bot.run()
