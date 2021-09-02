import sys
import csv
from datetime import datetime

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found.")


def create_name():
    now = datetime.now()
    dt = now.strftime("%d-%m-%Y-%H-%M-%S")
    return f'scraped-links-{dt}.csv'


def print_links(pages, links):
    counter = 1
    for link in links:
        if counter % 10 == 1:
            print(f'Page {counter // 10 + 1} of {pages}')
        print(link)
        counter += 1


def create_dict(keyword, keys, values):
    lst = [(keys[0], keyword[:-1])]
    for i in range(len(values)):
        if 'www.searchenginejournal.com' in values[i]: # Check if pointing to searchjournal.com
            lst.append((keys[i+1], values[i]))
        else:
            lst.append((keys[i+1], 'not_searchenginejournal'))

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

    # Open or create csv file
    with open(create_name(), mode='w') as csv_file:
        fieldnames = ['keyword'] + [f'link{x+1}' for x in range(pages*10)] # Generate fieldnames
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for keyword in file.readlines():
            url = f'https://www.searchenginejournal.com/ {keyword}' # Build a query
            links = [link for link in search(url, stop=pages * 10)] # Get the results

            # Save links to csv file
            data = create_dict(keyword, fieldnames, links)
            writer.writerow(data)

            # Print links associated with the given query
            print(f'\nResults for keyword: {keyword}')
            print_links(pages, links)

    file.close()
