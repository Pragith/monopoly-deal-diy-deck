#%%
import yaml, json

## FUNCTIONS
def update_main_template(MARKER_CARDS):
    ## TEMPLATE - MAIN
    with open('templates/v3-vanilla/template-index.html', 'r') as file:
        t_index = file.read()

    with open('templates/v3-vanilla/index.html', 'w') as file:
        file.write(t_index.replace('MARKER_CARDS', MARKER_CARDS))


## EXECUTION

# Read the project configuration
with open('config/card.yaml','r') as cnf:
    config = yaml.safe_load(cnf)

# Read the cards database
with open(f'db/{config["db"]}.yaml','r') as db:
    cards_db = yaml.safe_load(db)

    # Write the cards database to JSON
    f = open(f'db/{config["db"]}.json','w')
    f.write(json.dumps(cards_db))
    f.close()

property_regular = cards_db['cards']['property']['regular']
property_wild = cards_db['cards']['property']['wild']
action = cards_db['cards']['action']
money = cards_db['cards']['money']

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
print(f'> Total cards in the database: {total_cards}')


# Create cards & Draw on the template
all_cards = []


## TEMPLATE - MONEY
cards_money = []
with open('templates/v3-vanilla/template-money.html', 'r') as file:
    t_money = file.read()

for card in money:
    for qty in range(card['qty']):
        card_money = t_money.replace('MARKER_VALUE', str(card['value']))
        cards_money.append(card_money)

all_cards.append(''.join(cards_money))

## TEMPLATE - ACTION
cards_action = []
with open('templates/v3-vanilla/template-action.html', 'r') as file:
    t_action = file.read()

for card in action:
    for qty in range(card['qty']):
        card_action = t_action.replace('MARKER_MONEY', str(card['money'])).replace('MARKER_DESCRIPTION', card['description']).replace('MARKER_TITLE', card['title'])
        cards_action.append(card_action)

all_cards.append(''.join(cards_action))

## TEMPLATE - PROPERTY - REGULAR
cards_property_r = []
with open('templates/v3-vanilla/template-property-regular.html', 'r') as file:
    t_property_r = file.read()

for card in property_regular:
    for qty in range(card['qty']):
        card_rent_rows = ''
        rent_index = 1        
        for rent in card['rents']:
            card_rent_row = ''
            rent_css_index = len(card['rents'])        
            with open('templates/v3-vanilla/template-property-rent-row.html', 'r') as file:
                t_rent_row = file.read()
                card_rent_row = t_rent_row.replace('MARKER_RENT_AMOUNT', str(rent))
                card_rent_set = []
                with open('templates/v3-vanilla/template-property-rent-card-set.html', 'r') as file:
                    t_rent_set = file.read()
                    rent_card_index = 1                    
                    for rent_i in range(rent_index):      
                        card_rent_set.append(t_rent_set.replace('MARKER_CARD_DISPLAY_INDEX', str(rent_index)).replace('MARKER_CARD_CSS_INDEX', str(rent_css_index)))
                        rent_css_index -= 1                        
                card_rent_set.reverse()
                card_rent_set = ''.join(card_rent_set)
                card_rent_row = card_rent_row.replace('MARKER_RENT_CARD_SET', card_rent_set)
            card_rent_rows += card_rent_row
            rent_index += 1
        card_property_r = t_property_r.replace('MARKER_RENT_ROW', card_rent_rows).replace('MARKER_MONEY', str(card['money'])).replace('MARKER_TITLE', card['title']).replace('MARKER_COLOR', card['color'])
        cards_property_r.append(card_property_r)

all_cards.append(''.join(cards_property_r))



# Update the main template
MARKER_CARDS = ''
for card in all_cards:
    MARKER_CARDS += ''.join(card)
update_main_template(MARKER_CARDS)



# %%
# %%
