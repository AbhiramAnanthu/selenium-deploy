from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, jsonify, request

app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--remote-debugging-port=9222')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

@app.route('/', methods=['POST'])
def process_request():
    try:
        user_input = request.json['user_input']
        result = scraper(user_input)
        
        if result is not None:
            response = {"result": result}
        else:
            response = {"error": "Failed to scrape the webpage"}
            
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def scraper(url):
    try:
        driver.get(url)
        header = driver.find_element(By.TAG_NAME, "h1").text
        return header
    except Exception as e:
        return None

@app.route('/shutdown', methods=['POST'])
def shutdown():
    driver.quit()
    return 'Driver shutdown successfully'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
