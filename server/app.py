from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from bs4 import BeautifulSoup as bs
import requests
import json
import pandas as pd
from urllib.request import urlopen

app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def ping():
    return 'pong'

@app.route("/number/<int:number>")
def multi(number):
    result = number * 3
    return '{:d}'.format(result)

@app.route("/naverwindow/<int:shopid>")
def get_info(shopid):
    api_url = 'https://shopping.naver.com/v1/products?page=1&pageSize=1000&sort=RECENT&displayType=CATEGORY_HOME&storeId={:d}'.format(shopid)
    page = requests.get(api_url)
    soup = bs(page.content,'html.parser')
    response = json.loads(str(soup))
    response_keys = response.keys()
    return jsonify(response)

@app.route("/sum/<int:num_1>/<int:num_2>")
def sum(num_1,num_2):
    result = num_1 + num_2
    return '{:d}'.format(result)

@app.route("/naver")
def products():
    id = request.args.get('shop_id')
    id = int(id)
    count = request.args.get('product_count')
    count = int(count)
    page = request.args.get('product_page')
    page = int(page)
    api_url = 'https://shopping.naver.com/v1/products?page={:d}&pageSize={:d}&sort=RECENT&displayType=CATEGORY_HOME&storeId={:d}'.format(page,count,id)
    page = requests.get(api_url)
    soup = bs(page.content,'html.parser')
    response = json.loads(str(soup))
    response_keys = response.keys()
    return jsonify(response)

@app.route("/echo")
def echo():
    thing = request.args.get('thing')
    place = request.args.get('place')
    return 'the thing is {}, and the place is {}'.format(thing,place)

@app.route("/test")
def test():
    kwargs = {}
    kwargs['thing'] = request.args.get('thing')
    kwargs['place'] = request.args.get('place')
    return 'the thing is {}, and the place is {}'.format(**kwargs)

@app.route("/cafefy")
def product():
    shop_name = request.args.get('shop_name')
    product_url = 'https://{}.cafe24api.com/api/v2/products'.format(shop_name)
    headers={'Content-Type': 'application/json',
            'X-Cafe24-Client-Id': 'xoN6nzRsH1kmofcOi98mKH'
            }
    return requests.get(product_url, headers=headers).json()


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
