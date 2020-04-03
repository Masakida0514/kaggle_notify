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


def get_kernels_url():
    api = KaggleApi()
    api.authenticate()
    kernels_list = api.kernels_list(
        competition=COMPETITION_NAME,
        page_size=20,
        language='python',
        sort_by='scoreAscending'
    )

    now = datetime.datetime.utcnow()
    y = str(now.year)
    m = str(now.month)
    d = str(now.day)
    h = str(now.hour)
    kernels_url = y + '年' + m + '月'+ d + '日' + h + '時の\n'

    for kernel_info in kernels_list:
        title = getattr(kernel_info, 'title')
        url = getattr(kernel_info, 'ref')
        kernels_url += '*{}\n'.format(title)
        kernels_url += 'url : https://www.kaggle.com/{}\n'.format(url)
    logger.debug('Get {} kernels'.format(len(kernels_list)))

    return kernels_url

def post_line(message):
    # message = '\n{}\n{}'.format(COMPETITION_NAME, message)
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


if __name__ == "__main__":
    kernels_url = get_kernels_url()
    post_line(message=kernels_url)