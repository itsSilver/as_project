# coding=utf-8


from flask import render_template, request, jsonify
from . import main
from .. import spiders


@main.route('/')
def index():
    return render_template('index.html') 


@main.route('/start_spider/', methods=['GET', 'POST'])
def start_spider():
    if request.method == 'POST':
        urls = str(request.form['urls'])
        mid_str =  urls.split('.') 
        if mid_str[1] == 'betburger':
            # www.betburger.com
            urls = 'https://api-lv.betburger.com/api/v1/arbs/pro_search?access_token='
            dir_url = 'https://api-lv.betburger.com/api/v1/directories?access_token='
            bet_val_url = 'https://api-lv.betburger.com/api/v1/bet_combinations/'
            mb = spiders.back_mod_betburger.ModBetburger(urls, dir_url, bet_val_url)
            data = mb.get_data_info()
            return jsonify({'data': data})
        else:
            return jsonify({'data': False})
