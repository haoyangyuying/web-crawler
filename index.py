from flask import Flask, request, redirect
import requests
import re
import os

app = Flask(__name__)

# Function to scrape images
def scrape_images(asin):
    # Initialize an empty list to store the unique image URLs
    unique_urls = []

    # Construct the URL for the entered ASIN
    product_url = f"https://www.amazon.com.au/dp/{asin}"

    # Load the product page and extract the HTML source code as a string
    response = requests.get(product_url)
    page_source = response.text

    # Use regex to find all image URLs that match the pattern "https://.*?SL1500_\.jpg"
    image_urls = re.findall(r"https://.*?(?:1500_|1200_|1000_)\.jpg", page_source)[:30]

    # Loop through each URL and add to the list if it is not already present
    for url in image_urls:
        unique_url = url[url.rfind('"')+1:]
        if unique_url not in unique_urls:
            unique_urls.append(unique_url)

    # Generate HTML with embedded images using the unique image URLs
    html = """
    <div class="container">

        <form method="post">
            <label for="asin">Enter ASIN:</label>
            <input type="text" id="asin" name="asin" size="30" placeholder="Enter an ASIN...">
            <button type="submit">Scrape</button>
        </form>

        <div class="example-asins">
            <p>Example ASINs: B0BFR3K492, B09V25VFNK, B0BQY4VSSD</p>
        </div>

        <div class="image-grid">
    """

    for i, url in enumerate(unique_urls):
        # Add an anchor tag around the image with a link to the original size
        html += f'<a href="{url}"><img src="{url}" alt="product-image"></a>'

    html += '</div></div>'

    # Add CSS styles to format the container, input form, and clickable images
    html += """
    <style>
        .container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 15px;
            margin: 0 auto;
            max-width: 600px;
        }

        form {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }

        label {
            font-size: 16px;
            margin-right: 10px;
        }

        input[type="text"] {
            border: none;
            border-radius: 6px;
            padding: 10px;
            font-size: 16px;
            width: 60%;
        }

        button[type="submit"] {
            border: none;
            background-color: #ddd;
            color: black;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }

        button[type="submit"]:hover {
            background-color: #ccc;
        }

        .example-asins {
            margin-bottom: 10px;
        }

        .image-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            margin: 0 -5px;
        }

        .image-grid img {
            max-width: 100%;
            height: auto;
            margin: 10px 5px;
            cursor: pointer;
            transition: opacity 0.2s ease-in-out;
        }

        .image-grid img:hover {
            opacity: 0.7;
        }

        /* Media queries for smaller screens */
        @media only screen and (max-width: 768px) {
            .container {
                max-width: 100%;
                padding: 10px;
            }

            input[type="text"] {
                width: 100%;
            }

            .image-grid img {
                max-width: 45%;
                margin: 10px 5% 30px;
            }
        }

        /* Media queries for even smaller screens */
        @media only screen and (max-width: 480px) {
            .image-grid img {
                max-width: 90%;
                margin: 10px 5%;
            }
        }

    </style>
    """

    return html

# Function to scrape reviews
def scrape_reviews(asin):
    # Construct the URL for the entered ASIN
    product_url = f"https://www.amazon.com.au/product-reviews/{asin}"

    # Load the product page and extract the HTML source code as a string
    response = requests.get(product_url)
    page_source = response.text

    # Find all URLs of the form /gp/customer-reviews/{customer_review_id}/ASIN={asin}
    urls = re.findall(r'(/gp/customer-reviews/.*?.*?)("|\')', page_source)

    # Extract the first item from each tuple in the URLs list and add https://www.amazon.com.au/
    urls = ['https://www.amazon.com.au' + url[0] for url in urls]

    # Initialize an empty list to store the review text
    review_texts = []

    # Loop through each URL, load the page, extract the review text, and append it to the list
    for url in urls:
        # Load the review page and extract the HTML source code as a string
        response = requests.get(url)
        review_source = response.text

        # Use regex to find the review text that matches the pattern "<span data-hook="review-body" class="">.*?</span>"
        review_text = re.search(r'<span data-hook="review-body" class="">(.*?)</span>', review_source)

        # Check if review text exists before appending it to the list
        if review_text:
            review_text = review_text.group(1).strip()
            review_texts.append(review_text)

            # Print out the review text
            print(review_text)
    
    # Return the list of review texts
    return review_texts

@app.route('/images', methods=['GET', 'POST'])
def images():
    if request.method == 'POST':
    # Get the ASIN entered by the user in the form
        asin = request.form['asin']

            # Call the scrape_images function and pass the ASIN
        html = scrape_images(asin)

            # Return the HTML with embedded images and input form
        return html

        # If the request method is GET, just return the HTML with input form
    return """
        <div class="container">

            <form method="post">
                <label for="asin">Enter ASIN:</label>
                <input type="text" id="asin" name="asin" size="30" placeholder="Enter an ASIN...">
                <button type="submit">Scrape</button>
            </form>

            <div class="example-asins">
                <p>Example ASINs: B0BFR3K492, B09V25VFNK, B0BQY4VSSD</p>
            </div>

        </div>
        """
    
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
    # Get the ASIN entered by the user in the form
        asin = request.form['asin']
            # Call the scrape_reviews function and pass the ASIN
        html = scrape_reviews(asin)

        # Return the HTML with embedded reviews and input form
        return html

        # If the request method is GET, just return the HTML with input form
    return"""
        <div class="container">

            <form method="post">
                <label for="asin">Enter ASIN:</label>
                <input type="text" id="asin" name="asin" size="30" placeholder="Enter an ASIN...">
                <button type="submit">Scrape</button>
            </form>

        </div>
        """

@app.route('/')
def index():
    return redirect('/images')

app.run(host='0.0.0.0', port=5000, debug=True)
# app.run(debug=True)