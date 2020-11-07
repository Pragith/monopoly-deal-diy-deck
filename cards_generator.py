#%%
import yaml, math, cairo

# Read the cards database
with open('db/default.yaml','r') as db:
    cards_db = yaml.safe_load(db)

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

# %%
# Create & Draw on the template

# Read the card template:
with open('config/card.yaml','r') as db:
    card_template = yaml.safe_load(db)
height_mm = card_template['height_mm']
width_mm = card_template['width_mm']
dpi = card_template['dpi']
cards_per_page = card_template['cards_per_page']

WIDTH, HEIGHT = int((dpi*width_mm)/(25.44*cards_per_page)), int((dpi*height_mm)/(25.44*cards_per_page))
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
context = cairo.Context(surface)

def draw_1(ctx, width, height):
    ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

    pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
    pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
    pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity

    ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    ctx.set_source(pat)
    ctx.fill()

    ctx.translate(0.1, 0.1)  # Changing the current transformation matrix

    ctx.move_to(0, 0)
    # Arc(cx, cy, radius, start_angle, stop_angle)
    ctx.arc(0.2, 0.1, 0.1, -math.pi / 2, 0)
    ctx.line_to(0.5, 0.1)  # Line to (x,y)
    # Curve(x1, y1, x2, y2, x3, y3)
    ctx.curve_to(0.5, 0.2, 0.5, 0.4, 0.2, 0.8)
    ctx.close_path()

    ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
    ctx.set_line_width(0.02)
    ctx.stroke()

def draw_2(cr, width, height):
    cr.scale(width, height)
    cr.set_line_width(0.4)

    cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(0.2)

    cr.move_to(0.09, 0.23)
    cr.show_text("Hello")

    cr.move_to(0.27, 0.65)
    cr.text_path("World")
    cr.set_source_rgb(0.5, 0.5, 1)
    cr.fill_preserve()
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(0.01)
    cr.stroke()

    # draw helping lines
    cr.set_source_rgba(1, 0.2, 0.2, 0.6)
    cr.arc(0.04, 0.53, 0.02, 0, 2 * math.pi)
    cr.arc(0.27, 0.65, 0.02, 0, 2 * math.pi)
    cr.fill()

def draw_3(cr, width, height):
    cr.scale(width, height)
    cr.set_line_width(0.04)

    # a custom shape, that could be wrapped in a function
    x0 = 0.1  # parameters like cairo_rectangle
    y0 = 0.1
    rect_width = 0.8
    rect_height = 0.8
    radius = 0.4  # and an approximate curvature radius

    x1 = x0 + rect_width
    y1 = y0 + rect_height

    if rect_width / 2 < radius:
        if rect_height / 2 < radius:
            cr.move_to(x0, (y0 + y1) / 2)
            cr.curve_to(x0, y0, x0, y0, (x0 + x1) / 2, y0)
            cr.curve_to(x1, y0, x1, y0, x1, (y0 + y1) / 2)
            cr.curve_to(x1, y1, x1, y1, (x1 + x0) / 2, y1)
            cr.curve_to(x0, y1, x0, y1, x0, (y0 + y1) / 2)
        else:
            cr.move_to(x0, y0 + radius)
            cr.curve_to(x0, y0, x0, y0, (x0 + x1) / 2, y0)
            cr.curve_to(x1, y0, x1, y0, x1, y0 + radius)
            cr.line_to(x1, y1 - radius)
            cr.curve_to(x1, y1, x1, y1, (x1 + x0) / 2, y1)
            cr.curve_to(x0, y1, x0, y1, x0, y1 - radius)
    else:
        if rect_height / 2 < radius:
            cr.move_to(x0, (y0 + y1) / 2)
            cr.curve_to(x0, y0, x0, y0, x0 + radius, y0)
            cr.line_to(x1 - radius, y0)
            cr.curve_to(x1, y0, x1, y0, x1, (y0 + y1) / 2)
            cr.curve_to(x1, y1, x1, y1, x1 - radius, y1)
            cr.line_to(x0 + radius, y1)
            cr.curve_to(x0, y1, x0, y1, x0, (y0 + y1) / 2)
        else:
            cr.move_to(x0, y0 + radius)
            cr.curve_to(x0, y0, x0, y0, x0 + radius, y0)
            cr.line_to(x1 - radius, y0)
            cr.curve_to(x1, y0, x1, y0, x1, y0 + radius)
            cr.line_to(x1, y1 - radius)
            cr.curve_to(x1, y1, x1, y1, x1 - radius, y1)
            cr.line_to(x0 + radius, y1)
            cr.curve_to(x0, y1, x0, y1, x0, y1 - radius)

    cr.close_path()

    cr.set_source_rgb(0.5, 0.5, 1)
    cr.fill_preserve()
    cr.set_source_rgba(0.5, 0, 0, 0.5)
    cr.stroke()

#draw_1(context, WIDTH, HEIGHT)
draw_2(context, WIDTH, HEIGHT)
#draw_3(context, WIDTH, HEIGHT)

surface.write_to_png("decks/png/test1.png")  # Output to PNG
# %%
# %%



# %%

# %%
