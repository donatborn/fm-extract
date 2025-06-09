from flask import Flask, request, jsonify
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def extract_from_link(link):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
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
    app.run(host="0.0.0.0", port=5000)
