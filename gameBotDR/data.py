from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import Dispatcher
from constants import *

#
# Данные.
#

# Данные бота
bot = Bot(token=TOKEN1)
dp = Dispatcher(bot)

# Какой-то объект
someObj = ""

# Подсказка
sHint = {"code":"23849612818915214", "hint":"🎉🎉🎉 С днем рождения! 🎉🎉🎉"}

# Координаты позиции Игрока
curPlayerPos = [None, None, None] # первый и второй - это уравень массива
posByDefault = \
[
    46, 14, 
    {
        "rotat": 
        [
            {"lvl":0, "op":-1}, # UP
            {"lvl":1, "op":-1}, # Left
            {"lvl":0, "op": 1}, # DOWN
            {"lvl":1, "op": 1}  # RIGHT
        ]
    }
]

# // 
def myPos(msg, ps):
    global curPlayerPos
    return msg.answer("Вы находитесь в позиции: ["+str(ps[0])+", "+str(ps[1])+"]")

# Кнопки джестика
actvActionBtn = False
jestik = \
[
    [
        types.KeyboardButton(text="-90°"),
        types.KeyboardButton(text="Up"),
        types.KeyboardButton(text="+90°")
    ],
    [
        types.KeyboardButton(text="Left"),
        types.KeyboardButton(text="Down"),
        types.KeyboardButton(text="Right")
    ]
]

# Варинты действий
options = ""
keyOpts = ONE  # по умолчанию один
answOpts = ""

# // 
def getOpts():
    global options
    return options

# // 
def setOpts(data=""):
    global options
    options = data

# // 
def listOptions(msg, keyboard, k):
    global options
    tmpOpt = options["opt"]
    st = tmpOpt["title"]
    for opt in tmpOpt["select"][k]:
        st += opt
    return msg.answer(st, reply_markup=keyboard)


# qr-code 1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣0️⃣
# answer: 23 84 96 12 8 18 91 5 2 14
qrcodes = \
{
                           - qrcode - 
}

# // 
def getQrcode(obj):
    global qrcodes
    return qrcodes[obj]

# // 
def qrCodeSolved(obj):
    global qrcodes
    qrcodes[obj]["solved"] = True

# // 
def qrCodeNum(st):
    global qrcodes
    for k, v in qrcodes.items():
        if st == v["code"].lower() and v["solved"]:
            return v["N"]
    return ""

# // 
def qtyQrCodes(bl=True):
    global qrcodes
    
    result = ""
    solved = 0
    notSolved = 0
    for k, v in qrcodes.items():
        if v["solved"]:
            solved += 1
        else:
            notSolved += 1
    if bl:
        result = "✅ Найдено  "+str(solved)+"\n❌ Осталось "+str(notSolved)
    else:
        result = "❌ Осталось "+str(notSolved)

    return result

# // Помощь
def help(msg):
    hst = \
    {
        "h":     "help - показать справку",
        "qtyQr": "qrcode - сколько найдено/осталось",
        "mps":   "mps - текущая позиция на сетке",
        "btn": 
        [
            "Up - вперед", 
            "Down - вниз", 
            "Left - влево", 
            "Right - вправо",
            "-90° - поворот против часовой стрелке",
            "+90° - поворот по часовой стрелке"
        ],
        "d": "Действие - что ты будешь делать"
    }
    
    s = "+====================================+\n"
    s += "= "+hst["h"]+"\n"
    s += "=\n"
    s += "= "+hst["qtyQr"]+"\n"
    s += "=\n"
    s += "= "+hst["mps"]+"\n"
    s += "=\n"
    s += "= "+hst["btn"][0]+"\n"
    s += "= "+hst["btn"][1]+"\n"
    s += "= "+hst["btn"][2]+"\n"
    s += "= "+hst["btn"][3]+"\n"
    s += "= "+hst["btn"][4]+"\n"
    s += "= "+hst["btn"][5]+"\n"
    s += "=\n"
    s += "= "+hst["d"]+"\n"
    s += "+====================================+\n"

    return msg.answer(s)
