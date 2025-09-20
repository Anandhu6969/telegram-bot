from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7453337990:AAHKpCY-tceV5N47CsyUxLZ9KJEk5tz1KRU"

# Per-user ledger
ledger = {}
profit_percent = 0  # default profit %

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "✅ Ledger Bot Activated!\n\n"
        "💡 Usage Guide:\n"
        "• +amount → Record money you gave (loan/investment)\n"
        "• -amount → Record money returned to you\n"
        "• show ledger → View current balance & profit\n"
        "• /setprofit <number> → Update profit %\n"
        "• /reset → Clear your ledger\n"
    )
    await update.message.reply_text(msg)

# /setprofit command
async def set_profit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global profit_percent
    try:
        if len(context.args) == 0:
            await update.message.reply_text("❌ Please provide a profit %. Example: /setprofit 10")
            return
        profit_percent = float(context.args[0])
        await update.message.reply_text(f"✅ Profit % updated to {profit_percent}")
    except ValueError:
        await update.message.reply_text("❌ Invalid number. Example: /setprofit 10")

# /reset command
async def reset_ledger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    ledger[user_id] = {"given": [], "repaid": []}
    await update.message.reply_text("🔄 Ledger reset successfully!")

# Handle messages (+amount, -amount, show ledger)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # Ensure user has a ledger
    if user_id not in ledger:
        ledger[user_id] = {"given": [], "repaid": []}

    # Record money given
    if text.startswith("+"):
        try:
            amount = float(text[1:])
            ledger[user_id]["given"].append(amount)
            await update.message.reply_text(f"💰 Recorded: You gave {amount}")
        except ValueError:
            await update.message.reply_text("❌ Invalid format. Use +5000")

    # Record money repaid
    elif text.startswith("-"):
        try:
            amount = float(text[1:])
            ledger[user_id]["repaid"].append(amount)
            await update.message.reply_text(f"💸 Recorded: {amount} repaid to you")
        except ValueError:
            await update.message.reply_text("❌ Invalid format. Use -2000")

    # Show ledger
    elif text.lower() == "show ledger":
        total_given = sum(ledger[user_id]["given"])
        total_repaid = sum(ledger[user_id]["repaid"])
        profit_amount = (total_given * profit_percent) / 100
        expected_return = total_given - profit_amount
        pending = expected_return - total_repaid

        msg = (
            f"📒 Your Ledger Report\n\n"
            f"Total Given: {total_given}\n"
            f"Profit %: {profit_percent}\n"
            f"Profit Amount: {profit_amount}\n"
            f"Expected Return (Given - Profit): {expected_return}\n\n"
            f"Total Repaid: {total_repaid}\n"
            f"Pending Balance: {pending}\n"
        )

        if pending == 0:
            msg += "\n✅ Deal Closed!"

        await update.message.reply_text(msg)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setprofit", set_profit))
    app.add_handler(CommandHandler("reset", reset_ledger))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Ledger Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
