import requests
import os
import Transform_and_Load as trans
from bs4 import BeautifulSoup
from multiprocessing import Pool
import datetime

def download_page(page_number):
    base_url = "https://www.scrapethissite.com/pages/forms/"
    output_dir = "raw/hockey_pages"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    response = requests.get(base_url, params={"page_num": page_number})
    if response.status_code != 200:
        print(f"Failed to fetch page {page_number}.")
        return
    
    file_path = os.path.join(output_dir, f"Page_{page_number}.html")
    with open(file_path, "wb") as file:
        file.write(response.content)

def download_hockey_pages():
    base_url = "https://www.scrapethissite.com/pages/forms/"
    page_number = 1    
    page_numbers = []
    
    while True:
        response = requests.get(base_url, params={"page_num": page_number})
        if response.status_code != 200:
            print(f"Failed to fetch page {page_number}.")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        next_button = soup.find("a", {"aria-label": "Next"})
        if not next_button or "disabled" in next_button.get("class", []):
            break
        
        page_numbers.append(page_number)
        page_number += 1
    
    page_numbers.append(page_number)  # Append the last page (without the next button)

    with Pool() as pool:
        pool.map(download_page, page_numbers)
    
    print("Download process complete.")

if __name__ == "__main__":
    init_time=datetime.datetime.now()
    #Extract
    output_dir = "raw/hockey_pages"
    download_hockey_pages()
    #Transform
    directory_path = output_dir
    zip_file_name = "all_files.zip"
    output_excel_location = "transformed"
    trans.rename_and_zip_files(directory_path, zip_file_name)
    trans.create_nhl_stats_sheet(directory_path, output_excel_location)
    end_time = datetime.datetime.now()
    time_taken = end_time - init_time
    print(f"Total time taken = {time_taken}")
