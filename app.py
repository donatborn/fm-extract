from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os, time

app = Flask(__name__)

def extract_from_link(link):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.binary_location = "./chrome/chrome-linux64/chrome"
    service = Service(executable_path="./chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(link)
    time.sleep(2)

    result = {
        "contact": "",
        "name": "",
        "link": link,
        "email_title": ""
    }

    def get_text(xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text.strip()
        except:
            return ""

    contact_person = get_text("//*[contains(text(), 'Contact person:') or contains(text(), 'Ansprechpartner:')]/following-sibling::*")
    from_company = get_text("//*[contains(text(), 'From') or contains(text(), 'Von')]/following-sibling::*")
    title = get_text("//h1")
    project_id = get_text("//*[contains(text(), 'Project ID:') or contains(text(), 'Projekt-ID:')]/following-sibling::*")

    if contact_person:
        result["name"] = contact_person
        result["contact"] = f"{contact_person} ({from_company})" if from_company else contact_person
        result["email_title"] = f'Proposal for "{title or "Unknown Title"}" Position (Project ID: {project_id or "N/A"})'

    driver.quit()
    return result

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    links = data.get("links", [])
    results = [extract_from_link(link) for link in links]
    return jsonify(results)

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
