Instructions for Deployment of System
In order to deploy the system, follow the executable instructions listed below:

Run this the first time to start the execution:

chmod +x crawler.sh

Run this command with specifying what values you want in the brackets <>.

./crawler.sh <seed-file> <num-pages> <hops-away> <output-dir>

Definition of all variables for the purpose of our project:

Command argument
Definition
Project Argument 
seed-file
The file with the list of URLs we want to crawl.
seed.txt
num-pages
The number of maximum pages the crawler can return.
1000
hops-away
The number of hops away each URL can have.
6
output-dir
The directory that all crawled pages will be located in. 
pages


	

Example executable run according to our project arguments:
./crawler.sh seed.txt 1000 6 pages 
