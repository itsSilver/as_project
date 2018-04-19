# coding=utf-8


import os
import shutil
import threading
import Queue
from flask import render_template, request, jsonify
from . import main
from .. import spiders


@main.route('/')
def index():
    return render_template('index.html') 


@main.route('/start_spider/', methods=['GET', 'POST'])
def start_spider():
    if request.method == 'POST':
        try:
            urls = str(request.form['urls'])
            url_mid_name =  urls.split('.')[1]
            if url_mid_name == 'betburger':
                q = Queue.Queue()
                while True:
                    t1 = threading.Thread(target=get_data, args=(url_mid_name, q,))
                    t1.start()
                    t1.join()
                    data = q.get_nowait()
                    if len(data) != 0:
                        return jsonify({'data': data})
            else:
                return jsonify({'data': False})
        except:
            return jsonify({'data': False})


def get_data(url_mid_name, q):
    urls = 'https://api-lv.betburger.com/api/v1/arbs/pro_search?access_token='
    dir_url = 'https://api-lv.betburger.com/api/v1/directories?access_token='
    bet_val_url = 'https://api-lv.betburger.com/api/v1/bet_combinations/'
    mb = spiders.back_mod_betburger.ModBetburger(urls, dir_url, bet_val_url, url_mid_name)
    data = mb.get_data_info()
    q.put(data)


@main.route('/del_tmp/', methods=['GET'])
def del_tmp():
    if request.method == 'GET':
        now_dir = os.getcwd() + '/tmp/'
        dir_list = os.listdir(now_dir)
        if len(dir_list) > 0:
            shutil.rmtree(now_dir)
            os.mkdir(now_dir)
        return jsonify({'is_del':True}) 


@main.route('/current_bet_url/', methods=['POST'])
def current_bet_url():
    if request.method == 'POST':
        ranks1 = str(request.form['ranks1'].encode('utf-8'))
        url1 = str(request.form['url1'].encode('utf-8'))
        ranks2 = str(request.form['ranks2'].encode('utf-8'))
        url2 = str(request.form['url2'].encode('utf-8'))
        print("url1:",url1)
        print("url2:",url2)
        url1_mid_name = url1.split('.')[1]
        url2_mid_name = url2.split('.')[1]
        if url1_mid_name == "marathonbet":
            current_bet_url1 = spiders.open_marathon.get_current_url(url1, ranks1)
        else:
            current_bet_url1 = ''

        if url2_mid_name == "marathonbet":
            current_bet_url2 = spiders.open_marathon.get_current_url(url2, ranks2)
        else:
            current_bet_url2 = ''
        return jsonify({'url1': current_bet_url1, 'url2': current_bet_url2})
