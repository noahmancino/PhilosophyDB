'''
This script is meant to download from webpages which contain many links to web hosted PDFs
'''
import os
from scrape_config import url_to_scrape, download_location, base_path
import requests
from bs4 import BeautifulSoup

page_source = requests.get(url_to_scrape)
soup = BeautifulSoup(page_source.content, 'lxml')
links = [str(link['href']) for link in soup.find_all('a', href=True)]
links = set(links)
links = [link for link in links if link[-4:] == '.pdf']

# Crude way of dealing with relative paths
if base_path:
    for i, link in enumerate(links):
        if link[:4] != 'http':
            links[i] = base_path + link

for link in links:
    new_file_name = link.replace('/', '_')
    file_path = download_location + new_file_name
    print('Downloading ' + link + ' to ' + file_path)
    with open(file_path, 'wb') as f:
        try:
            f.write(requests.get(link).content)
        except Exception as ex:
            print('Error downloading ' + link)
            print(type(ex))
            f.close()
            os.remove(file_path)
