'''
Contains function used by other scripts whenever utility to download all pdf links form a web page needed.
'''
import os
import requests
from bs4 import BeautifulSoup


def download_all_pdfs_from_url(url, download_loc, base_pth=''):
    page_source = requests.get(url).content
    download_all_pdfs_from_src(page_source, download_loc, base_pth)

def download_all_pdfs_from_src(page_source, download_loc, base_pth=''):
    soup = BeautifulSoup(page_source, 'lxml')
    links = [str(link['href']) for link in soup.find_all('a', href=True)]
    links = set(links)
    links = [link for link in links if link[-4:] == '.pdf']

    if base_pth:
        for i, link in enumerate(links):
            if link[:4] != 'http':
                links[i] = base_pth + link

    for link in links:
        new_file_name = link.replace('/', '_')
        file_path = download_loc + new_file_name
        print('Downloading ' + link + ' to ' + file_path)
        with open(file_path, 'wb') as f:
            try:
                f.write(requests.get(link).content)
            except Exception as ex:
                print('Error downloading ' + link)
                print(type(ex))
                f.close()
                os.remove(file_path)