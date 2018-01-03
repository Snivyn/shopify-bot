# sharanga shopify bot v1.1

## About
This project is a work in progress. Its main goal is to automate the checkout process on any Shopify powered site given a few keywords. 

### Usage
Edit the fields under "USER SETTINGS" in the .py file. Keywords should be defined as a list, with each word seperated by a comma and placed within quotation marks. Some formatting is required for certain fields, as stated within the .py file.

### What can this project do?
* Find all products on a given Shopify site
* Search through products based on keywords
* Find sizes of products
* Add products based on sizes to cart
* Checkout products with given customer info
* Monitor sites until a product is found in real-time

### What's left to do?
* Proxy support
* Checkout process
* Log all events for debugging purposes
* Profiles for user info (billing and shipping)
* Manual captcha completion and 2Captcha support (if captchas are required)
* Get authentication token (doesn't appear to be required and is thus being left out for now)
* Add support for sites like KITH and DSMNY which use a different link for
products (i.e https://kith.com/collections/all/products.atom)
* PEP8 compliant

### What other features are planned for a final version?
* Rewrite in C# with a GUI (in progress)
* Support for queue-based releases
* Multithreading to support multiple tasks at once
* Preload payment token with a button click by the user (i.e user can click a button to fetch payment token prior to the drop so resources aren't wasted during tasks trying to get the token, ultimately saving time) or get payment token asynchronously
* Preload gateways by specifying a sitelist to save resources during runtime , saving time during the checkout process, while also leaving the option for the user to input a custom Shopify-enabled site to ensure as many sites are supported as possible

## Credits
 **Niveen Jegatheeswaran** - [@snivynGOD](https://twitter.com/snivynGOD)

## Disclaimer
Not affiliated with Shopify or any sites in any way. This is a personal project. Please do NOT sell this script. Share it with others and help build upon it to make it more efficient. 
It may not be stable. Please let me know of any problems you come across.

If you have any suggestions, or want to help make this better, let me know!

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details. 
