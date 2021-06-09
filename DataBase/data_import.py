import sqlite3 as sql
import requests
import json
import os, sys

class Card():
    """ Card info """
    def __init__(self, card_json):
        """ English card json """
        self.card_json = card_json
    
    def eng_card_name(self):
        """ English card name """
        return self.card_json['name']

    def rus_card_name(self):
        """ Russian card name """
        set_name = self.card_json['set']
        card_number = self.card_json['collector_number']
        rus_card_link = ''.join((f'http://api.scryfall.com/cards/{set_name}/{card_number}/ru'))
        rus_card_request = requests.get(rus_card_link)
        rus_card_json = rus_card_request.json()
        if rus_card_request.status_code == 404:
            return ('-')
        else:
            if 'printed_name' in rus_card_json:
                return rus_card_json['printed_name']
            else:
                return ''.join((f'{rus_card_json["card_faces"][0]["printed_name"]} // {rus_card_json["card_faces"][1]["printed_name"]}'))
    def card_image(self):
        if 'image_uris' in self.card_json:
            return self.card_json['image_uris']['normal']
        else:
            return self.card_json['card_faces'][0]['image_uris']['normal']


def add_card(card_name):
    for card in card_name:
        try:
            card.replace('//','+')
            card_request_string = ''.join((f'http://api.scryfall.com/cards/named?fuzzy={card.replace(" ","+")}'))
            card_request = requests.get(card_request_string)
            card_json = card_request.json()
            card_class = Card(card_json)
            card_insert = (card_class.eng_card_name(), card_class.rus_card_name(), card_class.card_image())
            cur.execute("INSERT OR IGNORE INTO cards VALUES(?,?,?);", card_insert)
            conn.commit()
        except:
            print('')

path = ''.join(f'{os.getcwd()}/ScryfallDataBase.db')
conn = sql.connect(path) #connecting to the database
cur = conn.cursor()
resp = requests.get('https://api.scryfall.com/catalog/card-names') #getting the card names
link = ''.join('https://api.scryfall.com/catalog/card-names')
link_request = requests.get(link)
link_json = link_request.json()
add_card(link_json['data'])