from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
import random
import pandas as pd

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
time.sleep(1)

def number_of_pages():
    try:
        page_list = driver.find_elements(By.CLASS_NAME, 'css-43nhzf')
        return(max([int(pg.text) for pg in page_list]))
    except Exception as e:
        print(e)
        return 1

max_page = number_of_pages()
print(f'Number of pages {max_page}')

columns = ['Title', 'Price', 'PpSM', 'Area', 'Street', 'City', 'Commune', 'District', 'Voivodeship', 'Rooms', 'Heating', 'Floor', 'Rent', 'Condition', 'Market', 'Form of Ownership',
           'Availability', 'Seller type', 'Additional Information', 
           'Year', 'Elevator', 'Type of Development', 'Material', 'Windows', 'Energy Certificate', 'Safety', #Building and materials
           'Security', 'Media', #Equipment
           'Description']
df = pd.DataFrame()


counter1 = 1
for page in range(1, max_page):
    print(f'Page Number {page}')
    listings = driver.find_elements(By.CSS_SELECTOR, 'a[data-cy="listing-item-link"]')
    
    # Loop through each listing and click
    counter2 = 1
    for listing in listings:
        # Open the link in a new tab
        listing_link = listing.get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", listing_link)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Wait for the new page to load
        time.sleep(0.1)  # Adjust delay as necessary
        title = driver.find_element(By.CLASS_NAME , 'css-9pzx6y').text
        size = driver.find_element(By.CLASS_NAME , 'css-1ftqasz').text
        print(title)
        # Close the tab and return to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(f"Clicked and opened listing {counter1}, {counter2}")
        counter1 += 1
        counter2 += 1
    
    driver.get(url.format(distance) + f'{page+1}')
    time.sleep(10)

time.sleep(1)
# Close the driver
driver.quit()

# Print the extracted data
# for house in houses:
#     print(house)