import csv
from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup


URL = "https://gpura.org/"
CSV_FILE = "visitors.csv"
TIMEZONE = "Asia/Kolkata"
FIELDNAMES = ["date", "time", "reads", "downloads"]


def clean_count(value):
    return value.strip().replace(",", "")


def fetch_visitor_stats():
    response = requests.get(
        URL,
        headers={"User-Agent": "gpurastatupdater/1.0"},
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    totals = soup.find("div", class_="item-stats-totals")
    if totals is None:
        raise RuntimeError("Could not find item-stats-totals on gpura.org")

    stats = {}
    for stat in totals.find_all("span", class_="item-stats-totals-stat"):
        count = stat.find("strong", class_="item-stats-totals-count")
        if count is None:
            continue

        label = stat.get_text(" ", strip=True).replace(count.get_text(strip=True), "")
        key = label.strip().lower()
        if key in {"reads", "downloads"}:
            stats[key] = clean_count(count.get_text(strip=True))

    missing = [key for key in ("reads", "downloads") if key not in stats]
    if missing:
        raise RuntimeError(f"Missing visitor stats: {', '.join(missing)}")

    return stats


def read_existing_rows():
    try:
        with open(CSV_FILE, mode="r", newline="") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def write_rows(rows):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main():
    ist = pytz.timezone(TIMEZONE)
    current_time = datetime.now(ist)
    stats = fetch_visitor_stats()

    row = {
        "date": current_time.strftime("%Y-%m-%d"),
        "time": current_time.strftime("%H:%M:%S"),
        "reads": stats["reads"],
        "downloads": stats["downloads"],
    }

    existing_rows = read_existing_rows()
    existing_rows.insert(0, row)
    write_rows(existing_rows)


if __name__ == "__main__":
    main()
