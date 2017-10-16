# sharanga - a shopify bot
# developed by @snivynGOD

import requests
from bs4 import BeautifulSoup as bs
import webbrowser


def shopify_download(sitemap):
    '''
    (str)
    Assigns all products on a Shopify site to lists my_products and my_links.
    >>> shopify_download("https://kith.com/sitemap_products_1.xml")
    '''

    # Downloading sitemap
    try:
        session = requests.session()
        raw_data = session.get(sitemap)
        soup = bs(raw_data.content, 'html.parser')
    except:
        print("[ERROR] Connection error. Double check the site you "
              "provided and your internet connection.")
        user_input()

    count = 0
    links_temp = []
    products_temp = []

    for product in soup.find_all("url"):
        links_temp = (str)(product.find("loc").string).lower()
        try:
            image_title = product.find("image:image")
            title = image_title.find("image:title")
            products_temp = (str)(title.string).lower()

            # Saving product|link combo
            my_products.insert(count, products_temp)
            my_links.insert(count, links_temp)
            count += 1
        except:
            continue


def shopify_search():
    '''
    Outputs products that match the previously entered keywords.
    >>> shopify_search()
    '''
    keyword_count = len(keywords)
    keyword_matches = 0
    count = 0
    result_count = 0

    for product in my_products:
        keyword_matches = 0
        for word in keywords:
            if product.find(word) != -1:
                keyword_matches += 1
                if keyword_matches == keyword_count:
                    my_results.insert(result_count, count)
                    print(result_count, "|", product, "|", my_links[count])
                    result_count += 1
                count += 1
    print("[INFO] Found " + (str)(result_count) + " matches.")


def add_to_cart(site, variant):
    '''
    (str, str) -> str
    Given a site and a variant ID, a link with the product added to the cart
    will be returned.
    >>>add_to_cart(https://shop.antisocialsocialclub.com/, 1488552847,1)
    https://shop.antisocialsocialclub.com/cart/1488552847:1/
    '''
    URL = site + variant + ":1"
    return URL

print("------------------------------------------------------------------")
print("shopify auto cart v1.0")
print("developed by @snivynGOD\n")
print("Searches all products on a Shopify powered site for specific"
      "products and proceeds to add the item to the user's cart and"
      "displays the cart in a web browser. Not completely automated (yet).")
print("------------------------------------------------------------------\n")


# Global variables
my_products = []
my_links = []
my_results = []

# Gathering data from user
site = input("Load site: ")
url = "https://" + site + "/sitemap_products_1.xml"
keywords = input("Enter keywords: ").lower().split()
cart_link = "https://" + site + "/cart/"

# Downloading all products from site
shopify_download(url)
print("[INFO] Found " + (str)(len(my_products)) + " products.")

# Searching for products with keywords
shopify_search()
print("[INFO] Found all products with selected keywords.")

# Choosing which product to add to cart
atc_product = input("[INPUT] Which product do you want to add to cart?: ")
atc_link = my_links[my_results[(int)(atc_product)]]

# Specifying a site and collecting raw page data
print("[INFO] Collecting raw data...")
res = requests.get(atc_link + ".xml")
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
