from bs4 import BeautifulSoup
import requests
import csv
import pytz
from datetime import datetime

url = "https://gpura.org/"
csv_file = 'data.csv'

def main():
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    num_elements = soup.find_all('p', class_='theNum')
    data_dict = {}

    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    data_dict["date"] = current_time.strftime('%Y-%m-%d') 
    data_dict["time"] = current_time.strftime('%H:%M:%S')

    data_dict["items"] = num_elements[0].get_text()
    data_dict["languages"] = num_elements[1].get_text()
    data_dict["collections"] = num_elements[2].get_text()
    data_dict["authors"] = num_elements[3].get_text()
    data_dict["pages"] = num_elements[4].get_text()

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, list(data_dict.keys()))
        
        if file.tell() == 0:
            writer.writeheader()
        
        writer.writerow(data_dict)

if __name__ == "__main__":
    main()
