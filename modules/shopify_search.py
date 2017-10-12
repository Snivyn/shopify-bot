# shopify search
# developed by @snivynGOD

import requests
from bs4 import BeautifulSoup as bs


def shopify_download(sitemap):
    '''
    (str) -> (list)
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


print("------------------------------------------------------------------")
print("shopify search v1.1")
print("developed by @snivynGOD\n")
print("Assigns all product names and links to list variables given a")
print("Shopify URL.")
print("------------------------------------------------------------------\n")

# Global variables
my_products = []
my_links = []
my_results = []

# Gathering data from user
site = input("Load site: ")
url = "https://" + site + "/sitemap_products_1.xml"
keywords = input("Enter keywords: ").lower().split()

# Downloading all products from site
shopify_download(url)
print("[INFO] Found " + (str)(len(my_products)) + " products.")

# Searching for products with keywords
shopify_search()
print("[INFO] All tasks complete.")
