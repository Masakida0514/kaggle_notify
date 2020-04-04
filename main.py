import os
import json
import datetime
import requests
from logging import StreamHandler, INFO, DEBUG, Formatter, FileHandler, getLogger

# import dotenv
from kaggle import KaggleApi

LINE_NOTIFY_TOKEN = os.environ['LINE_NOTIFY_TOKEN']
COMPETITION_NAME = os.environ['COMPETITION_NAME']

logger = getLogger(__name__)
log_fmt = Formatter(
    '%(asctime)s %(name)s %(lineno)d [%(levelname)s][%(funcName)s] %(message)s')
# info
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(log_fmt)
logger.addHandler(handler)
logger.setLevel(INFO)
# debug
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(log_fmt)
logger.addHandler(handler)
logger.setLevel(DEBUG)

def get_time_now():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    y = str(now.year)
    m = str(now.month)
    d = str(now.day)
    h = str(now.hour)
    message = y + '年' + m + '月'+ d + '日' + h + '時のカーネルについてお知らせします!'
    return message

def get_kernels_list():
    api = KaggleApi()
    api.authenticate()
    kernels_list = api.kernels_list(
        competition=COMPETITION_NAME,
        page_size=18,
        language='python',
        sort_by='scoreAscending'
    )
    return kernels_list

def get_kernels_list_2():
    api = KaggleApi()
    api.authenticate()
    kernels_list = api.kernels_list(
        competition=COMPETITION_NAME,
        page_size=18,
        language='python',
    )
    return kernels_list

def make_kernels_url(kernels_list):
    kernels_url = ''
    kernels_url_2 = ''
    i = 0
    for kernel_info in kernels_list:
        title = getattr(kernel_info, 'title')
        url = getattr(kernel_info, 'ref')
        if i <= 8:
            kernels_url += '*{}\n'.format(title)
            kernels_url += 'url : https://www.kaggle.com/{}\n'.format(url)
        else:
            kernels_url_2 += '*{}\n'.format(title)
            kernels_url_2 += 'url : https://www.kaggle.com/{}\n'.format(url)
        i += 1
    logger.debug('Get {} kernels'.format(len(kernels_list)))

    return kernels_url, kernels_url_2

def post_line(message):
    message = '\n{}'.format(message)

    headers = {
        'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN
    }
    payload = {
        'message': message
    }

    try:
        requests.post('https://notify-api.line.me/api/notify',
                      data=payload, headers=headers)
        logger.debug('Post LINE')
    except Exception as e:
        logger.error(e)


def main():
    time_now = get_time_now()
    kernels_list = get_kernels_list()
    kernels_list_2 = get_kernels_list_2()
    kernels_url, kernels_url_2 = make_kernels_url(kernels_list)
    hot_url, hot_url_2 = make_kernels_url(kernels_url_2)

    post_line(message='順位順')
    post_line(message=kernels_url)
    post_line(message=kernels_url_2)

    post_line(message='ホットな奴ら')
    post_line(message=hot_url)
    post_line(message=hot_url_2)

    post_line(message='更新終了：いざ勉強')
    post_line(message=time_now)

if __name__ == "__main__":
    main()

