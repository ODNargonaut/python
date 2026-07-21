from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from constants import *
from data import *
from mapGrid import *


# // Проверка на наличие столкновений с объектами
def checkForCollisionsWithObj(newPos):
    global curPlayerPos, mapGrid, someObj

    Obj = mapGrid[newPos[0]][newPos[1]]
    if Obj == EMPTYSPACE:
        curPlayerPos = newPos[:]
    elif Obj == OBJCARPER:
        curPlayerPos = newPos[:]
    elif Obj == OBJDOORMYROOM:
        curPlayerPos = newPos[:]
    elif Obj == OBJCORRIDORDOOR:
        curPlayerPos = newPos[:]
    elif Obj == OBJDENDOOR:
        curPlayerPos = newPos[:]
    elif Obj == OBJPLASTICCARPER:
        curPlayerPos = newPos[:]
    elif Obj == OBJTOILETDOOR:
        curPlayerPos = newPos[:]
    elif Obj == OBJBATHROOMDOOR:
        curPlayerPos = newPos[:]
    elif Obj == OBJENTRANCEDOOR:
        curPlayerPos = newPos[:]
    elif Obj == OBJFRONTDOOR:
        curPlayerPos = newPos[:]
    elif Obj == OBJFOOTWEAR:
        curPlayerPos = newPos[:]
    elif Obj == OBJSHOEBAGS:
        curPlayerPos = newPos[:]
    elif Obj == OBJCATTRAY:
        curPlayerPos = newPos[:]
        
    someObj = sceneObjects[Obj]


# // 
def rotation(h, msg):
    global jestik, curPlayerPos
    ar = curPlayerPos[2]["rotat"]
    offset = 0

    # если была добавлена кнопка
    if actvActionBtn:
        offset = 1
    else:
        offset = 0
    
    if h == "+":
        # меняем местами кнопки по часовой
        tmp1 = jestik[1+offset][2]
        jestik[1+offset][2] = jestik[0+offset][1]
        tmp2 = jestik[1+offset][1]
        jestik[1+offset][1] = tmp1
        jestik[0+offset][1] = jestik[1+offset][0]
        jestik[1+offset][0] = tmp2
        # меняем их действия по часовой
        tmp1 = ar[0]
        ar[0] = ar[3]
        ar[3] = ar[2]
        ar[2] = ar[1]
        ar[1] = tmp1
    elif h == "-":
        # меняем местами кнопки против часовой
        tmp1 = jestik[1+offset][0]
        jestik[1+offset][0] = jestik[0+offset][1]
        tmp2 = jestik[1+offset][1]
        jestik[1+offset][1] = tmp1
        jestik[0+offset][1] = jestik[1+offset][2]
        jestik[1+offset][2] = tmp2
        # меняем их действия против часовой
        tmp1 = ar[1]
        ar[1] = ar[2]
        ar[2] = ar[3]
        ar[3] = ar[0]
        ar[0] = tmp1

    keyboard = types.ReplyKeyboardMarkup \
    (
        keyboard=jestik,
        resize_keyboard=True
    )
    if actvActionBtn:
        keyboard = actionBtn(False)
        setOpts()
    else:
        setOpts()

    return msg.answer(".", reply_markup=keyboard)


# // 
def movement(direct):
    newPos = curPlayerPos[:]
    rot = newPos[2]["rotat"]

    if direct == DUP:
        newPos[rot[0]["lvl"]] += (STEP*rot[0]["op"])
    elif direct == DLEFT:
        newPos[rot[1]["lvl"]] += (STEP*rot[1]["op"])
    elif direct == DDOWN:
        newPos[rot[2]["lvl"]] += (STEP*rot[2]["op"])
    elif direct == DRIGHT:
        newPos[rot[3]["lvl"]] += (STEP*rot[3]["op"])
    
    # Проверка столкновений с объектами
    checkForCollisionsWithObj(newPos)


# // 
def actionBtn(bl):
    if bl:
        jestik.insert(0, [types.KeyboardButton(text="Действие")])
    else:
        del jestik[0]

    keyboard = types.ReplyKeyboardMarkup \
    (
        keyboard=jestik,
        resize_keyboard=True
    )
    return keyboard

# // Отобразить кнопку с данными
def displayBtnWithData(bl, msg, someObj):
    global actvActionBtn, keyOpts
    if bl:
        setOpts(someObj[2])
    else:
        setOpts()
        keyOpts = ONE
        answOpts = ""
    actvActionBtn = bl
    return msg.answer(someObj[0], reply_markup=actionBtn(someObj[1]))


# // Выбранный вариант
def selectedOption(s):
    global actvActionBtn, keyOpts
    if not actvActionBtn and getOpts() != "":
        descr = getOpts()["opt"]["description"][keyOpts]
        qr = getOpts()["opt"]["qr"]
        if s == VARIANT1 and int(VARIANT1) <= len(descr):
            return descr[s]
        elif s == VARIANT2 and int(VARIANT2) <= len(descr):
            return descr[s]
        elif s == VARIANT3 and int(VARIANT3) <= len(descr):
            return descr[s]
        elif s == VARIANT4 and int(VARIANT4) <= len(descr):
            return descr[s]
        elif s == VARIANT5 and int(VARIANT5) <= len(descr):
            return descr[s]
        elif s == qr["code"].lower() and qr["k"] == keyOpts and qr["answ"] == answOpts:
            qrCodeSolved(getOpts()["Name"])
    return ""


# // 
def hint(st):
    if st == sHint["code"]:
        return sHint["hint"]
    return ""


# // Start ф-ия
@dp.message_handler(commands=['start'])
async def Start(msg: types.Message):
    global curPlayerPos, posByDefault, jestik

    keyboard = types.ReplyKeyboardMarkup \
    (
        keyboard=jestik,
        resize_keyboard=True
    )

    curPlayerPos = posByDefault
    
    await msg.answer("🔥🔥Игра началась!🔥🔥", reply_markup=keyboard)
    await help(msg)
    await msg.answer("Ваша цель - найти все QrCode!\n"+qtyQrCodes())
    await myPos(msg, curPlayerPos)
    print("user: "+msg.from_user.full_name)


# // Определение направлений и действий
@dp.message_handler(content_types=['text'])
async def DetermOfDirecAndActns(msg: types.Message):
    global someObj, jestik, actvActionBtn, options, curPlayerPos, keyOpts, answOpts

    mtext = msg.text.lower()

    hnt = hint(mtext)
    if hnt != "":
        await msg.answer(hnt)

    sel = selectedOption(mtext)
    if sel != "":
        answOpts = mtext
        await msg.answer(" ".join(sel["s"].split()))
        if sel["k"] != NULL:
            answOpts = ""
            keyOpts = sel["k"]
            await displayBtnWithData(True, msg, [".", True, getOpts()])

    if mtext == DLEFT:
        movement(DLEFT)
    elif mtext == DUP:
        movement(DUP)
    elif mtext == DDOWN:
        movement(DDOWN)
    elif mtext == DRIGHT:
        movement(DRIGHT)
    elif mtext == DCLOCKWISE:
        await rotation("+", msg)
        actvActionBtn = False
        keyOpts = ONE
        answOpts = ""
    elif mtext == DCOUNTERCLOCKWISE:
        await rotation("-", msg)
        actvActionBtn = False
        keyOpts = ONE
        answOpts = ""
    elif mtext == ACTION:
        await listOptions(msg, actionBtn(False), keyOpts)
        actvActionBtn = False
    elif mtext == QTYQRCODE:
        await msg.answer(qtyQrCodes())
    elif mtext == HELP:
        await help(msg)
    elif mtext == MYPOS:
        await myPos(msg, curPlayerPos)

    if someObj != "":
        if not actvActionBtn and someObj[1] and mtext == DUP:
            await displayBtnWithData(True, msg, someObj)
        elif actvActionBtn and not someObj[1]:
            await displayBtnWithData(False, msg, someObj)
        else:
            if someObj[2]["Name"] != EMPTYSPACE:
                await msg.answer(someObj[0])
            if not actvActionBtn:
                setOpts()
                keyOpts = ONE
                answOpts = ""
        someObj = ""

    qrN = qrCodeNum(mtext)
    if qrN != "":
        await msg.answer(qrN)

    print("lvl "+str(keyOpts)+" lvl")
    
    ps = curPlayerPos
    print("Направление: "+mtext)
    print("Позиция: ["+str(ps[0])+", "+str(ps[1])+"]")
    print("Выбранный ответ: "+str(answOpts))
    print("user: "+msg.from_user.full_name)


# // Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp)