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

    existing_data = []
    try:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
    except FileNotFoundError:
        pass

    existing_data.insert(0, data_dict)

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(data_dict.keys()))
        writer.writeheader()
        writer.writerows(existing_data)


if __name__ == "__main__":
    main()
