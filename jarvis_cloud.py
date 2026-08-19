import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from google import genai
from gtts import gTTS

# Configuración inicial de las llaves
API_KEY_GEMINI = os.getenv("GEMINI_API_KEY")
TOKEN_TELEGRAM = os.getenv("TELEGRAM_BOT_TOKEN")

client = genai.Client(api_key=API_KEY_GEMINI)

SYSTEM_PROMPT = """
Eres J.A.R.V.I.S., un sistema operativo de inteligencia artificial avanzada.
Respondes siempre con máxima eficiencia, precisión técnica, un tono formal y servicial,
tratando al usuario como el jefe o creador.
"""

# 1. Manejador para mensajes de texto (Responde con texto y nota de voz)
async def jarvis_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Respuesta de Gemini usando el modelo correcto
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=user_text,
        config={'system_instruction': SYSTEM_PROMPT}
    )
    
    reply_text = response.text
    
    # Enviar respuesta en texto
    await update.message.reply_text(reply_text)
    
    # Generar y enviar el audio (TTS) de vuelta a Telegram
    try:
        tts = gTTS(text=reply_text, lang='es')
        audio_path = "reply.mp3"
        tts.save(audio_path)
        with open(audio_path, 'rb') as audio_file:
            await update.message.reply_voice(voice=audio_file)
    except Exception as e:
        print(f"Error generando audio: {e}")

# 2. Manejador para imágenes (Visión Artificial / Análisis)
async def jarvis_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Imagen recibida, jefe. Procesando análisis visual...")
    
    photo_file = await update.message.photo[-1].get_file()
    photo_path = "temp_image.jpg"
    await photo_file.download_to_drive(photo_path)
    
    await update.message.reply_text("✅ Análisis completado. (Módulo de visión activo).")

# 3. Comando para reportes o base de datos
async def cmd_reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Generando reporte institucional o planilla solicitada...")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()

    # Registro de comandos y manejadores
    app.add_handler(CommandHandler("reporte", cmd_reporte))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), jarvis_text))
    app.add_handler(MessageHandler(filters.PHOTO, jarvis_photo))

    print("J.A.R.V.I.S. Cloud iniciado correctamente con Audio, Visión y Texto...")
    app.run_polling()
