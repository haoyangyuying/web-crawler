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

    app.run(host='0.0.0.0', port=port, debug=True)
    # app.run(debug=True)