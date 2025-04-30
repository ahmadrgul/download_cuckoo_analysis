import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def are_downloads_completed(download_dir):
    while True:
        if not any(filename.endswith('.crdownload') for filename in os.listdir(download_dir)):
            break
        time.sleep(1)

def resource_path(relative_path):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), relative_path)

analysis_number = int(input("Latest Analysis Number: "))
number_of_analysis = int(input("Number of Analysis to Download: "))

download_path = os.path.join(os.environ["USERPROFILE"], "Downloads", "analysis")
os.makedirs(download_path, exist_ok=True)

driver_path = resource_path("chromedriver.exe")

options = Options()
options.add_experimental_option("prefs", {
    'download.default_directory': download_path,
    'download.prompt_for_download': False,
})

driver = webdriver.Chrome(service=Service(driver_path), options=options)
wait = WebDriverWait(driver, 20)
number_of_downloads = 0

while number_of_downloads < number_of_analysis:
    url = f'https://sandbox.pikker.ee/analysis/{analysis_number}/export/'
    driver.get(url)
    
    if '404' not in driver.page_source:
        try:
            button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit" and contains(@class, "btn") and contains(@class, "btn-primary")]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(@class, "btn") and contains(@class, "btn-primary")]')))
            button.click()
        except:
            continue
        number_of_downloads += 1

    analysis_number -= 1

if are_downloads_completed(download_path):
    driver.quit()
