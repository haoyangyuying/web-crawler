from flask import Flask, request, send_from_directory
import requests
import re
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize an empty list to store the unique image URLs
    unique_urls = []

    if request.method == 'POST':
        # Get the ASIN entered by the user in the form
        asin = request.form['asin']

        # Construct the URL for the entered ASIN
        product_url = f"https://www.amazon.com.au/dp/{asin}"

        # Load the product page and extract the HTML source code as a string
        response = requests.get(product_url)
        page_source = response.text

        # Use regex to find all image URLs that match the pattern "https://.*?SL1500_\.jpg"
        image_urls = re.findall(r"https://.*?SL1500_\.jpg", page_source)

        # Loop through each URL and add to the list if it is not already present
        for url in image_urls:
            unique_url = url[url.rfind('"')+1:]
            if unique_url not in unique_urls:
                unique_urls.append(unique_url)

    # Generate HTML with embedded images using the unique image URLs
    html = """
    <form method="post">
        <label for="asin">Enter ASIN:</label>
        <input type="text" id="asin" name="asin">
        <button type="submit">Scrape</button>
    </form>

    <div class="image-grid">
    """

    for i, url in enumerate(unique_urls):
        # Add an anchor tag around the image with a link to the original size
        html += f'<a href="{url}"><img src="{url}" alt="product-image"></a>'

    html += '</div>'

    # Add CSS styles to format the image grid and clickable images
    html += """
    <style>
    .image-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }
    .image-grid img {
        max-width: 200px;
        margin: 10px;
        cursor: pointer;
        transition: opacity 0.2s ease-in-out;
    }
    .image-grid img:hover {
        opacity: 0.7;
    }
    </style>
    """

    # Return the HTML with embedded images and input form
    return html

# Serve static files from the 'static' directory
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Use environment variables to get the port and debug mode
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', True)

    app.run(host='0.0.0.0', port=port, debug=debug)
