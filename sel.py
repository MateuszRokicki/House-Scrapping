from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
import random
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
print(url.format(distance))
driver.get(url.format(distance))

# Wait for the page to load
time.sleep(1)

def number_of_pages(driver:webdriver.Chrome):
    try:
        page_list = driver.find_elements(By.CLASS_NAME, 'css-43nhzf')
        return(max([int(pg.text) for pg in page_list]))
    except Exception as e:
        print(e)
        return 1

def split_address(full_address):
    address_list = [part.strip() for part in full_address.split(',')]
    voivodeship = address_list[-1]
    district = address_list[-2]
    commune = address_list[-3]
    city = address_list[-4]
    if len(address_list) == 5:
        street = address_list[0]
    else:
        street = ''
    return voivodeship, district, commune, city, street


max_page = number_of_pages(driver)
print(f'Number of pages {max_page}')

columns = ['Title', 'Price', 'PpSM', #Basic info
           'Street', 'City', 'Commune', 'District', 'Voivodeship', #Address
           'Area', 'Rooms', 'Heating', 'Floor', 'Rent', 'Condition', 'Market', 'Form of Ownership', 'Availability', 'Seller type', 'Additional Information', #Details
           'Year', 'Elevator', 'Type of Development', 'Material', 'Windows', 'Energy Certificate', 'Safety', #Building and materials
           'Security', 'Media', #Equipment
           'Description']
df = pd.DataFrame()


details_mapping = {
    'Ogrzewanie' : 'Heating',
    'Piętro' : 'Floor',
    'Czynsz' : 'Rent',
    'Stan wykończenia' : 'Condition',
    'Rynek' : 'Market',
    'Forma własności' : 'Form of Ownership',
    'Dostępne od' : 'Availability',
    'Typ ogłoszeniodawcy' : 'Seller type',
    'Informacje dodatkowe' : 'Additional information',
    'Winda' : 'Elevator',
    'Rodzaj zabudowy' : 'Type of development',
    'Windows' : 'Okna',
    'Bezpieczeństwo' : 'Safety',
    'Wyposażenie' : 'Equipment',
    'Zabezpieczenia' : 'Security',
}

internal_index = 1
for page in range(1, max_page):
    print(f'Page Number {page}')
    
    # Get all listings from page
    listings = driver.find_elements(By.CSS_SELECTOR, 'a[data-cy="listing-item-link"]')
    
    # Loop through each listing and click
    for listing in listings:
        print(internal_index)
        # Open the link in a new tab for listing
        listing_link = listing.get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", listing_link)
        driver.switch_to.window(driver.window_handles[-1])
        print(listing_link)
        # Wait for the new page to load
        time.sleep(0.1)  
        
        # Get listing details
        title = driver.find_element(By.CLASS_NAME , 'css-wqvm7k').text
        price = driver.find_element(By.CLASS_NAME , 'css-1o51x5a').text # 1ftqasz
        ppsm = driver.find_element(By.CLASS_NAME , 'css-z3xj2a').text
        address = driver.find_element(By.CLASS_NAME , 'css-1jjm9oe').text
        voivodeship, district, commune, city, street = split_address(address)
        
        area_rooms = driver.find_elements(By.CLASS_NAME , 'css-1ftqasz')
        area = area_rooms[0].text
        rooms = area_rooms[1].text
        
        # Scroll to an end of the page to load everything
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Open all hidden elements
        elements = driver.find_elements(By.CLASS_NAME, "css-1g1u77j")
        for element in elements:
            driver.execute_script("arguments[0].click();", element)
        
        
        details = driver.find_elements(By.CLASS_NAME , 'css-1airkmu')
        details = [detail.text for detail in details]
        
        # Add empty string if no value for key
        i = 0
        while i < len(details):
            if ":" in details[i] and (i + 1 == len(details) or ":" in details[i + 1]):
                details.insert(i + 1, ' ')
                i += 1  # Skip the inserted element to avoid infinite loop
            i += 1   
            
        # Remove unwanted characters
        details = [
            detail.replace(':', '').strip().split('\n') if '\n' in detail else detail.replace(':', '').strip()
            for detail in details]
        
        details = dict(zip(details[::2], details[1::2]))
        mapped_dict = {details_mapping[key]: value for key, value in details.items() if key in details_mapping}
        print(details)
        print(mapped_dict)
        time.sleep(2)
        
        print(title, price, ppsm)
        print(voivodeship, district, commune, city, street)
        # Close the tab and return to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        internal_index += 11
    
    driver.get(url.format(distance) + f'{page+1}')
    time.sleep(10)

time.sleep(1)
# Close the driver
driver.quit()

# Print the extracted data
# for house in houses:
#     print(house)