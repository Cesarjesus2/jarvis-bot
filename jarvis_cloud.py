import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from google import genai
from gtts import gTTS

# Configuración inicial
API_KEY_GEMINI = os.getenv("GEMINI_API_KEY")
TOKEN_TELEGRAM = os.getenv("TELEGRAM_BOT_TOKEN")

client = genai.Client(api_key=API_KEY_GEMINI)

SYSTEM_PROMPT = """
Eres J.A.R.V.I.S., un sistema operativo de inteligencia artificial avanzada.
Respondes siempre con máxima eficiencia, precisión técnica, un tono formal y servicial,
tratando al usuario como el jefe o creador.
"""

# Manejador para mensajes de texto
async def jarvis_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Respuesta de Gemini
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=user_text,
        config={'system_instruction': SYSTEM_PROMPT}
    )
    
    reply_text = response.text
    await update.message.reply_text(reply_text)

# Manejador para imágenes (Visión Artificial / Análisis)
async def jarvis_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Imagen recibida, jefe. Procesando análisis visual...")
    
    # Obtener el archivo de la foto enviada a Telegram
    photo_file = await update.message.photo[-1].get_file()
    photo_path = "temp_image.jpg"
    await photo_file.download_to_drive(photo_path)
    
    # Aquí puedes integrar tu lógica de YOLO11n o DeepFace usando 'photo_path'
    # Por ahora, le pediremos a Gemini que descifre o comente la imagen si deseas:
    
    await update.message.reply_text("✅ Análisis completado. (Módulo de visión activo).")

# Comando para reportes o base de datos
async def cmd_reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Generando reporte institucional o planilla solicitada...")
    # Aquí programamos la lógica para generar Excel/PDF o consultar SQLite

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()

    # Registro de manejadores
    app.add_handler(CommandHandler("reporte", cmd_reporte))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), jarvis_text))
    app.add_handler(MessageHandler(filters.PHOTO, jarvis_photo))

    print("J.A.R.V.I.S. Cloud iniciado correctamente...")
    app.run_polling()
