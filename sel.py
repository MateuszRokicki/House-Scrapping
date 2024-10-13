from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
import random

ua = UserAgent()
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
]

# Configure Chrome options
options = Options()
# options.add_argument("--headless")  # Run headless for no GUI
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"user-agent={random.choice(user_agents)}")

# Set up the Chrome WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the URL
url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/opolskie/nyski/lambinowice/lambinowice?distanceRadius={}&viewType=listing&page="
distance = 25
driver.get(url.format(distance))

# Wait for the page to load
time.sleep(2)

def number_of_pages():
    try:
        page_list = driver.find_elements(By.CLASS_NAME, 'css-43nhzf')
        return(max([int(pg.text) for pg in page_list]))
    except Exception as e:
        print(e)
        return 1

max_page = number_of_pages()

# Find listings
# listings = driver.find_elements(By.CLASS_NAME, 'css-136g1q2')
listings = driver.find_elements(By.CLASS_NAME, 'css-13gthep')#'css-16vl3c1')

# Extract data
# houses = []
for listing in listings[:1]:
    print(listing.get_attribute('href'))
    listing.click()
    # house_info = listing.text.split('\n')
    # print(house_info)
    # title = listing.find_element(By.CSS_SELECTOR, 'h3.css-1rhznz4').text.strip()
#     price = listing.find_element(By.CSS_SELECTOR, 'p.css-lk61n3').text.strip()
#     location = listing.find_element(By.CSS_SELECTOR, 'p.css-wqmnxv').text.strip()
    
#     houses.append({
#         'Title': title,
#         'Price': price,
#         'Location': location
#     })

time.sleep(20)
# Close the driver
driver.quit()

# Print the extracted data
# for house in houses:
#     print(house)