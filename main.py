import os
import time
import random

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from db import (
    init_db,
    get_user,
    update_balance,
    update_game,
    set_bonus_time,
    reset_db
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

BONUS_AMOUNT = 2500
COOLDOWN = 24 * 60 * 60


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id, user.first_name)

    await update.message.reply_text(
        "🎮 Gachyx\n\n➕ Добавить в группу"
    )

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    top_users = get_top()
    my_rank = get_user_rank(user_id)
    me = get_user(user_id)

    text = "🏆 ТОП БАЛАНСА\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for i, u in enumerate(top_users):
        mark = medals[i] if i < 3 else f"{i+1}."
        text += f"{mark} {u[1]} — {u[2]} 🍬\n"

    text += f"\n──────────────\n"
    text += f"👤 Ты: {me[1]}\n"
    text += f"📍 Место: #{my_rank}\n"
    text += f"💰 Баланс: {me[2]} 🍬"

    await update.message.reply_text(text)

# ---------- PROFILE ----------
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


# ---------- BALANCE ----------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    await update.message.reply_text(f"💰 Баланс: {user[2]} 🍬")


# ---------- CUBE ----------
async def cube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("❌ кубик <ставка>")
        return

    bet = int(context.args[0])
    user = get_user(user_id)

    if user[2] < bet:
        await update.message.reply_text("❌ нет средств")
        return

    update_balance(user_id, -bet)

    dice = await update.message.reply_dice("🎲")
    value = dice.dice.value

    if value in [4, 6]:
        win = bet * 2
        update_balance(user_id, win)
        update_game(user_id, True)
        await update.message.reply_text(f"🏆 Победа +{win} 🍬")
    else:
        update_game(user_id, False)
        await update.message.reply_text(f"💀 Проигрыш -{bet} 🍬")


# ---------- BONUS ----------
async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    now = int(time.time())
    last = user[6]

    if now - last < COOLDOWN:
        left = COOLDOWN - (now - last)
        h = left // 3600
        m = (left % 3600) // 60

        await update.message.reply_text(f"⏳ Бонус через {h}ч {m}м")
        return

    update_balance(user_id, BONUS_AMOUNT)
    set_bonus_time(user_id, now)

    await update.message.reply_text(f"🎁 +{BONUS_AMOUNT} 🍬")


# ---------- TRANSFER ----------
async def transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    sender = get_user(user_id)

    if not context.args:
        await update.message.reply_text("❌ перевод <сумма> [ID]")
        return

    amount = int(context.args[0])

    # reply mode
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    else:
        if len(context.args) < 2:
            await update.message.reply_text("❌ укажи ID")
            return
        target_id = int(context.args[1])
        target = get_user(target_id)

    if sender[2] < amount:
        await update.message.reply_text("❌ нет средств")
        return

    update_balance(user_id, -amount)
    update_balance(target.id, amount)

    await update.message.reply_text(
        f"💸 {sender[1]} отправил {amount} 🍬 {target.first_name}"
    )


# ---------- TEXT ----------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text in ["профиль", "/profile"]:
        await profile(update, context)

    elif text in ["баланс", "/balance"]:
        await balance(update, context)

    elif text.startswith("кубик") or text.startswith("/cube"):
        context.args = text.split()[1:]
        await cube(update, context)

    elif text in ["бонус", "/bonus"]:
        await bonus(update, context)

    elif text.startswith("перевод") or text.startswith("/transfer"):
        context.args = text.split()[1:]
        await transfer(update, context)


# ---------- RESET DB ----------
async def restart_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ нет доступа")
        return

    reset_db()
    await update.message.reply_text("🔄 БД очищена")


# ---------- MAIN ----------
def main():
    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("bonus", bonus))
    app.add_handler(CommandHandler("cube", cube))
    app.add_handler(CommandHandler("transfer", transfer))
    app.add_handler(CommandHandler("restart_db", restart_db))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Gachyx bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
