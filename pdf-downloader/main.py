import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

#this is a simple pdf downloader script written in python by DHIRAJ

url = "https://www.aspirestudy.in/notifications/nimcet/nimcetmaterial.php"

response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

pdf_links = []
for link in soup.find_all("a", href=True):
    if link["href"].endswith(".pdf"):
        pdf_links.append(link["href"])

for pdf_link in tqdm(pdf_links, desc="Downloading PDFs", unit="file"):
    filename = os.path.basename(pdf_link)
    
    try:
        response = requests.get(pdf_link, stream=True)
        response.raise_for_status()

        with open(filename, "wb") as f:
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
                
            progress_bar.close()

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")
        # Handle the error (e.g., skip this file or log the error)

print("Downloaded PDFs:", pdf_links)

