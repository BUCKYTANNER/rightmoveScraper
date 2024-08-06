import datetime
import time
from datetime import date
import csv
from bs4 import BeautifulSoup
import requests

minBedrooms = input("What is the minimum number of bedrooms you need? ")
def find_flats():
    html_text = requests.get('https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=POSTCODE%5E319633&radius=1.0&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=').text
    soup = BeautifulSoup(html_text, 'lxml')
    flats = soup.find_all("div", class_= "propertyCard-wrapper")

    data = [['Address', 'NoOfBedrooms', 'TotalPrice', 'PricePerBedroom', 'Distance', 'Hyperlink']]
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

        if bedrooms < int(minBedrooms):
            continue

        address = flat.find("address").text.strip().replace(',', '')

        distance = flat.find("div", class_="propertyCard-distance").text.split()[0]
        distance = float(distance)

        hyperlink = "https://www.rightmove.co.uk" + flat.find("a", class_="propertyCard-link").get('href')

        data.append([address, bedrooms, totalPrice, pricePerRoom, distance, hyperlink])

    with open(str(date.today())+".csv", 'w', newline= '') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    print("CSV Created")


if __name__ == '__main__':
    while True:
        find_flats()
        timeToWait = 86400 # 1 day -> 86400 seconds
        print("See you tomorrow!")
        time.sleep(86400)
