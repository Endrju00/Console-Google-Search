import sys
import csv
from datetime import datetime
import requests
import json

# GLOBAL VARIABLES
API_KEY = open('.api_key').read()
CX = '7929aaa645c6089dc'
PAGES = 1 # Script does not work for more pages


def create_name():
    """Return the string (filename) with current datetime."""
    now = datetime.now()
    dt = now.strftime("%d-%m-%Y-%H-%M-%S")
    return f'{dt}.csv'


def print_links(links):
    """Print links on particular pages."""
    for link in links:
        print(link)


def create_dict(keyword, keys, values):
    """Return dict with given keywords and values"""
    lst = [(keys[0], keyword[:-1])] # Given keyword as a first value
    for i in range(len(values)):
        lst.append((keys[i+1], values[i]))

    return dict(lst)



if __name__ == '__main__':
    # Open the keywords.txt
    try:
        file = open('keywords.txt')
    except:
        print("ERROR: Could not open the keyword.txt. Please check if it is in current directory.")
        exit()

    # Open or create csv file for links
    name = create_name()
    with open(f'scrapedLinks-{name}', mode='w') as csv_file:
        fieldnames = ['keyword'] + [f'link{x+1}' for x in range(PAGES*10)] # Generate fieldnames
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Open or create csv file for totalResults
        with open(f'totalResults-{name}', mode='w') as csv_file:
            fieldnames2 = ['keyword', 'totalResults'] # Generate fieldnames
            writer2 = csv.DictWriter(csv_file, fieldnames=fieldnames2)
            writer2.writeheader()

            # Read the keywords
            for keyword in file.readlines():
                url = f'https://www.googleapis.com/customsearch/v1?q={keyword}&key={API_KEY}&cx={CX}' # Build a query
                r = requests.get(url) # Get the results
                data = r.json() # Save in json format

                # Get the number of results and save them in csv file with the keyword
                totalResults = data['queries']['request'][0]['totalResults']
                writer2.writerow({'keyword': keyword[:-1], 'totalResults': totalResults})

                # Get the links
                links = [item['link'] for item in data['items']]

                # Save links to csv file
                d = create_dict(keyword, fieldnames, links)
                writer.writerow(d)

                # Print links associated with the given query
                print(f'\nTotal number of results: {totalResults}')
                print(f'Results for keyword: {keyword}')
                print_links(links)

    file.close()
