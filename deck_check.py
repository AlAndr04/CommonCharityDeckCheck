import requests
import json
import re

cardRarity = "Common"

def get_card_list():
    r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
    print(r.status_code)
    cards_reformed = {}
    cards = r.json()["data"]
    for card in cards:
        card.pop("id", None)
        for entry in card["card_images"]:
            key = str(entry["id"])
            if len(key) < 8:
                while len(key) < 8:
                    key = "0"+key
            cards_reformed[key] = card
    print(len(cards_reformed.items()))
    with open('data.json', 'w', encoding = 'utf8') as fp:
        json.dump(cards_reformed, fp, ensure_ascii=False)

def create_rarity_list_files(cardRarity):
    jointRarityName = cardRarity.replace(" ","")
    with open("data.json", "r", encoding='utf-8') as read_file:
        cards = json.load(read_file)
    f = open('list'+jointRarityName+'.txt', 'wb')
    commons = {}
    for card_id, card_info in cards.items():
        if "card_sets" in card_info:
            for printing in card_info["card_sets"]:
                if printing["set_rarity"] == cardRarity:
                    commons[card_id] = card_info["name"]
                    f.write((card_info["name"]+"\n").encode('utf-8'))
                    break
    f.close()
    with open('idTo'+jointRarityName+'.json', 'w') as fp:
        json.dump(commons, fp)

def check_deck_for_rarity(deckName, cardRarity):
    jointRarityName = cardRarity.replace(" ","")
    deckJson = {}
    deckJson["deckName"] = re.match("/?(.*?).ydk", deckName).group(1)
    deckJson["isOfRarity"] = True
    with open("data.json", "r", encoding='utf-8') as read_file:
        cards = json.load(read_file)
    with open("idTo"+jointRarityName+".json", "r", encoding='utf-8') as read_file:
        cardsOfRarity = json.load(read_file)
    with open(deckName, 'r', encoding='utf-8') as file:
        deck_cards = file.read().splitlines()
    for card in deck_cards:
        if card[0]!= "#" and card[0]!= "!":
            if len(card) < 8:
                while len(card) < 8:
                    card="0"+card
            if card not in cardsOfRarity.keys():
                deckJson["isOfRarity"] = False
                if card not in cards.keys():
                    if "unavailableCards" not in deckJson.keys():
                        deckJson["unavaiableCards"]=[card]
                    else:
                        deckJson["unavaiableCards"].append(card)
                elif "notCardsOfRarity" not in deckJson.keys():
                    deckJson["notCardsOfRarity"] = [cards[card]["name"]]
                elif deckJson["notCardsOfRarity"][-1] != cards[card]["name"]:
                    deckJson["notCardsOfRarity"].append(cards[card]["name"])
    return deckJson

def get_archetypes_for_rarity(cardRarity, minCards):
    jointRarityName = cardRarity.replace(" ","")
    archetypes={}
    with open("data.json", "r", encoding='utf-8') as read_file:
        cards = json.load(read_file)
    with open("idTo"+jointRarityName+".json", "r", encoding='utf-8') as read_file:
        cardsOfRarity = json.load(read_file)
    print(jointRarityName)
    for card_id, card_name in cardsOfRarity.items():
        if "archetype" in cards[card_id]:
            archetype = cards[card_id]["archetype"]
            if archetype not in archetypes.keys():
                archetypes[archetype] = [card_name]
            else:
                archetypes[archetype].append(card_name)
    archetypesWithMinCards = {}
    for archetype, cards in archetypes.items():
        if len(cards) >= minCards:
            archetypesWithMinCards[archetype] = cards
    return archetypesWithMinCards

if __name__ == "__main__":
    #get_card_list()
    #create_rarity_list_files("Common")
    #print(check_deck_for_rarity("RU IN FORCE.ydk", "Common"))
    print(get_archetypes_for_rarity("Common", 10))

