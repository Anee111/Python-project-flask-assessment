# youtube_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_youtube_videos():
    url = "https://www.youtube.com/results?search_query=python"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    videos = []
    for item in soup.select(".yt-lockup-content"):
        title = item.select_one(".yt-lockup-title a").text
        videos.append(title)
    return videos
