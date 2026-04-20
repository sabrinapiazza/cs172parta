#main file 


from queue import Queue
from urllib.parse import urljoin, urldefrag
from bs4 import BeautifulSoup
import requests

#advithi
frontier = Queue()
visited = set() 
seed_list = []

#grabbing all the urls from the seed.txt file
with open("seed.txt", "r") as file_urls:
    for url_line in file_urls:
        indiv_url = url_line.strip() 
        if indiv_url: 
            seed_list.append(indiv_url)

#double checking seed_list grabs all the url links
#print(seed_list)

# load the urls from seed list into frontier
for i_url in seed_list:
    frontier.get(i_url)
    #add link to visted list
    visited.add(i_url)

#while the frontier isn't empty & max_count < threshold,
count = 0
while not frontier.empty() and count < 1000:
    curr_url = frontier.get()

#sabrina

# grab each url from frontier & parse through & save html file
# add all the links to the frontier