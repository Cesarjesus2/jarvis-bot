import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai
from gtts import gTTS

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Configuración inicial
API_KEY_GEMINI = os.getenv("GEMINI_API_KEY")
TOKEN_TELEGRAM = os.getenv("TELEGRAM_BOT_TOKEN")

client = genai.Client(api_key=API_KEY_GEMINI)

SYSTEM_PROMPT = """
Eres J.A.R.V.I.S., un sistema operativo de inteligencia artificial avanzada. 
Respondes siempre con máxima eficiencia, precisión técnica, un tono formal y servicial, 
tratando al usuario como el jefe o creador.
"""

async def jarvis_core(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # 1. Obtener respuesta de Gemini
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=user_text,
        config={'system_instruction': SYSTEM_PROMPT}
    )
    
    reply_text = response.text
    await update.message.reply_text(reply_text)
    
    # 2. Generar audio (TTS)
    tts = gTTS(text=reply_text, lang='es')
    audio_path = "reply.mp3"
    tts.save(audio_path)
    
    # 3. Enviar audio a Telegram
    await update.message.reply_voice(voice=open(audio_path, 'rb'))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), jarvis_core))
    app.run_polling()
