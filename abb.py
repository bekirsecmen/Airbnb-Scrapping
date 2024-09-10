from scrapingbee import ScrapingBeeClient
from bs4 import BeautifulSoup
import json

client = ScrapingBeeClient(api_key='R42LZ0ZMK7PVREC7235KP3J372IZCC68OF1X2O9BF4U5LPEYCIW1HV01C1WKBNVI7NC4GAL9AJNIW56T')

print("starting ... ")
response = client.get("https://www.airbnb.com/s/Beyoglu--Istanbul/homes?checkin=2024-05-20&checkout=2024-05-27", 
                      params = { 
                        'country_code': 'tr',
                        'premium_proxy': 'True',
                        'wait_browser': 'load',
    }
)

soup = BeautifulSoup(response.content, "lxml")

results = []

listings = soup.find_all("div", class_="lxq01kf")

for listing in listings:
    # Extract the title of the listing
    title = listing.find("div", class_="t1jojoys").get_text(strip=True) if listing.find("div", class_="t1jojoys") else 'N/A'

    # Extracting the description
    description_section = listing.find("div", class_="fb4nyux")
    description = description_section.get_text(strip=True) if description_section else 'N/A'

    beds = 'N/A'
    date_range = 'N/A'

    # Find all subtitle divs for the number of beds and date range within the listing
    beds_and_dates = listing.find_all("div", {"data-testid": "listing-card-subtitle"})

    for subtitle in beds_and_dates:
        text = subtitle.get_text(strip=True)
        
        # Check if the subtitle text contains information about beds
        if 'bed' in text.lower():
            beds = text
        # Check if the subtitle text looks like a date range
        elif '-' in text:
            date_range = text

    # Extracting the price per day (usually found with a different class)
    price_per_day = listing.find("div", class_="pquyp1l").get_text(strip=True) if listing.find("div", class_="pquyp1l") else 'N/A'

    # Extracting the rating
    rating = listing.find("div", class_="t1a9j9y7").get_text(strip=True) if listing.find("div", class_="t1a9j9y7") else 'N/A'

    # Extracting the listing URL. The URL is relative, need to prepend the base Airbnb URL.
    listing_url_section = listing.find("div", class_="c14whb16") 
    listing_url = (
        "https://www.airbnb.com" + listing_url_section.find("a")["href"] if listing_url_section else ""
    )

    # Create a dictionary for the current listing
    listing_data = {
        "Title": title,
        "Description": description,
        "Beds": beds,
        "Price Per Day": price_per_day,
        "Rating": rating,
        "Listing URL": listing_url
    }

    # Append the listing dictionary to the results list
    results.append(listing_data)

# Write the results to a JSON file
with open('airbnb_beyoglu_results.json', 'w') as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print("Results saved to airbnb_beyoglu_results.json")
