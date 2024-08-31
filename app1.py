# app.py
# app.py
from flask import Flask, render_template
from youtube_scraper import scrape_youtube_videos
from amazon_scraper import scrape_amazon_products

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/youtube')
def youtube_data():
    videos = scrape_youtube_videos()
    return render_template('youtube.html', videos=videos)

@app.route('/amazon')
def amazon_data():
    products = scrape_amazon_products()
    return render_template('amazon.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
