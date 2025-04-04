'''
Script to download PDFs from web page
'''
from download_all_pdfs import download_all_pdfs_from_url
import sys

if len(sys.argv) not in [3, 4]:
    print(sys.argv)
    print("Usage: python DownloadPDFScript.py <url> <download_loc> -<base_pth>")
    sys.exit(0)

base_pth = False
if len(sys.argv) == 4:
    base_pth = sys.argv[3]
url = sys.argv[1]
download_loc = sys.argv[2]

download_all_pdfs_from_url(url, download_loc, base_pth)
