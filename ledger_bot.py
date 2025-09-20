from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7453337990:AAHKpCY-tceV5N47CsyUxLZ9KJEk5tz1KRU"

# Simple in-memory ledger (resets if you restart the bot)
ledger = {
    "deposits": [],
    "issued": []
}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "✅ Ledger Bot Activated!\n\n"
        "📊 Current Group Status:\n"
        "• Operator: You\n"
        "• USDT Rate: 1\n"
        "• Ledger Status: Active 🟢\n\n"
        "💡 Quick Guide:\n"
        "• Type +amount to record a deposit\n"
        "• Type 'show ledger' to view statistics\n"
        "• Type /start to see this menu again"
    )
    await update.message.reply_text(msg)

# Handle messages (+amount, show ledger)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Add deposit
    if text.startswith("+"):
        try:
            amount = float(text[1:])
            ledger["deposits"].append(amount)
            await update.message.reply_text(f"💰 Deposit recorded: {amount}")
        except ValueError:
            await update.message.reply_text("❌ Invalid format. Use +100")

    # Show ledger
    elif text.lower() == "show ledger":
        total_in = sum(ledger["deposits"])
        total_out = sum(ledger["issued"])
        pending = total_in - total_out

        msg = (
            f"📒 Ledger Report\n\n"
            f"Total Deposits: {total_in}\n"
            f"Total Issued: {total_out}\n"
            f"Pending: {pending}\n"
            f"USDT Rate: 1"
        )
        await update.message.reply_text(msg)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Ledger Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
