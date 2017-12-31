'''
sharanga shopify bot v1.1
a shopify bot (WIP)
developed by @snivynGOD

TO-DO
- check if payment was successful or failed
- MAYBE get auth token? doesn't appear to be needed though
- MAYBE get captcha? not sure if needed (create captcha solving module if so)
- add module for sites like KITH and DSMNY which use a different link for
products (https://kith.com/collections/all/products.atom)
- rewrite in C# with a GUI and multi-threading to support multiple tasks at once (coming soon)
- PEP8 compliant

EFFICIENCY TO-DO
not insanely effective but it'll help

- preload payment tokens with button click by user (i.e user can click a button
to fetch payment token prior to the drop so resources aren't wasted during tasks
trying to get the token) or get payment token asynchronously
- preload gateways by specifying a sitelist, but also leaving the option for
a user inputted shopify site to ensure as many sites are supported as possible
'''

from bs4 import BeautifulSoup as soup
import requests
import time
import json
import urllib3
import codecs
import random


''' ------------------------------ SETTINGS ------------------------------ '''
# Global settings
base_url = "https://www.deadstock.ca"  # Don't add a / at the end

# Search settings
keywords = ["adidas", "cs2"]  # Seperate keywords with a comma
size = "11"

# If a size is sold out, a random size will be chosen instead, as a backup plan
random_size = True

# To avoid a Shopify soft-ban, a delay of 7.5 seconds is recommended if
# starting a task much earlier than release time (minutes before release)
# Otherwise, a 1 second or less delay will be ideal
search_delay = 1

# Checkout settings
email = "email@domain.com"
fname = "Bill"
lname = "Nye"
addy1 = "123 Jolly St"
addy2 = ""  # Can be left blank
city = "Toronto"
province = "Ontario"
country = "Canada"
postal_code = "M1G1E4"
phone = "4169671111"
card_number = "4510000000000000"  # No spaces
cardholder = "FirstName LastName"
exp_m = "12"  # 2 digits
exp_y = "2017"  # 4 digits
cvv = "666"  # 3 digits

''' ------------------------------- MODULES ------------------------------- '''


def get_products(session):
    '''
    Gets all the products from a Shopify site.
    '''
    # Download the products
    link = base_url + "/products.json"
    r = session.get(link, verify=False)

    # Load the product data
    products_json = json.loads(r.text)
    products = products_json["products"]

    # Return the products
    return products


def keyword_search(session, products, keywords):
    '''
    Searches through given products from a Shopify site to find the a product
    containing all the defined keywords.
    '''
    # Go through each product
    for product in products:
        # Set a counter to check if all the keywords are found
        keys = 0
        # Go through each keyword
        for keyword in keywords:
            # If the keyword exists in the title
            if(keyword.upper() in product["title"].upper()):
                # Increment the counter
                keys += 1
            # If all the keywords were found
            if(keys == len(keywords)):
                # Return the product
                return product


def find_size(session, product, size):
    '''
    Find the specified size of a product from a Shopify site.
    '''
    # Go through each variant for the product
    for variant in product["variants"]:
        # Check if the size is found
        # Use 'in' instead of '==' in case the site lists sizes as 11 US
        if(size in variant["title"]):
            variant = str(variant["id"])

            # Return the variant for the size
            return variant

    # If the size isn't found but random size is enabled
    if(random_size):
        # Initialize a list of variants
        variants = []

        # Add all the variants to the list
        for variant in product["variants"]:
            variants.append(variant["id"])

        # Randomly select a variant
        variant = str(random.choice(variants))

        # Return the result
        return variant


def generate_cart_link(session, variant):
    '''
    Generate the add to cart link for a Shopify site given a variant ID.
    '''
    # Create the link to add the product to cart
    link = base_url + "/cart/" + variant + ":1"

    # Return the link
    return link


def get_payment_token(card_number, cardholder, expiry_month, expiry_year, cvv):
    '''
    Given credit card details, the payment token for a Shopify checkout is
    returned.
    '''
    # POST information to get the payment token
    link = "https://elb.deposit.shopifycs.com/sessions"

    payload = {
        "credit_card": {
            "number": card_number,
            "name": cardholder,
            "month": expiry_month,
            "year": expiry_year,
            "verification_value": cvv
        }
    }

    r = requests.post(link, json=payload, verify=False)

    # Extract the payment token
    payment_token = json.loads(r.text)["id"]

    # Return the payment token
    return payment_token


def get_shipping(postal_code, country, province, cookie_jar):
    '''
    Given address details and the cookies of a Shopify checkout session, a shipping option is returned
    '''
    # Get the shipping rate info from the Shopify site
    link = base_url + "//cart/shipping_rates.json?shipping_address[zip]=" + postal_code + "&shipping_address[country]=" + country + "&shipping_address[province]=" + province
    r = session.get(link, cookies=cookie_jar, verify=False)

    # Load the shipping options
    shipping_options = json.loads(r.text)

    # Select the first shipping option
    ship_opt = shipping_options["shipping_rates"][0]["name"].replace(' ', "%20")
    ship_prc = shipping_options["shipping_rates"][0]["price"]

    # Generate the shipping token to submit with checkout
    shipping_option = "shopify-" + ship_opt + "-" + ship_prc

    # Return the shipping option
    return shipping_option


def add_to_cart(session, variant):
    '''
    Given a session and variant ID, the product is added to cart and the
    response is returned.
    '''
    # Add the product to cart
    link = base_url + "/cart/add.js?quantity=1&id=" + variant
    response = session.get(link, verify=False)

    # Return the response
    return response


def submit_customer_info(session, cookie_jar):
    '''
    Given a session and cookies for a Shopify checkout, the customer's info
    is submitted.
    '''
    # Submit the customer info
    payload = {
        "utf8": u"\u2713",
        "_method": "patch",
        "authenticity_token": "",
        "previous_step": "contact_information",
        "step": "shipping_method",
        "checkout[email]": email,
        "checkout[buyer_accepts_marketing]": "0",
        "checkout[shipping_address][first_name]": fname,
        "checkout[shipping_address][last_name]": lname,
        "checkout[shipping_address][company]": "",
        "checkout[shipping_address][address1]": addy1,
        "checkout[shipping_address][address2]": addy2,
        "checkout[shipping_address][city]": city,
        "checkout[shipping_address][country]": country,
        "checkout[shipping_address][province]": province,
        "checkout[shipping_address][zip]": postal_code,
        "checkout[shipping_address][phone]": phone,
        "checkout[remember_me]": "0",
        "checkout[client_details][browser_width]": "1710",
        "checkout[client_details][browser_height]": "1289",
        "checkout[client_details][javascript_enabled]": "1",
        "button": ""
    }

    link = base_url + "//checkout.json"
    response = session.get(link, cookies=cookie_jar, verify=False)

    # Get the checkout URL
    link = response.url
    checkout_link = link

    # POST the data to the checkout URL
    response = session.post(link, cookies=cookie_jar, data=payload, verify=False)

    # Return the response and the checkout link
    return (response, checkout_link)

''' ------------------------------- CODE ------------------------------- '''

# Initialize
session = requests.session()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
product = None

# Loop until a product containing all the keywords is found
while(product == None):
    # Grab all the products on the site
    products = get_products(session)
    # Grab the product defined by keywords
    product = keyword_search(session, products, keywords)
    if(product == None):
        time.sleep(search_delay)

# Get the variant ID for the size
variant = find_size(session, product, size)

# Get the cart link
cart_link = generate_cart_link(session, variant)

# Add the product to cart
r = add_to_cart(session, variant)

# Store the cookies
cj = r.cookies

# Get the payment token
p = get_payment_token(card_number, cardholder, exp_m, exp_y, cvv)

# Submit customer info and get the checkout url
(r, checkout_link) = submit_customer_info(session, cj)

# Get the shipping info
ship = get_shipping(postal_code, country, province, cj)

# Get the payment gateway ID
link = checkout_link + "?step=payment_method"
r = session.get(link, cookies=cj, verify=False)

bs = soup(r.text, "html.parser")
div = bs.find("div", {"class": "radio__input"})
print(div)

gateway = ""
values = str(div.input).split('"')
for value in values:
    if value.isnumeric():
        gateway = value
        break

# Submit the payment
link = checkout_link
payload = {
    "utf8": u"\u2713",
    "_method": "patch",
    "authenticity_token": "",
    "previous_step": "payment_method",
    "step": "",
    "s": p,
    "checkout[payment_gateway]": gateway,
    "checkout[credit_card][vault]": "false",
    "checkout[different_billing_address]": "true",
    "checkout[billing_address][first_name]": fname,
    "checkout[billing_address][last_name]": lname,
    "checkout[billing_address][address1]": addy1,
    "checkout[billing_address][address2]": addy2,
    "checkout[billing_address][city]": city,
    "checkout[billing_address][country]": country,
    "checkout[billing_address][province]": province,
    "checkout[billing_address][zip]": postal_code,
    "checkout[billing_address][phone]": phone,
    "checkout[shipping_rate][id]": ship,
    "complete": "1",
    "checkout[client_details][browser_width]": str(random.randint(1000, 2000)),
    "checkout[client_details][browser_height]": str(random.randint(1000, 2000)),
    "checkout[client_details][javascript_enabled]": "1",
    "g-recaptcha-repsonse": "",
    "button": ""
    }

r = session.post(link, cookies=cj, data=payload, verify=False)
