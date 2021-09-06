import sys
import csv
from datetime import datetime
import requests
import json

# GLOBAL VARIABLES
API_KEY = open('.api_key').read()
CX = '7929aaa645c6089dc'


def create_name():
    """Return the string (filename) with current datetime."""
    now = datetime.now()
    dt = now.strftime("%d-%m-%Y-%H-%M-%S")
    return f'{dt}.csv'


def print_links(page_num, pages, links):
    """Print links on particular pages."""
    print(f'\nPage {page_num} of {pages}')
    for link in links:
        print(link)


def create_dict(keyword, keys, values):
    """Return dict with given keywords and values"""
    lst = [(keys[0], keyword[:-1])] # Given keyword as a first value
    for i in range(len(values)):
        lst.append((keys[i+1], values[i]))

    return dict(lst)



if __name__ == '__main__':
     # Get num of pages
    try:
        pages = int(sys.argv[1])
    except IndexError:
        pages = 1
        print("WARNING: No argument passed, number of pages set to 1.\n")
    except ValueError:
        print("ERROR: You should pass an integer as an argument.")
        exit()

    # Open the keywords.txt
    try:
        file = open('keywords.txt')
    except:
        print("ERROR: Could not open the keyword.txt. Please check if it is in current directory.")
        exit()

    # Open or create csv file for links
    name = create_name()
    with open(f'scrapedLinks-{name}', mode='w') as csv_file:
        fieldnames = ['keyword'] + [f'link{x+1}' for x in range(pages*10)] # Generate fieldnames
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Open or create csv file for totalResults
        with open(f'totalResults-{name}', mode='w') as csv_file:
            fieldnames2 = ['keyword', 'totalResults'] # Generate fieldnames
            writer2 = csv.DictWriter(csv_file, fieldnames=fieldnames2)
            writer2.writeheader()

            # Read the keywords
            for keyword in file.readlines():
                for page_num in range(pages):
                    url = f'https://www.googleapis.com/customsearch/v1?q={keyword}&key={API_KEY}&cx={CX}&start={page_num*10+1}' # Build a query
                    r = requests.get(url) # Get the results
                    data = r.json() # Save in json format

                    # At 1st page save results
                    if not page_num:
                        # Get the number of results and save them in csv file with the keyword
                        totalResults = data['queries']['request'][0]['totalResults']
                        writer2.writerow({'keyword': keyword[:-1], 'totalResults': totalResults})
                        print(f'\n\nTotal number of results: {totalResults}')
                        print(f'Results for keyword: {keyword[:-1]}')

                    # Get the links
                    links = [item['link'] for item in data['items']]

                    # Save links to csv file
                    d = create_dict(keyword, fieldnames, links)
                    writer.writerow(d)

                    # Print links associated with the given query
                    print_links(page_num+1, pages, links)

    file.close()
