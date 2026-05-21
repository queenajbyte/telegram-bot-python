import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ambil token dari environment
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BOT_NAME = os.getenv("BOT_NAME", "Queenajbot")

# Inisialisasi Groq
client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👑 Halo! Saya adalah **{BOT_NAME}** — AI Trading Assistant Solana.\n\n"
        "Kamu bisa tanya apa saja tentang meme coin, trading, atau minta saya scan token.\n"
        "Coba ketik: `scan $WIF` atau `analisis SOL`"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Prompt system untuk Queenajbot
    system_prompt = f"""
    Kamu adalah {BOT_NAME}, AI Trading Agent yang cerdas, fun, dan hati-hati di Solana.
    Spesialis meme coin, sniping, dan analisis token.
    Jawab dalam bahasa Indonesia yang santai tapi profesional.
    Selalu ingatkan risiko trading.
    """

    try:
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "llama3-70b-8192"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=800
        )
        ai_reply = response.choices[0].message.content
        await update.message.reply_text(ai_reply)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Maaf, saya sedang mengalami gangguan. Coba lagi nanti ya.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print(f"✅ {BOT_NAME} sedang aktif...")
    app.run_polling()

if __name__ == "__main__":
    main()
