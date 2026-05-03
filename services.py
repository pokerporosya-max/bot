import random
from db import get_user, add, update
from utils import now


def bonus(uid):
    amount = random.randint(150, 250)
    add(uid, "balance", amount)
    return amount


def exchange(uid, amount):
    if amount < 100:
        return None

    user = get_user(uid)
    if user[1] < amount:
        return False

    bottles = amount // 100
    add(uid, "balance", -bottles * 100)
    add(uid, "bottles", bottles)
    return bottles


def fap(uid):
    user = get_user(uid)
    if user[2] < 1:
        return False

    add(uid, "bottles", -1)
    add(uid, "fap", 1)
    return True


def water(uid):
    grow = random.randint(1, 12)
    add(uid, "cactus", grow)
    return grow
