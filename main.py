import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from db import init_db, get_user, update_balance, update_game

TOKEN = os.getenv("BOT_TOKEN")

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id, user.first_name)

    await update.message.reply_text(
        "🎮 Добро пожаловать в Gachyx\n\n➕ Добавить в группу"
    )

# --- PROFILE ---
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    await update.message.reply_text(
        f"👤 Профиль\n\n"
        f"Имя: {user[1]}\n"
        f"ID: {user[0]}\n"
        f"🍬 Баланс: {user[2]}\n"
        f"🎮 Игры: {user[3]}\n"
        f"🏆 Победы: {user[4]}\n"
        f"❌ Поражения: {user[5]}"
    )

# --- BALANCE ---
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(f"💰 Баланс: {user[2]} 🍬")

# --- BONUS ---
async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    update_balance(user_id, 2500)
    await update.message.reply_text("🎁 +2500 🍬")

# --- CUBE GAME ---
async def cube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("❌ Укажи ставку: кубик 100")
        return

    bet = int(context.args[0])
    user = get_user(user_id)

    if user[2] < bet:
        await update.message.reply_text("❌ Недостаточно средств")
        return

    update_balance(user_id, -bet)

    dice = await update.message.reply_dice(emoji="🎲")
    value = dice.dice.value

    if value in [4, 6]:
        win = bet * 2
        update_balance(user_id, win)
        update_game(user_id, True)
        await update.message.reply_text(f"🏆 Победа +{win} 🍬")
    else:
        update_game(user_id, False)
        await update.message.reply_text(f"💀 Проигрыш -{bet} 🍬")

# --- TEXT COMMANDS ---
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.effective_user.id

    get_user(user_id, update.effective_user.first_name)

    if text == "профиль":
        await profile(update, context)

    elif text == "баланс":
        await balance(update, context)

    elif text == "игры":
        await update.message.reply_text("🎮 Кубик")

    elif text.startswith("кубик"):
        context.args = text.split()[1:]
        await cube(update, context)

    elif text == "бонус":
        await bonus(update, context)

# --- MAIN ---
def main():
    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("bonus", bonus))
    app.add_handler(CommandHandler("cube", cube))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
