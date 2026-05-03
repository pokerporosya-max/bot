import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# храним игры в памяти
JOKER_GAMES = {}

# множители по шагам
MULTIPLIERS = [1.2, 1.44, 1.73, 2.07, 2.5]


# ---------------- START GAME ----------------
async def start_joker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("❌ джокер <ставка>")
        return

    bet = int(context.args[0])

    joker_pos = random.randint(0, 2)

    JOKER_GAMES[user_id] = {
        "bet": bet,
        "step": 0,
        "joker_pos": joker_pos,
        "message_id": None
    }

    await send_board(update, context, user_id)


# ---------------- BOARD ----------------
async def send_board(update, context, user_id):
    game = JOKER_GAMES[user_id]

    step = game["step"]
    multiplier = MULTIPLIERS[step]

    bet = game["bet"]
    win_now = int(bet * multiplier)

    text = (
        f"🎴 Игра: Джокер\n\n"
        f"💰 Банк: {bet} 🍬\n"
        f"📈 Множитель: x{multiplier}\n"
        f"💵 Выигрыш: {win_now} 🍬"
    )

    keyboard = [
        [
            InlineKeyboardButton("🂠", callback_data="0"),
            InlineKeyboardButton("🂠", callback_data="1"),
            InlineKeyboardButton("🂠", callback_data="2"),
        ],
        [
            InlineKeyboardButton("💰 Забрать", callback_data="take"),
            InlineKeyboardButton("❌ Отмена", callback_data="cancel"),
        ]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    if game["message_id"] is None:
        msg = await update.message.reply_text(text, reply_markup=markup)
        game["message_id"] = msg.message_id
    else:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=game["message_id"],
            text=text,
            reply_markup=markup
        )


# ---------------- CLICK ----------------
async def joker_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in JOKER_GAMES:
        await query.edit_message_text("❌ Игра не найдена")
        return

    game = JOKER_GAMES[user_id]
    step = game["step"]
    joker = game["joker_pos"]
    bet = game["bet"]

    data = query.data

    # ---------------- CANCEL ----------------
    if data == "cancel":
        del JOKER_GAMES[user_id]
        await query.edit_message_text(f"❌ Игра отменена\n💰 Ставка возвращена: {bet}")
        return

    # ---------------- TAKE MONEY ----------------
    if data == "take":
        multiplier = MULTIPLIERS[step]
        win = int(bet * multiplier)

        del JOKER_GAMES[user_id]
        await query.edit_message_text(
            f"💰 Забрал выигрыш!\n\n"
            f"💵 Получено: {win} 🍬\n"
            f"📈 x{multiplier}"
        )
        return

    # ---------------- CARD PICK ----------------
    choice = int(data)

    # ❌ проигрыш
    if choice != joker:
        board = create_board(joker, choice, reveal=True)

        del JOKER_GAMES[user_id]

        await query.edit_message_text(
            f"{board}\n\n💀 ПРОИГРЫШ\n- {bet} 🍬"
        )
        return

    # 🃏 ПОБЕДА
    game["step"] += 1
    game["joker_pos"] = random.randint(0, 2)

    board = create_board(joker, choice, reveal=True)

    multiplier = MULTIPLIERS[step]
    win_now = int(bet * multiplier)

    await query.edit_message_text(
        f"{board}\n\n"
        f"🎴 ДЖОКЕР!\n\n"
        f"💰 Банк: {bet} 🍬\n"
        f"📈 x{multiplier}\n"
        f"💵 Сейчас: {win_now} 🍬"
    )

    await send_board(update, context, user_id)


# ---------------- BOARD VISUAL ----------------
def create_board(joker, choice, reveal=False):
    cards = ["🂠", "🂠", "🂠"]

    if reveal:
        for i in range(3):
            if i == joker:
                cards[i] = "🃏"
            elif i == choice:
                cards[i] = "💀"

    return f"[ {cards[0]} ] [ {cards[1]} ] [ {cards[2]} ]"
