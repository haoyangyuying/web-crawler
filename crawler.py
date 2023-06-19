import requests
import re

# Create a list of ASINs for the products to be scraped
asins = ['B0BQY28ZJK', 'B092W8MTSV']

# Loop through each ASIN and scrape its product page
for asin in asins:

    # Construct the URL for the current ASIN
    product_url = f"https://www.amazon.com.au/dp/{asin}"
    
    # Load the product page and extract the HTML source code as a string
    response = requests.get(product_url)
    page_source = response.text

    # Use regex to find all image URLs that match the pattern "https://.*?SL1500_\.jpg"
    image_urls = re.findall(r"https://.*?SL1500_\.jpg", page_source)

    # Use a set to keep track of unique image URLs
    unique_urls = set()

    # Loop through each URL and add to the set if it is not already present
    for url in image_urls:
        unique_url = url[url.rfind('"')+1:]
        if unique_url not in unique_urls:
            unique_urls.add(unique_url)
            print(unique_url)
