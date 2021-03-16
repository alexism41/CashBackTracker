import re
import requests
from enum import IntEnum
from bs4 import BeautifulSoup
from datetime import date
from collections import namedtuple

today = date.today()
currentQuarter = ((today.month -1)//3)+1

class Type(IntEnum):
    Discover = 1
    Chase = 2
    AmericanExpress = 3
    Citi = 4
    BestBuy = 5

BestCurrentDeals = {
    ## "category" : (cardType, value) ##
    "food": (0,1),
    "travel": (0,1),
    "gas": (0,1),
    "other": (0,1)
}


DiscoverItCashBack = {
    "food": 1,
    "travel": 1,
    "gas": 1,
    "other": 1,
    "Base": 1,
    "id": Type.Discover
}
DiscoverCBCurrentOffer = ""
ChaseFreedom = {
    "food": 1,
    "travel": 1,
    "gas": 1,
    "other": 1,
    "Base": 1,
    "id": Type.Chase
}
ChaseFreedomCurrentOffer = ""
AECashMagnet = {
    "food": 1.5,
    "travel": 1.5,
    "gas": 1.5,
    "other": 1.5,
    "Base": 1.5,
    "id": Type.AmericanExpress
}
CitiQuicksilver = {
    "food": 1.5,
    "travel": 1.5,
    "gas": 1.5,
    "other": 1.5,
    "Base": 1.5,
    "id": Type.Citi
}
BestBuyVisa = {
    "food": 2,
    "travel": 1,
    "gas": 3,
    "other": 1,
    "Base": 1,
    "id": Type.BestBuy
}
cardList = []
cardList.append(DiscoverItCashBack)
cardList.append(ChaseFreedom)
cardList.append(CitiQuicksilver)
cardList.append(AECashMagnet)
cardList.append(BestBuyVisa)

def updateDeals():
    global DiscoverCBCurrentOffer 
    DiscoverCBCurrentOffer = getDiscoverDeal()
    getChaseDeal()

def getDiscoverDeal():
    r = requests.get('https://www.discover.com/credit-cards/cashback-bonus/cashback-calendar.html')
    soup = BeautifulSoup(r.text, "html.parser")
    quarter = "q"+str(currentQuarter)

    for comp in soup.find_all(id = quarter):
        currentOffer = comp.p.text

    willSave = False
    DiscoverDeal = ""
    for word in currentOffer.split():
        if willSave and word != "from":
            DiscoverDeal += word + " "
        if word == "at":
            willSave = True
        if word == "from":
            willSave = False
            break
    
    if "Gas" in DiscoverDeal:
        DiscoverItCashBack.update({"gas": 5})
    else:
        DiscoverItCashBack.update({"gas": 1})
    if "Food" in DiscoverDeal or "Dining" in DiscoverDeal or "Restaurants" in DiscoverDeal or "Grocery" in DiscoverDeal:
        DiscoverItCashBack.update({"food": 5})
    else:
        DiscoverItCashBack.update({"food": 1})
    if "Travel" in DiscoverDeal:
        DiscoverItCashBack.update({"travel": 5})
    else:
        DiscoverItCashBack.update({"travel": 1})
    if DiscoverItCashBack.get("food") == 1 and DiscoverItCashBack.get("gas") == 1 and DiscoverItCashBack.get("travel") == 1:
        DiscoverItCashBack.update({"other": 5})
    else:
        DiscoverItCashBack.update({"other": 1})

    return DiscoverDeal

def getChaseDeal():
    r = requests.get('https://creditcards.chase.com/cash-back-credit-cards/freedom/flex?CELL=60KX')
    soup = BeautifulSoup(r.text, "html.parser")
    
    divList = soup.find_all("div", class_= "primary-item-content")
    offerDiv = divList[1]
    offersList = list()
    num = 1
    for tag in offerDiv.find_all("p"):
        if(num != 1):
            offersList.append(tag.text)
        num += 1
    

    for sentence in offersList:
        wordList = sentence.split()
        value = wordList[1]
        value = int(value[:-1])
        
        if "gas" in sentence.lower():
            ChaseFreedom.update({"gas": value})
        if "travel" in sentence.lower():
            ChaseFreedom.update({"travel": value})
        if "food" in sentence.lower() or "dining" in sentence.lower() or "grocery" in sentence.lower() or "restaurants" in sentence.lower():
            ChaseFreedom.update({"food": value})
        if "other" in sentence.lower():
            ChaseFreedom.update({"other": value}) 

def getBestInEach():
    updateDeals()
    maxFood = cardList[0].get("food")
    maxTravel = cardList[0].get("travel")
    maxGas = cardList[0].get("gas")
    maxOther = cardList[0].get("other")
    maxCard = cardList[0].get("id")
    BestCurrentDeals.update({"food": (maxCard, maxFood)})
    BestCurrentDeals.update({"travel": (maxCard, maxTravel)})
    BestCurrentDeals.update({"gas": (maxCard, maxGas)})
    BestCurrentDeals.update({"other": (maxCard, maxOther)})
    
    for card in range(1, len(cardList)):
        currentCard = cardList[card]["id"]
        if cardList[card]["food"] > maxFood:
            maxFood = cardList[card]["food"]
            BestCurrentDeals.update({"food": (currentCard, maxFood)})
        if cardList[card]["travel"] > maxTravel:
            maxTravel = cardList[card]["travel"]
            BestCurrentDeals.update({"travel": (currentCard, maxTravel)})
        if cardList[card]["gas"] > maxGas:
            maxGas = cardList[card]["gas"]
            BestCurrentDeals.update({"gas": (currentCard, maxGas)})
        if cardList[card]["other"] > maxOther:
            maxOther = cardList[card]["other"]
            BestCurrentDeals.update({"other": (currentCard, maxOther)})
    return BestCurrentDeals
