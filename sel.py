from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
import random
import pandas as pd
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import datetime

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
# url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?distanceRadius={}&viewType=listing&page="
distance = 15
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
    ### Figure out splitting adifferent addresses
    # os. Zacisze, Kopice, Grodków, brzeski, opolskie
    # ul. Zwycięska 3, Partynice, Krzyki, Wrocław, dolnośląskie
    # ul. Obozowa, Łambinowice, Łambinowice, nyski, opolskie
    address_list = [part.strip() for part in full_address.split(',')]
    voivodeship = address_list[-1]
    address = {'Voivodeship' : voivodeship}
    if len(address_list) == 5:
        street = address_list[0]
    else:
        street = ''
        
    if address_list[-2][-3:] in ('ski', 'cki'):
        district = address_list[-2]
        commune = address_list[-3]
        city = address_list[-4]
        address.update({'District' : district, 'Commune' : commune, 'City' : city, 'City District' : None, 'Subdistrict' : None})
    else:
        city = address_list[-2]
        city_district = address_list[-3]
        subdistrict = address_list[-4]
        address.update({'District' : None, 'Commune' : None, 'City' : city, 'City District' : city_district, 'Subdistrict' : subdistrict})
        
    address['Street'] = street
    return address

def split_and_map(elements, map_dict:dict):
    if not isinstance(elements, list):
        elements = [elements]
    elements_dict = {}
    for key, value in map_dict.items():
        if key in elements:
            elements_dict[value] = True
        else:
            elements_dict[value] = False
    # elements = {map_dict.get(el, el): el in map_dict for el in elements}
    return elements_dict

def transform_details(details):
    details = [detail.text for detail in details] 
    print(details)
    transformed_details = []
    # Add empty string if no value for key
    i = 0
    while i < len(details):
        if ":" in details[i] and (i + 1 == len(details) or ":" in details[i + 1]):
            details.insert(i + 1, ' ')
            i += 1  # Skip the inserted element to avoid infinite loop
        i += 1   
        
    # Remove unwanted characters
    for i, detail in enumerate(details):
        detail = detail.replace(':', '').replace(' zł', '').strip()
        if '\n' in detail:
            details[i] = detail.split('\n')
        else:
            if detail == '':
                details[i] = None
            else:
                details[i] = detail
    
    # for detail in details:
    #     if not isinstance(detail, list):
    #         if detail == '':
    #             detail = None   
    #     transformed_details.append(detail)
        
    transformed_details = dict(zip(details[::2], details[1::2]))
    not_found_keys = set()
    for key in transformed_details.keys():
        if key not in apartment_details_mapping.keys() or key not in equipment_mapping.keys() or key not in media_mapping.keys() or key not in additional_information_mapping.keys() or key not in security_mapping.keys():
            not_found_keys.add(key)
            
    if not_found_keys:
        with open(f'Not_Found_Keys_{datetime.datetime.now().strftime("%Y-%m-%d")}', 'w') as f:
            for key in not_found_keys:
                f.write(str(key) + '\n')
    
    return transformed_details
            

apartment_columns = ['ID', 'URL', 'Title', 'Price', 'PpSM', #Basic info
                    'Street', 'Subdistrict', 'City District', 'City', 'Commune', 'District', 'Voivodeship', #Address
                    'Area', 'Rooms', 'Two-story', 'Heating', 'Floor', 'Rent', 'Condition', 'Market', 'Form of Ownership', 'Availability', 'Seller Type', #Details
                    # 'Additional Information',
                    'Balcony', 'Basement', 'Air Conditioning', 'Utility Room', 'Garden', 'Garage/Parking Space', 'Terrace', 'Separate Kitchen', #Additional Information
                    'Year', 'Elevator', 'Type of Development', 'Building Material', 'Windows', 'Energy Certificate', 'Safety', #Building and materials
                    'Anti-burglary Blinds', 'Anti-burglary Doors/Windows', 'Intercom/Videophone', 'Alarm System', 'Gated Community', 'Monitoring/Security' #Security
                    'Furniture', 'Refigerator', 'TV', 'Washing Machine', 'Stove', 'Dishwasher', 'Oven', #Equipment
                    'Internet', 'Cable TV', 'Landline', #Media
                    'Description']

apartment_details_mapping = {
    'Ogrzewanie' : 'Heating',
    'Piętro' : 'Floor',
    'Czynsz' : 'Rent',
    'Stan wykończenia' : 'Condition',
    'Rynek' : 'Market',
    'Forma własności' : 'Form of Ownership',
    'Dostępne od' : 'Availability',
    'Typ ogłoszeniodawcy' : 'Seller Type',
    'Informacje dodatkowe' : 'Additional Information',
    'Rok budowy' : 'Year',
    'Winda' : 'Elevator',
    'Rodzaj zabudowy' : 'Type of Development',
    'Materiał budynku' : 'Building Material',
    'Okna' : 'Windows',
    'Certyfikat energetyczny' : 'Energy Certificate',
    'Bezpieczeństwo' : 'Safety',
    'Wyposażenie' : 'Equipment',
    'Zabezpieczenia' : 'Security'
}

equipment_mapping = {
    'meble' : 'Furniture',
    'Lodówka' : 'Refigerator',
    'Telewizor' : 'TV',
    'pralka' : 'Washing Machine',
    'kuchenka' : 'Stove',
    'zmywarka' : 'Dishwasher',
    'piekarnik' : 'Oven'
}

media_mapping = {
    'internet' : 'Internet',
    'telewizja kablowa' : 'Cable TV',
    'telefon' : 'Landline'
}

additional_information_mapping = {
    'balkon' : 'Balcony',
    'piwnica' : 'Basement',
    'klimatyzacja' : 'Air Conditioning',
    'pom. użytkowe' : 'Utility Room',
    'ogródek' : 'Garden',
    'garaż/miejsce parkingowe' : 'Garage/Parking Space',
    'taras' : 'Terrace',
    'oddzielna kuchnia' : 'Separate Kitchen'
}

security_mapping = {
    'rolety antywłamaniowe' : 'Anti-burglary Blinds',
    'drzwi / okna antywłamaniowe' : 'Anti-burglary Doors/Windows',
    'domofon / wideofon' : 'Intercom/Videophone',
    'monitoring / ochrona' : 'Monitoring/Security',
    'system alarmowy' : 'Alarm System',
    'teren zamknięty' : 'Gated Community'
}

df = pd.DataFrame(columns=apartment_columns).assign(Year=1900)

max_page = number_of_pages(driver)
print(f'Number of pages {max_page}')

internal_index = 1
for page in range(1, max_page+1):
    print(f'Page Number {page}')
    
    # Get all listings from page
    listings = driver.find_elements(By.CSS_SELECTOR, 'div[data-cy="search.listing.organic"] a[data-cy="listing-item-link"]')
    # print(listings)
    print(f'Listings {len(listings)}')
    
    # Loop through each listing and click
    for listing in listings:
        print(internal_index)
        # Open the link in a new tab for listing
        listing_link = listing.get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", listing_link)
        driver.switch_to.window(driver.window_handles[-1])
        print(listing_link)
        
        id = listing_link.split('-')[-1].replace('.','').replace('ID', '')
        if df['ID'].str.contains(id).any():
            break
        
        listing_info = {'ID' : id, 'URL' : listing_link}
        # Wait for the new page to load
        time.sleep(0.1)  
        
        # Get listing details
        title = driver.find_element(By.CLASS_NAME , 'css-4utb9r').text # wqvm7k
        price = driver.find_element(By.CLASS_NAME , 'css-1o51x5a').text # 1ftqasz
        if price == 'Zapytaj o cenę':
            price = None
        try:
            # print(price)
            price = float(price.replace('zł', '').replace(' ', ''))
        except Exception as e:
            print(e)
            
        try:
            ppsm = driver.find_element(By.CLASS_NAME , 'css-z3xj2a').text
        except NoSuchElementException:
            ppsm = None
        try:
            # print(ppsm)
            ppsm = float(ppsm.replace('zł/m²', '').replace(' ',''))
        except Exception as e:
            print(e)
        # print(ppsm)
            
        listing_info.update({'Title' : title, 'Price' : price, 'PpSM' : ppsm})
            
        address = driver.find_element(By.CLASS_NAME , 'css-1jjm9oe').text
        address_dict = split_address(address)
        listing_info.update(address_dict)
        
        area_rooms = [el.text for el in driver.find_elements(By.CLASS_NAME , 'css-1ftqasz')]
        for el in area_rooms:
            if 'm²' in el:
                listing_info.update({'Area' : el.replace('m²', '')})
            elif el.split(' ')[1][:3] == 'pok':
                listing_info.update({'Rooms' : el.split(' ')[0]})
            else:
                listing_info.update({'Two-story' : True})
        
        # Scroll to an end of the page to load everything
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Open all hidden elements
        elements = driver.find_elements(By.CLASS_NAME, "css-1g1u77j")
        for element in elements:
            driver.execute_script("arguments[0].click();", element)
        
        details = driver.find_elements(By.CLASS_NAME , 'css-1airkmu')
            
        details = transform_details(details)
        
        
        mapped_dict = {apartment_details_mapping[key] if key in apartment_details_mapping else key : value for key, value in details.items()} 
        try:
            mapped_dict['Elevator'] = True if str.lower(mapped_dict['Elevator']) == 'tak' else False
        except KeyError:
            print('Elevator not found')
            mapped_dict['Elevator'] = False

        ###TODO
        # split list of 'Additional Information' into columns and map to english
        additional_information_dict = mapped_dict.pop('Additional Information', [])
        additional_information_dict = split_and_map(additional_information_dict, additional_information_mapping)
        mapped_dict.update(additional_information_dict)
        
        # split list of Media into columns
        media_dict = mapped_dict.pop('Media', [])
        media_dict = split_and_map(media_dict, media_mapping)
        mapped_dict.update(media_dict)
        # print(media_dict)
        # print(mapped_dict)
        
        # split list of Equipment into columns
        # print('Equipment')
        equipment_dict = mapped_dict.pop('Equipment', [])
        equipment_dict = split_and_map(equipment_dict, equipment_mapping)
        mapped_dict.update(equipment_dict)
        # print(equipment_dict)
        
        # split list of Security into columns
        # print('Security')
        security_dict = mapped_dict.pop('Security', [])
        security_dict = split_and_map(security_dict, security_mapping)
        mapped_dict.update(security_dict)
        # print(security_dict)
                
        # print(mapped_dict)
        listing_info.update(mapped_dict)
        
        ###TODO
        # Get description
        desc = driver.find_element(By.CLASS_NAME, 'css-iba5ag').text.replace('\n', ' ').replace('\t', '') #cy1ltv
        listing_info.update({'Description' : desc})        
        # print(listing_info['Alarm System'])
        time.sleep(0.5)
        
        # Close the tab and return to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        internal_index += 1
        df.loc[len(df)] = listing_info
        
        # print(df)
    if page != max_page:
        # break
        driver.get(url.format(distance) + f'{page+1}')
        time.sleep(10)

# df.fillna('NULL', inplace=True)
print(df)
print(df['Alarm System'])
df.to_csv("test.csv", index=False, na_rep='NULL')
time.sleep(1)
# Close the driver
driver.quit()

# Print the extracted data
# for house in houses:
#     print(house)