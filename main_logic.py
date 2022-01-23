import requests
import json
import re

cardRarity = "Common"

def get_card_list():
    r = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
    non_effect_effect_monsters = ["Tuner Monster", "Toon Monster", "Gemini Monster"]
    print(r.status_code)
    cards_reformed = {}
    cards = r.json()["data"]
    for card in cards:
        card.pop("id", None)
        if card["type"] in non_effect_effect_monsters:
            card["type"] = "Effect "+card["type"]
        for entry in card["card_images"]:
            key = str(entry["id"])
            if len(key) < 8:
                while len(key) < 8:
                    key = "0"+key
            cards_reformed[key] = card
    print(len(cards_reformed.items()))
    with open('data.json', 'w', encoding = 'utf8') as fp:
        json.dump(cards_reformed, fp, ensure_ascii=False)

def get_types():
    dictio = {}
    with open("data.json", "r", encoding='utf-8') as read_file:
        cards = json.load(read_file)
    for card in cards.values():
        if not dictio.get(card["type"]):
            dictio[card["type"]] = 1
        else:
            dictio[card["type"]]+=1
    return dictio

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
            if not archetypes.get(archetype):
                archetypes[archetype] = {card_name:0}
            elif not archetypes[archetype].get(card_name):
                archetypes[archetype][card_name]=0
    archetypesWithMinCards = {}
    for archetype, cards in archetypes.items():
        list_cards = list(cards.keys())
        if len(list_cards) >= minCards:
            archetypesWithMinCards[archetype] = list_cards
    return archetypesWithMinCards

def search_cards_by_spec(cardRarity, search_json):
    jointRarityName = cardRarity.replace(" ","")
    card_list = {}
    with open("data.json", "r", encoding='utf-8') as read_file:
        cards = json.load(read_file)
    with open("idTo"+jointRarityName+".json", "r", encoding='utf-8') as read_file:
        cardsOfRarity = json.load(read_file)
    for card_id in cardsOfRarity:
        match = True
        if (search_json["name"] != ""
            and search_json["name"].lower()
            not in cards[card_id]["name"].lower()):
            match = False
        if (search_json["effect"] != ""
            and search_json["effect"].lower()
            not in cards[card_id]["desc"].lower()):
            match = False
        if search_json["type"] != "":
            if (search_json["type"].lower()
                not in cards[card_id]["type"].lower()):
                match = False
            elif search_json["sub_type"] != "":
                if search_json["type"].lower() == "monster":
                    sub_type_correct = search_json["sub_type"].lower() in cards[card_id]["type"].lower() 
                else:
                    sub_type_correct = search_json["sub_type"].lower() == cards[card_id]["race"].lower()
                if not sub_type_correct:
                    match = False
            if "monster" in cards[card_id]["type"].lower():
                if (search_json["attribute"] != ""
                        and search_json["attribute"].lower()
                        != cards[card_id]["attribute"].lower()):
                    match = False
                if search_json["level"].isnumeric():
                    if "link" in cards[card_id]["type"].lower():
                        level = cards[card_id]["linkval"]
                    else:
                        level = cards[card_id]["level"]
                    if int(search_json["level"]) != level:
                        match = False
                elif search_json["level"] != "":
                    match = False
                if search_json["ATK"].isnumeric():
                    if int(search_json["ATK"]) != cards[card_id]["atk"]:
                        match = False
                elif search_json["ATK"] != "":
                    match = False
                if search_json["DEF"].isnumeric():
                    if "link" in cards[card_id]["type"].lower():
                        match = False
                    elif int(search_json["DEF"]) != cards[card_id]["def"]:
                        match = False
                elif search_json["DEF"] != "":
                    match = False
                if (search_json["is_penlum"]
                    and "pendulum" not in cards[card_id]["type"].lower()):
                    match = False
                
        if (search_json["monster_type"] != ""
            and search_json["monster_type"].lower()
            != cards[card_id]["race"].lower()):
            match = False
        if (search_json["monster_sub_type"] != ""
            and search_json["monster_sub_type"].lower()
            not in cards[card_id]["type"].lower()):
            match = False
        
        if match:
            card_list[cards[card_id]["name"]] = cards[card_id]["desc"]
    return card_list
if __name__ == "__main__":
    #get_card_list()
    #create_rarity_list_files("Common")
    #print(check_deck_for_rarity("RU IN FORCE.ydk", "Common"))
    print(search_cards_by_spec("Common", {"name":"Odd-Eyes", "effect":"",
                                          "type":"monster",
                                          "sub_type":"effect",
                                          "monster_type":"",
                                          "monster_sub_type":"",
                                        "attribute":"dark",
                                        "level":"",
                                        "ATK":"2500",
                                        "DEF": "",
                                        "is_penlum":True}))

