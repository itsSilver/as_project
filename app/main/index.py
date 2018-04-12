# coding=utf-8


from flask import render_template, request
from . import main


@main.route('/')
def index():
    return render_template('index.html') 


@main.route('/start_spider/', methods=['GET', 'POST'])
def start_spider():
    if request.method == 'POST':
        urls = request.form['urls']
        print urls
