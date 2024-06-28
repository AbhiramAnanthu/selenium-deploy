from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, jsonify, request

app = Flask(__name__)
chrome_options=Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

def scraper(url):
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.get(url)
    header = driver.find_element(By.TAG_NAME, "h1").text
    return header


@app.route('/', methods=['POST'])
def process_request():
    try:
        # Get user input from POST data
        user_input = request.json['user_input']

        # Process user input to get final result
        result = scraper(user_input)

        if result is not None:
            # Prepare JSON response
            response = {"result": result}
        else:
            response = {"error": "Failed to scrape the webpage"}

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)