import requests
import json

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

def create_common_list_files():    
    with open("data.json", "r", encoding='utf-8') as read_file:
        cards = json.load(read_file)
    f = open('list_common.txt', 'wb')
    commons = {}
    for card_id, card_info in cards.items():
        if "card_sets" in card_info:
            for printing in card_info["card_sets"]:
                if printing["set_rarity"] == "Common":
                    commons[card_id] = card_info["name"]
                    f.write((card_info["name"]+"\n").encode('utf-8'))
                    break
    f.close()
    with open('id_to_common.json', 'w') as fp:
        json.dump(commons, fp)

def check_deck_for_commons(deck_name):
    is_common = True
    not_common_cards = []
    unavailable_cards = []
    with open("data.json", "r", encoding='utf-8') as read_file:
        cards = json.load(read_file)
    with open("id_to_common.json", "r", encoding='utf-8') as read_file:
        commons = json.load(read_file)
    with open(deck_name, 'r', encoding='utf-8') as file:
        deck_cards = file.read().splitlines()
    for card in deck_cards:
        if card[0]!= "#" and card[0]!= "!":
            if len(card) < 8:
                while len(card) < 8:
                    card="0"+card
            if card not in commons.keys():
                is_common = False
                if card not in cards.keys():
                    unavailable_cards.append(card)
                elif len(not_common_cards) == 0 or (len(not_common_cards) > 0
                                                  and not_common_cards[-1] != cards[card]["name"]):
                    not_common_cards.append(cards[card]["name"])
    if is_common:
        result = "The deck {} is legal for common charity.\n".format(deck_name)
    else:
        result = "The deck {} is not legal for common charity\n".format(deck_name)
        if len(unavailable_cards) > 0:
            result+= ("WARNING: Some of the card ids were not found in the database.\n"
            +"Please check that the following ids belong to cards and that the deck is not outdated:\n")
            for card_id in unavailable_cards:
                result+=card_id+"\n"
        result+="The illegal cards in the deck are:\n"
        for card in not_common_cards:
            result+=card+"\n"
    return result

if __name__ == "__main__":
    #get_card_list()
    #create_common_list_files()
    check_deck_for_commons("RU IN FORCE.ydk")

