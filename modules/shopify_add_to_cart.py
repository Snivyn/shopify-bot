# shopify add to cart
# developed by @snivynGOD

import requests
from bs4 import BeautifulSoup as bs
import webbrowser


def add_to_cart(site, variant):
    '''
    (str, str, int) -> str
    Given a site and a variant ID, a link with the product added to the cart
    will be returned.
    >>>add_to_cart(https://shop.antisocialsocialclub.com/, 1488552847,1)
    https://shop.antisocialsocialclub.com/cart/1488552847:1/
    '''
    URL = site + variant + ":1"
    return URL

print("------------------------------------------------------------------")
print("shopify add to cart v1.0")
print("Adds products to cart and displays it in a web browser.")
print("developed by @snivynGOD")
print("------------------------------------------------------------------\n")

user_site = input("[INPUT] What site do you want to buy from?: ")
cart_link = "https://" + user_site + "/cart/"
user_url = input("[INPUT] What product were you looking at?: ")

# Specifying a site and collecting raw page data
print("[INFO] Collecting raw data...")
res = requests.get(user_url + ".xml")
page = bs(res.text, "lxml")
data = page.select(".")

# Parsing necessary data (variant IDs and sizes)
print("[INFO] Searching for variant|size combos...")
variants = page.find_all("id")
sizes = page.find_all("title")
variant_list = []
size_list = []
print("[INFO] Found", len(variants), "variant tags and", len(sizes),
      "size tags. Parsing data...")

# Exporting variant ID and size data to lists
count = 0
for val in variants:
    try:
        variant_list += [str(val.string)]
        size_list += [str(sizes[count].string)]
        count += 1
    except:
        print("[INFO] Parsed all variant|size combos.")
        break

# Displaying all variant|size combos
print("[INFO] Displaying all found variant|size combos...")
count = 0
for val in variant_list:
    try:
        print("\t", size_list[count], "|", val)
        count += 1
    except:
        print("[INFO] All variant and sizing data retrieved.")
        break

# Finding variant ID for the selected size to add to cart
user_size = input("[INPUT] What size are you looking for?: ")
count = 0
cart_variant = ""
for val in size_list:
    if(val == user_size):
        print("[INFO] Variant ID: " + variant_list[count])
        cart_variant = variant_list[count]
    count += 1

webbrowser.open(add_to_cart(cart_link, cart_variant))
