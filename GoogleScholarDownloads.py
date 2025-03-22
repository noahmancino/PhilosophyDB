'''
Utility for scraping Google Scholar pages of researchers for their publicly available articles
'''
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import subprocess
from download_all_pdfs import download_all_pdfs_from_src

if len(sys.argv) != 3:
    print(len(sys.argv))
    print('Usage: python GoogleScholarDownloads.py <url> <download_loc>')

url = sys.argv[1]
download_loc = sys.argv[2]

# Selenium stuff is all
chrome_options = Options()
chrome_options.add_argument("--headless")

service = Service('/opt/homebrew/bin/chromedriver')  # Default homebrew path
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

time.sleep(1)

# Meant to click 'show more' until all citation shown.
# Limited for loop in case of unforeseen circumstances or extremely large bibliographies
for _ in range(10):
    try:
        button = driver.find_element(By.ID, 'gsc_bpf_more')

        if button.get_attribute('disabled'):
            print("Button is disabled. Exiting loop.")
            break

        button.click()
        print("Button clicked.")

        time.sleep(.5)
    except Exception as e:
        print(f"An error occurred: {e}")
        break

print('Extracting base page source...')
html_content = driver.page_source
driver.quit()

# Run pdf extraction on each link
soup = BeautifulSoup(html_content, 'lxml')
links = [str(link['href']) for link in soup.find_all('a', href=True)]
links = set(links)
links = [link for link in links if 'view_op=view_citation' in link]
for link in links:
    result = subprocess.run(['python', 'DownloadPDFScript.py', 'https://scholar.google.com/' + link, download_loc],
                            capture_output=True,
                            text=True)
    print('Citation page output: {}'.format(result.stdout))

    if result.stderr:
        print(f'Errors: {result.stderr}')





