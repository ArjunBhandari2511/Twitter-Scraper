from flask import Flask, render_template, jsonify
import threading
import time
import requests
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/stir")
db = client['twitter_trends']
trends_collection = db['trends']

# Proxy and Selenium Setup
PROXY = "http://sid:@HVNSking.123@us-ca.proxymesh.com:31280"
firefox_options = Options()
firefox_options.add_argument(f"--proxy-server={PROXY}")
firefox_options.add_argument("--headless")
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")

# Global variable to store trending topics
background_result = {}

# Function to get the public IP used by the proxy
def get_public_ip_via_proxy(proxy_url):
    try:
        response = requests.get("https://httpbin.org/ip", proxies={"http": proxy_url, "https": proxy_url})
        if response.status_code == 200:
            return response.json().get("origin", "Unknown IP")
    except Exception as e:
        print(f"Error fetching public IP: {e}")
        return "Error"

# Function to get trending topics
def get_trending_topics():
    global background_result
    driver = None

    try:
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
        driver.get("https://twitter.com/login")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text"))).send_keys("SarcArjunB", Keys.RETURN)
        time.sleep(3)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("Sarathi@2511", Keys.RETURN)
        time.sleep(5)

        driver.get("https://x.com/explore/tabs/for-you")
        time.sleep(5)

        target_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.r-18u37iz"))
        )
        
        trending_topics = [f"Trending {i + 1}: {element.text}" for i, element in enumerate(target_elements[:5])]
        
        public_ip = get_public_ip_via_proxy(PROXY)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        trends_collection.insert_one({
            "trends": trending_topics,
            "timestamp": time.time(),
            "public_ip": public_ip,
            "completed_at": timestamp
        })

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if driver:
            driver.quit()

    background_result["trending"] = trending_topics
    background_result["timestamp"] = timestamp
    background_result["public_ip"] = public_ip
    background_result["completed_at"] = timestamp 

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_trending', methods=['GET'])
def get_trending():
    threading.Thread(target=get_trending_topics, daemon=True).start()
    return jsonify({'message': 'Fetching trending topics, please wait...'})

@app.route('/get_trending_result', methods=['GET'])
def get_trending_result():
    if 'trending' in background_result:
        response_data = {
            'trending': background_result['trending'],
            'timestamp': background_result['timestamp'],
            'public_ip': background_result['public_ip'],
            'completed_at': background_result['completed_at']
        }
        return json.dumps(response_data, indent=2), 200, {'Content-Type': 'application/json'}
    return jsonify({'message': 'Trending topics are still being fetched...'})

@app.route('/get_all_trends', methods=['GET'])
def get_all_trends():
    trends = trends_collection.find().sort("timestamp", -1)
    trends_list = [{
        "trends": trend["trends"],
        "timestamp": trend["timestamp"],
        "public_ip": trend["public_ip"]
    } for trend in trends]
    return jsonify(trends_list)

@app.route('/get_last_execution_time', methods=['GET'])
def get_last_execution_time():
    if 'timestamp' in background_result:
        return jsonify({'last_execution_time': background_result['timestamp']})
    return jsonify({'message': 'The script has not yet completed.'})

@app.route('/get_public_ip', methods=['GET'])
def get_public_ip():
    latest_trend = trends_collection.find_one(sort=[("timestamp", -1)])
    if latest_trend:
        return jsonify({'public_ip': latest_trend['public_ip']})
    return jsonify({'message': 'No public IP available yet'})

if __name__ == '__main__':
    app.run(debug=True)
