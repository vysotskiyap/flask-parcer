from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

name = "PARcer"
app = Flask(__name__)

def parse_site(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    for item in soup.select('.product'):
        title_elem = item.select_one('.product-title')
        price_elem = item.select_one('.product-price')
        link_elem = item.select_one('a')

        title = title_elem.text.strip() if title_elem else 'No title'
        price = price_elem.text.strip() if price_elem else 'No price'
        link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else '#'

        products.append({'title': title, 'price': price, 'link': link})

    return products

@app.route('/', methods=['GET', 'POST'])
def index():
    products = []
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            products = parse_site(url)
    return render_template('index.html', products=products)

if name == '__main__':
    app.run(host='0.0.0.0', port=10000)
