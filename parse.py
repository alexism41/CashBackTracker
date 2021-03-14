import requests
from bs4 import BeautifulSoup
from datetime import date
from collections import namedtuple

today = date.today()
currentQuarter = ((today.month -1)//3)+1

DiscoverItCashBack = {
    "food": False,
    "travel": False,
    "gas": False,
    "other": False,
    "Base": 1
}
DiscoverCBCurrentOffer = ""
ChaseFreedom = {
    "food": False,
    "travel": False,
    "gas": False,
    "other": False,
    "Base": 1
}
ChaseFreedomCurrentOffer = ""
AECashMagnet = {
    "food": False,
    "travel": False,
    "gas": False,
    "other": False,
    "Base": 1.5
}
CitiQuicksilver = {
    "food": False,
    "travel": False,
    "gas": False,
    "other": False,
    "Base": 1.5
}
BestBuyVisa = {
    "food": False,
    "travel": False,
    "gas": False,
    "other": False,
    "Base": 1
}


def updateDeals():
    global DiscoverCBCurrentOffer 
    DiscoverCBCurrentOffer = getDiscoverDeal()

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
        DiscoverItCashBack.update({"gas": True})
    else:
        DiscoverItCashBack.update({"gas": False})
    if "Food" in DiscoverDeal or "Dining" in DiscoverDeal or "Restaurants" in DiscoverDeal or "Grocery" in DiscoverDeal:
        DiscoverItCashBack.update({"food": True})
    else:
        DiscoverItCashBack.update({"food": False})
    if "Travel" in DiscoverDeal:
        DiscoverItCashBack.update({"travel": True})
    else:
        DiscoverItCashBack.update({"travel": False})
    if DiscoverItCashBack.get("food") == False and DiscoverItCashBack.get("gas") == False and DiscoverItCashBack.get("travel") == False:
        DiscoverItCashBack.update({"other": True})
    else:
        DiscoverItCashBack.update({"other": False})

    return DiscoverDeal

def getChaseDeal():
    r = requests.get('https://creditcards.chase.com/cash-back-credit-cards/freedom/flex?CELL=60KX')
    soup = BeautifulSoup(r.text, "html.parser")
    ## find relevant data and store current deal for the quarter

def getBestBuyDeal():
    print("cannot access Best Buy site")


getBestBuyDeal()

