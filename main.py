import time
from datetime import date
from bs4 import BeautifulSoup, ResultSet
import requests
import pandas as pd


def scrape_flats(url) -> ResultSet:
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    flats = soup.find_all("div", class_="propertyCard-wrapper")
    return flats


def scrape_data(flats) -> list:
    data = []
    for flat in flats:

        totalPrice = flat.find("span", class_="propertyCard-priceValue").text.strip()
        totalPrice = totalPrice.split()[0].replace('£', '').replace(',', '')
        totalPrice = int(totalPrice)

        bedrooms = flat.find("div", class_="propertyCard-details").h2.text.strip()
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

    return data


def build_df(information):
    df = pd.DataFrame(information, columns=['Address', 'No of Bedrooms', 'Total Price', 'Price per Bedroom', 'Distance',
                                            'Hyperlink'])
    return df


def display_df(dataFrame, minBedrooms=0):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    print(dataFrame.loc[dataFrame['No of Bedrooms'] >= minBedrooms])


def get_minBedrooms_from_user():
    while True:
        minBedrooms = input("What is the minimum number of bedrooms you need? ")

        try:
            minBedrooms = int(minBedrooms)
            break
        except ValueError:
            print("Please enter a valid integer.")

    return minBedrooms


def make_csv(df):
    fileName = input("Enter name for .csv: ")  # TODO: Check if file name is valid
    if fileName == "":
        fileName = str(date.today())

    df.to_csv(fileName, index=False)


def find_flats(url, generateCSV=False):
    flats = scrape_flats(url)
    dataOnFlats = scrape_data(flats)
    df = build_df(dataOnFlats)
    display_df(df, get_minBedrooms_from_user())

    if generateCSV:
        make_csv(df)


if __name__ == '__main__':
    while True:
        urlToScrape = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=POSTCODE%5E319633&radius=1.0&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='
        find_flats(urlToScrape, generateCSV=False) #TODO: refactor generateCSV, instead of paramater ask user for (Y/N) input
        print("See you tomorrow!")
        timeToWait = 86400  # 1 day -> 86400 seconds
        time.sleep(86400)
