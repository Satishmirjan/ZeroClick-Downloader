from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Start browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.udemy.com/join/passwordless-auth/?locale=en_US&next=https%3A%2F%2Fwww.udemy.com%2F%3Futm_source%3Dadwords-brand%26utm_medium%3Dudemyads%26utm_campaign%3DBrand-Udemy_la.EN_cc.India_dev.%26campaigntype%3DSearch%26portfolio%3DBrandDirect%26language%3DEN%26product%3DCourse%26test%3D%26audience%3DKeyword%26topic%3D%26priority%3D%26utm_content%3Ddeal4584%26utm_term%3D_._ag_133043842301_._ad_595460368494_._kw_udemy_._de_c_._dm__._pl__._ti_kwd-296956216253_._li_9303595_._pd__._%26matchtype%3Db%26gad_source%3D1%26gad_campaignid%3D17099057432%26gbraid%3D0AAAAADROdO3PFt8C2Iao91pE01ZfMAcq2%26gclid%3DCjwKCAiA_orJBhBNEiwABkdmjIIdTUORS_FnWJ_oWubL2IBtcDdFhuLjwxa8AAEUT9EqpjDUdkVGfRoC1tgQAvD_BwE&response_type=html&action=login&mode")

# Login
driver.find_element(By.ID, "username").send_keys("Satishnda3576@gmail.com")
driver.find_element(By.ID, "password").send_keys("10rupeeskipepsifawzanbhaisexy")
driver.find_element(By.ID, "login-btn").click()
sleep(3)

# Get all links
links = driver.find_elements(By.TAG_NAME, "a")
htac_links = [link.get_attribute("href") for link in links if "htac" in link.text.lower()]

# Visit each link & download
for url in htac_links:
    driver.get(url)
    sleep(2)
    
    download_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Download')]")
    download_btn.click()
    
    sleep(3)

driver.quit()
