# University Accomodation Web Scraper

# Overview
This Python-based web scraper retrieves rental property data from Rightmove for properties located within a mile of the University of Glasgow. </br> 
The scraped data is organized into a Pandas DataFrame for further analysis or manipulation. </br> 
Additionally, there is an option to save the data as a CSV file for easy sharing and record-keeping.

# Features
* <b>Scrapes rental property data:</b> Gathers information such as property title, price, location, and other relevant details from Rightmove.
* <b>Data organization:</b> Compiles the collected data into a well-structured Pandas DataFrame.
* <b>CSV export (optional):</b> Offers the ability to save the DataFrame as a CSV file for offline use or further processing.

# Usage
Clone the repository or download the script:


```
git clone https://github.com/L00K-LUKE/UniversityAccommodationWebScraper.git
```

# Modify the script (if needed):

Adjust the parameters in the script to match your specific requirements, such as the search URL or any specific filtering criteria for the properties.

# Run the script:

`python rightmove_scraper.py`

# View the DataFrame:

After running the script, the rental property data will be displayed as a Pandas DataFrame.

# Optional - Export to CSV:

If you wish to save the data to a CSV file, simply pass True as an argument when find_flats is called. 

```
find_flats(True)
```
The file will be saved with the name being the date in the same directory as the script.

# Customization
* Search Criteria: Modify the search URL to target specific areas or types of properties.
* Data Fields: Customize the fields you want to extract by adjusting the BeautifulSoup selectors.
* CSV Filename: Change the filename in the CSV export section to your preferred name.
  
