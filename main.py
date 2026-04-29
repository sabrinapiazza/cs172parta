#main file 


from queue import Queue
from urllib.parse import urljoin, urldefrag, quote 
from bs4 import BeautifulSoup
from compliance import ComplianceManager
import requests
import os
import sys

#advithi
frontier = Queue()
visited = set() 
seed_list = []

#making this into system argument
#os.makedirs("pages", exist_ok=True)

if len(sys.argv) != 5:
    print("Usage: ./crawler.sh <seed-file> <num-pages> <hops-away> <output-dir>")
    sys.exit(1)

seed_file = sys.argv[1]
max_pages = int(sys.argv[2])
max_hops = int(sys.argv[3])
output_dir = sys.argv[4]

os.makedirs(output_dir, exist_ok=True)

# used for robots.txt check - Pramika 
compliance = ComplianceManager()

#grabbing all the urls from the seed.txt file
#for deployment type seed.txt when running as specified above
with open(seed_file, "r") as file_urls:
    for url_line in file_urls:
        indiv_url = url_line.strip() 
        if indiv_url: 
            seed_list.append(indiv_url)

#double checking seed_list grabs all the url links
#print(seed_list)

# load the urls from seed list into frontier
for i_url in seed_list:
    # 0 is the hop count!
    frontier.put((i_url,0))
    #add link to visted list
    visited.add(i_url)


#while the frontier isn't empty & max_count < threshold,
count = 0
while not frontier.empty() and count < max_pages:
    # curr_url = frontier.get()
    curr_url, hop = frontier.get()


    # --- ROBOTS.TXT CHECK --- Pramika
    if not compliance.can_fetch(curr_url):
        print(f"Skipping {curr_url} (Blocked by robots.txt)")
        continue

    try:
        response = requests.get(curr_url, timeout=5)
        html = response.text
    except:
        continue

    # --- META TAG CHECK ---
    meta_rules = compliance.check_meta_tags(html)
    
    # If 'noindex', we don't save the file
    if not meta_rules["noindex"]:
        # with open(f"pages/page_{count}.html", "w", encoding="utf-8") as save:
        with open(f"{output_dir}/page_{count}.html", "w", encoding="utf-8") as save:
            save.write(html)
            count += 1 

    # If 'nofollow', we don't extract links from this page
    if meta_rules["nofollow"]:
        continue
    #------------------------------

    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        #print(link.get('href'))
        href = link.get('href')

        if not href:
            continue

        # join urls
        href = urljoin(curr_url, href)

        # remove bookmakrs #main
        href, _ = urldefrag(href)

        # sorts out only links with http
        if not href.startswith("https://"): 
            continue

        # removes self paths 
        if href.rstrip("/") == curr_url.rstrip("/"):
            continue

        # no pdf no pictures 
        bad_extensions = (".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp")
        if href.lower().endswith(bad_extensions):
            continue

        # invalid characters in urls to avoid MalformedURLexception
        href = quote(href, safe=":/?=&%") 

        # ensures there are no duplicates
        if href not in visited:
            if hop + 1 <= max_hops:
                print("clean url:", href)
                frontier.put((href, hop + 1))
                visited.add(href)


#sabrina

# grab each url from frontier & parse through & save html file
# add all the links to the frontier