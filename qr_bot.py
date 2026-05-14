import logging
import qrcode
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Tokeningizni shu yerga qo'ying
TOKEN = "BU_YERGA_TOKENINGIZNI_QOYING"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men QR-kod generatoriman.\n\n"
        "Menga quyidagilarni yuboring:\n"
        "🔗 Link (https://...) — link uchun QR\n"
        "🖼 Rasm — rasm uchun QR\n\n"
        "Sinab ko'ring!"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Foydalanish:\n"
        "1. Link yuboring → QR-kod oling\n"
        "2. Rasm yuboring → Rasm URL si uchun QR-kod oling\n"
    )

def make_qr(text: str) -> io.BytesIO:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    await update.message.reply_text("QR-kod tayyorlanmoqda...")
    buf = make_qr(text)
    await update.message.reply_photo(photo=buf, caption=f"✅ QR-kod: {text[:50]}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_url = file.file_path
    await update.message.reply_text("Rasm uchun QR-kod tayyorlanmoqda...")
    buf = make_qr(file_url)
    await update.message.reply_photo(photo=buf, caption="✅ Rasm URL si uchun QR-kod tayyor!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Bot ishga tushdi...")
    app.run_polling()
