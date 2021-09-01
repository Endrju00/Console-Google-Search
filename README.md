# ONELY Intern tasks - scraping
Algorithm is as follows:
1. The program is looping through a list of keywords in the .txt file (keywords.txt)
2. Then it queries Google.com using the following set of queries:
a. site:https://www.searchenginejournal.com/ {keyword}
3. For every query, the program goes through Google Search Results and extracts all the
links pointing to SearchEngineJournal. We need extractions only from the first page
of results but if you can get more, it would be a good addition.
4. We also want the total number of results (the number above the first result) to be
extracted.
5. The program saves all the links pointing to SearchEngineJournal to a CSV file.
6. The total numbers of results should be saved in a different file along with the associated
keyword.
