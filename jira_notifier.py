import feedparser
import requests
import time
import hashlib
import os
import json
from bs4 import BeautifulSoup
import re
from winotify import Notification

PROJECT_NAME = ''
RSS_FEED_URL = ''
JESSSION_ID = ''
LINK_NUMBER = 2
FETCH_EVERY_SECOND = 500

def fetch_rss_feed():
    payload = {}
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cache-Control': 'max-age=0',
      'Connection': 'keep-alive',
      'Cookie': rf'JSESSIONID={JESSSION_ID};',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", RSS_FEED_URL, headers=headers, data=payload)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch RSS feed.")
        return None
    
def parse_rss_feed(feed_content):
    feed = feedparser.parse(feed_content)
    return feed.entries

def sanitizeText(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def send_notification_with_url(title, message, url):
    toast = Notification(app_id="Jira Notifier",
                        title=title,
                        msg=message)

    toast.add_actions(label="Open", 
                    launch=url)
    toast.show()

def get_feed_hash(entries):
    hash_string = "".join([entry.title + entry.summary for entry in entries])
    return hashlib.sha256(hash_string.encode()).hexdigest()

def get_seen_entries():
    if os.path.exists("seen_entries.json"):
        with open("seen_entries.json", "r") as file:
            return json.load(file)
    else:
        return []

def save_seen_entries(entries):
    with open("seen_entries.json", "w") as file:
        json.dump(entries, file)

def extract_id_from_string(input_string):
    pattern = rf'{PROJECT_NAME}-\d+'
    match = re.search(pattern, input_string)
    
    if match:
        return match.group()
    else:
        return None

def extract_second_link_url(entry_title):
    soup = BeautifulSoup(entry_title, "html.parser")
    
    anchor_tags = soup.find_all("a")
    
    if len(anchor_tags) >= LINK_NUMBER:
        second_link_url = anchor_tags[1].get("href")
        return second_link_url
    
    return None

def check_rss_feed():
    feed_content = fetch_rss_feed()
    if feed_content:
        entries = parse_rss_feed(feed_content)
        seen_entries = get_seen_entries()

        current_hash = get_feed_hash(entries)
        if not os.path.exists("initial_hash.txt"):
            with open("initial_hash.txt", "w") as file:
                file.write(current_hash)
            return

        with open("initial_hash.txt", "r") as file:
            initial_hash = file.read()
            if current_hash != initial_hash:

                with open("initial_hash.txt", "w") as file:
                    file.write(current_hash)

                new_entries = [entry for entry in entries if entry.title not in seen_entries]

                for entry in new_entries:
                    title = extract_id_from_string(sanitizeText(entry.title))
                    summary = sanitizeText(entry.summary)
                    link = extract_second_link_url(entry.title)
                    print(title)
                    print(summary)
                    print(link)
                    print("----------------------------------------------------")
                    if title is not None and summary is not None:
                        send_notification_with_url(title[0:64], summary[0:256], link)

                seen_entries.extend([entry.title for entry in new_entries])
                save_seen_entries(seen_entries)

def main():
    while True:
        check_rss_feed()
        time.sleep(FETCH_EVERY_SECOND) 

if __name__ == "__main__":
    main()