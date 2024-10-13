import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
ua = UserAgent()

headers = {'User-Agent':str(ua.chrome)}

def main():

# Base URL of the listing
    base_url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/opolskie/nyski/lambinowice/lambinowice?distanceRadius=35&viewType=listing&page="

    # Function to extract listing data from a single page
    def get_listings(page):
        url = base_url + str(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract data for each listing
        listings = []
        for listing in soup.find_all('article', class_='css-1o565rw'):
            title = listing.find('h3', class_='css-1rhznz4').text.strip()
            price = listing.find('p', class_='css-lk61n3').text.strip()
            location = listing.find('p', class_='css-wqmnxv').text.strip()
            
            listings.append({
                'Title': title,
                'Price': price,
                'Location': location
            })
        
        return listings

    # Iterate through pages and collect data
    def get_total_pages():
        response = requests.get(base_url + "1")
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # Locate the pagination section using 'data-cy' attribute
        # pagination = soup.find('ul', attrs={'data-cy': 'frontend.search.base-pagination.nexus-pagination'})
        pagination = soup.find('ul', class_ = 'e1h66krm4 css-iiviho')
        # print(pagination)
        if pagination:
            # Get all page numbers (they are <li> elements inside the <ul>)
            page_numbers = pagination.find_all('li')
            if page_numbers:
                # The last valid number will be the total pages, ignore '...' and 'next' buttons
                total_pages = int(page_numbers[-2].text.strip())
                return total_pages
        
        return 1  # Fallback to 1 if pagination not found

    # Scrape all listings
    def scrape_all_listings():
        response = requests.get(base_url + "1")
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify())

        
        total_pages = get_total_pages()
        print(f"Total pages: {total_pages}")
        
        all_listings = []
        for page in range(1, total_pages + 1):
            all_listings.extend(get_listings(page))
            print(f"Scraped page {page}")
        
        return all_listings

    # Scrape all pages
    listings = scrape_all_listings()


    # Convert to pandas DataFrame and export to CSV
    df = pd.DataFrame(listings)
    print(df)
    # df.to_csv('house_listings.csv', index=False)
    # print("Data saved to house_listings.csv")

    
if  __name__ == "__main__":
        main()