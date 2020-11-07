#%%
import yaml


#%%
# Read the cards database
with open('cards_db.yaml','r') as db:
    cards_db = yaml.safe_load(db)

property_regular = cards_db['cards']['property']['regular']
property_wild = cards_db['cards']['property']['wild']
action = cards_db['cards']['action']
money = cards_db['cards']['money']


# %%
# Total cards check:
'''
106 Total
20 Money
34 Action
13 Rent
28 Property Regular
11 Property Wild
'''
total_cards = 0

for card in property_regular:
    total_cards += card['qty']

for card in property_wild:
    total_cards += card['qty']

for card in action:
    total_cards += card['qty']

for card in money:
    total_cards += card['qty']

total_cards
# %%
