"""
様々なサイトからコンテンツを取得するためのAPIを提供します.
"""
import json

import requests

from flask import Blueprint
from bs4 import BeautifulSoup

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def index_api():
    """APIのリソースを提供"""
    return 'hello'


@bp.route('/get_contents/qiita')
def get_contents_qiita():
    """
    Qiitaの記事一覧を取得してJsonでお返し.
    手に入れるのは1日のトレンドとして表示される全件 Qiita上では毎日5時, 17時に変化するらしいのであんまり叩かないように(?)
    """

    res = requests.get('https://qiita.com/')
    soup = BeautifulSoup(res.text, 'html.parser')
    target = soup.select('div[data-hyperapp-app="Trend"]')[0]
    return target.get('data-hyperapp-props')


@bp.route('/get_contents/gigazine')
def get_contents_gigazine():
    """
    Gigazineの記事一覧を取得してJsonでお返し.
    40件手に入るんですかね？
    """
    targets = []
    res = requests.get('https://gigazine.net')
    soup = BeautifulSoup(res.text, 'html.parser')
    section_all = soup.find_all('section')
    for section in section_all:
        target = section.find('h2').find('a')
        targets.append(dict(title=target.find('span').string, url=target.get('href'),
                            created_at=section.find('time').get('datetime')))

    return json.dumps(targets)


@bp.route('/get_contents/github_trending')
def get_contents_github_trending():
    """
    GitHub Trendingからトレンドを取得
    """
    targets = []
    res = requests.get('https://github.com/trending?since=daily&spoken_language_code=en')
    soup = BeautifulSoup(res.text, 'html.parser')
    article_all = soup.find_all('article')
    for article in article_all:
        name = article.find('h1').find('a').get('href')
        url = 'https://github.com' + name
        description = article.find('p', class_='col-9 text-gray my-1 pr-4').string
        targets.append({'name': name, 'url': url, 'description': description})

    return json.dumps(targets)


@bp.route('/get_contents/hacker_news')
def get_contents_hacker_news():
    """
    Hacker NewsからBestニュースを取得
    """
    targets = []
    res = requests.get('https://hacker-news.firebaseio.com/v0/beststories.json')
    for itemId in res.json()[0:19]:
        res = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{itemId}.json")
        targets.append(res.json())

    return json.dumps(targets)

