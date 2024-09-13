import settings
import bs
import bsUI
import os
import bsInternal
import time
import json
from threading import Timer
from random import randrange
from datetime import datetime
from settings import *
import logger
from logger import storage
correctAnswer = None
answeredBy = None
bankfile = logger.bank
customer = logger.customers


def _customer():
    if os.path.exists(customer):
        with open(customer) as f:
            _customer = json.loads(f.read())
            storage.customers = _customer
    return storage.customers


def commit_custom():
    if os.path.exists(customer):
        with open(customer, 'w') as f:
            f.write(json.dumps(storage.customers, indent=4))


# items = _customer()
# for item in items:
#     for i, e in items[item]["effects"].items():
#         now = datetime.now()
#         expiry = datetime.strptime(e, '%d-%m-%Y %H:%M:%S')
#         if expiry < now:
#             print 'expired item found'
#             items[item]['tag'] = ""
#             items.pop(i)

#sprint(storage.customers.keys())
def checkExpiredItems():
    now = datetime.now()
    items = storage.customers
    flag = 0
    expired = []
    for key, value in items.items():
        for i, e in value["effects"].items():
            expiry = datetime.strptime(e, '%d-%m-%Y %H:%M:%S')
            if expiry < now:
                if value["effects"] != {}:
                    #print(key, " remove: ", i)
                    value["effects"].pop(i)
                    flag=1
                    
        # Comprueba los que no poseen efectos.
        if value["effects"] == {}:
            #print("vacio")
            # agregalo a lista de jugadores sin efectos.
            expired.append(key)
            
    # Comprueba de que la lista no este vacia.
    if expired:
        # Remuevelo.
        for id in expired:
            items.pop(id)
            flag=1
            #print("remove: ", id)
    
    # Guarda los cambios.       
    if flag == 1:
        commit_custom()
def askQuestion():
    global answeredBy
    global correctAnswer
    keys = []
    for x in questionsList:
        keys.append(x)

    question = keys[randrange(len(keys))]
    correctAnswer = questionsList[question]
    if question == 'add':
        a = randrange(100, 999)
        b = randrange(10, 99)
        correctAnswer = str(a + b)
        question = 'What is ' + str(a) + ' + ' + str(b) + '?'
    elif question == 'multiply':
        a = randrange(100, 999)
        availableB = [0, 1, 10, 5]
        b = availableB[randrange(4)]
        correctAnswer = str(a * b)
        question = 'What is ' + str(a) + ' x ' + str(b) + '?'
    bsInternal._chatMessage(question)
    answeredBy = None
    checkExpiredItems()
    return


def checkAnswer(msg, clientID):
    global answeredBy
    if True:  # msg.lower() == correctAnswer:
        if answeredBy is not None:
            bsInternal._chatMessage('Already awarded to ' + answeredBy)
        else:
            for i in bsInternal._getForegroundHostActivity().players:
                if i.getInputDevice().getClientID() == clientID:
                    answeredBy = i.getName()
                    accountID = i.get_account_id()
                    bs.screenMessage(answeredBy + ': ' + msg,
                                     color=(0, 0.6, 0.2), transient=True)
            try:
                bsInternal._chatMessage(
                    'Congratulations ' + answeredBy + '! You won ' + bs.getSpecialChar('ticket') + '10.')
                addCoins(accountID, 10)
            except:
                pass

    '''else:
        bs.screenMessage('Wrong', color=(1, 0, 0), transient=True, clients=[clientID])'''
    return


def addCoins(accountID, amount):
    if os.path.exists(bankfile):
        with open(bankfile) as f:
            bank = json.loads(f.read())
    else:
        bank = {}
    if accountID not in bank:
        bank[accountID] = 0
    bank[accountID] += amount
    with open(bankfile, 'w') as f:
        f.write(json.dumps(bank, indent=4))
    if amount > 0:
        bs.playSound(bs.getSound('cashRegister'))
    print 'Transaction successful'


def getCoins(accountID):
    if os.path.exists(bankfile):
        with open(bankfile, 'r') as f:
            coins = json.loads(f.read())
            if accountID in coins:
                return coins[accountID]
    return 0


if settings.enableCoinSystem:
    timer = bs.Timer(questionDelay * 1000, askQuestion,
                     timeType='real', repeat=True)

