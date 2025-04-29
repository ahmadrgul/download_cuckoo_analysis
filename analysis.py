import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def resource_path(relative_path):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), relative_path)

highest_analysis_number = int(input("Latest Analysis Number: "))
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

for n in range(highest_analysis_number, highest_analysis_number - number_of_analysis, -1):
    driver.get(f'https://sandbox.pikker.ee/analysis/{n}/export/')
    try:
        button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit" and contains(@class, "btn") and contains(@class, "btn-primary")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(@class, "btn") and contains(@class, "btn-primary")]')))
        button.click()
    except:
        pass
    time.sleep(10)

driver.quit()
