#main file 


from queue import Queue
#from urllib.parse import urljoin, urldefrag
from bs4 import BeautifulSoup
import requests
import os

#advithi
frontier = Queue()
visited = set() 
seed_list = []
os.makedirs("pages", exist_ok=True)

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
    frontier.put(i_url)
    #add link to visted list
    visited.add(i_url)

#while the frontier isn't empty & max_count < threshold,
count = 0
while not frontier.empty() and count < 1000:
    curr_url = frontier.get()
    try:
        html = requests.get(curr_url).text
    except:
        continue

    with open(f"pages/page_{count}.html", "w") as save:
        save.write(html)
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'): #ask ta 
        print(link.get('href'))
        href = link.get('href')
        if href and href not in visited:
            frontier.put(href)
            visited.add(href)

    count += 1 


#sabrina

# grab each url from frontier & parse through & save html file
# add all the links to the frontier