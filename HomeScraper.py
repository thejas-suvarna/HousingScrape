#These are the packages that you will need to install in your environment

#Create a folder. Run 'python3 -m venv env'
#Run 'source env/bin/activate' <- you are now in the virtual environment
#install packages using pip

#run this file using "python HomeScraper.py"

from bs4 import BeautifulSoup
import requests
import csv

#given the text of the website source code. Extract the information we need followed by a given keyword
def datareturn(text, string):
    potential_start = text.find(string) + len(string) + 1
    potential_end = text.find("-", potential_start)
    if ((potential_end - potential_start) > 10):
        return -1
    else:
        return text[potential_start: potential_end]

#Specialized data return function for acres because it is follow by '>' instead of '-'
def datareturnAcres(text, string):
    potential_start = text.find(string) + len(string) + 1
    potential_end = text.find(">", potential_start)
    if ((potential_end - potential_start) > 10):
        return -1
    else:
        return text[potential_start: potential_end]

filename = "Listings.csv"
file = csv.writer(open(filename, "w"))

# Write CSV Header, If you dont need that, remove this line
file.writerow(["date", "value", "address", "url", "seller", "buyer", "build-year", "sqft", "bedrooms", "full baths", "half-baths", "lot size"])

#28 pages of info
for i in range(1,28):
    url = "https://bsaonline.com/ASSG_AdvancedSearch/AdvancedSearchResults?Agricultural=true&Commercial=true&Residential=true&Industrial=true&TimberCutover=true&Developmental=true&AdvancedPropClassSearch=False&uid=283&SaleDateRange=3%2F30%2F2019-9%2F30%2F2019&PriceRange=0-0&AreaRange=0-0&YearBuiltRange=0-0&BedRange=0-0&BathRange=0-0&SearchOrigin=1&DetailResultsGrid-size=50&DetailResultsGrid-page=" + i.__str__()
    print(i)
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    #find all rows which acts as one transaction using the class search attribute
    for listing in content.findAll('tr', attrs={"class": "site-search-row"}):
        #put each piece of data into a structure
        collection = []
        for data in listing.findAll('td'):
            collection.append(data)
        listingObj = {
            "url": collection[0].get_text(),
            "date": collection[1].get_text(),
            "value": collection[2].get_text(),
            "address": collection[3].get_text(),
            "seller": collection[4].get_text(),
            "buyer": collection[5].get_text(),
        }

        #go to each url
        url1 = "https://bsaonline.com" + listingObj["url"]
        response1 = requests.get(url1, timeout=5)
        content1 = BeautifulSoup(response1.content, "html.parser")

        text = content1.get_text()
        text = text[text.find("Summary Information"):text.find("Assessed Value")]

        #add info to the dictionary
        listingObj["build-year"] = datareturn(text, "Year Built:")
        listingObj["sqft"] = datareturn(text, "Sq. Feet:")
        listingObj["bedrooms"] = datareturn(text, "Bedrooms:")
        listingObj["fullbath"] = datareturn(text, "Full Baths:")
        listingObj["halfbath"] = datareturn(text, "Half Baths:")
        listingObj["lotsize"] = datareturnAcres(text, "Acres:")
        # listingObj["size"] =

        #write to file
        file.writerow([listingObj["date"],
                       listingObj["value"],
                       listingObj["address"],
                       listingObj["url"],
                       listingObj["seller"],
                       listingObj["buyer"],
                       listingObj["build-year"],
                       listingObj["sqft"],
                       listingObj["bedrooms"],
                       listingObj["fullbath"],
                       listingObj["halfbath"],
                       listingObj["lotsize"]])



