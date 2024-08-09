import time
from datetime import date
from bs4 import BeautifulSoup
import requests
import pandas as pd

def find_flats(generateCSV = False):
    html_text = requests.get('https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=POSTCODE%5E319633&radius=1.0&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=').text
    soup = BeautifulSoup(html_text, 'lxml')
    flats = soup.find_all("div", class_= "propertyCard-wrapper")


    data = []
    for flat in flats:

        totalPrice = flat.find("span", class_ = "propertyCard-priceValue").text.strip()
        totalPrice = totalPrice.split()[0].replace('£', '').replace(',', '')
        totalPrice = int(totalPrice)

        bedrooms = flat.find("div", class_ = "propertyCard-details").h2.text.strip()
        if bedrooms.split()[0] != "Studio":
            bedrooms = int(bedrooms.split()[0])
            pricePerRoom = round(totalPrice / bedrooms, 2)
        else:
            bedrooms = 0
            pricePerRoom = totalPrice

        address = flat.find("address").text.strip().replace(',', '')

        distance = flat.find("div", class_="propertyCard-distance").text.split()[0]
        distance = float(distance)

        hyperlink = "https://www.rightmove.co.uk" + flat.find("a", class_="propertyCard-link").get('href')

        data.append([address, bedrooms, totalPrice, pricePerRoom, distance, hyperlink])

    df = pd.DataFrame(data, columns= ['Address', 'No of Bedrooms', 'Total Price', 'Price per Bedroom', 'Distance', 'Hyperlink'])

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    while True:
        minBedrooms = input("What is the minimum number of bedrooms you need? ")

        try:
            minBedrooms = int(minBedrooms)
            break
        except ValueError:
            print("Please enter a valid integer.")

    print(df.loc[df['No of Bedrooms'] >= minBedrooms])

    if generateCSV:
        fileName = str(date.today())
        df.to_csv(fileName, index=False)


if __name__ == '__main__':
    while True:
        find_flats(True)
        print("See you tomorrow!")
        timeToWait = 86400 # 1 day -> 86400 seconds
        time.sleep(86400)
