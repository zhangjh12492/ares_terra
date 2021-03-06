import urllib
import requests

from urllib import request
import urllib.request
from bs4 import BeautifulSoup
import multiprocessing
import time
from uaa.member_register import urllib_create_mem
from hermes.agent_r_com import urllib_month_bill_list
import os

root_path = os.getcwd()
uaa_root_path = root_path[0:root_path.find('ares_terra')] + 'ares_terra%suaa' % os.sep
file = open(uaa_root_path + '{}conf{}valid_proxy_ip.txt'.format(os.sep, os.sep), 'a')


def getProxyIp():
    proxy = []
    for i in range(1, 3):
        print(i)
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Ubuntu Chromium/44.0.2403.89 '
                                'Chrome/44.0.2403.89 '
                                'Safari/537.36'}
        req = urllib.request.Request(url='http://www.xicidaili.com/nt/{0}'.format(i), headers=header)
        r = urllib.request.urlopen(req)
        soup = BeautifulSoup(r, 'html.parser', from_encoding='utf-8')
        table = soup.find('table', attrs={'id': 'ip_list'})
        tr = table.find_all('tr')[1:]
        # 解析得到代理ip的地址，端口，和类型
        for item in tr:
            tds = item.find_all('td')
            temp_dict = {}
            kind = "{0}:{1}".format(tds[1].get_text().lower(), tds[2].get_text())
            proxy.append(kind)
    return proxy


def brash(proxy_dict):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Ubuntu Chromium/44.0.2403.89 '
                            'Chrome/44.0.2403.89 '
                            'Safari/537.36'}
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy_dict})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url="https://www.baidu.com/", headers=header)
        urllib.request.urlopen(req)
    except Exception as e:
        print("failed")
    else:
        print("--> successful", proxy_dict)
        file.write(proxy_dict+"\n")
        # proxy_id = {"http": "http://" + proxy_dict}
        # try:
        #     # urllib_create_mem(proxy_id)
        #     urllib_month_bill_list(proxy_id)
        #
        # except Exception as err:
        #     print('--> create member error : ' + str(err))
    return None


from hermes.config import Config
from utils.request_util import get_token

if __name__ == '__main__':
    Config.env = 'prod'
    token = get_token('plat')
    i = 0
    t = 0
    proxies = getProxyIp()
    # 为了爬取的代理ip不浪费循环5次使得第一次的不能访问的ip尽可能利用
    for i in range(5):
        i += 1
        # 多进程代码开了16个进程
        pool = multiprocessing.Pool(processes=4)
        results = []
        for i in range(len(proxies)):
            results.append(pool.apply_async(brash, (proxies[i],)))
        # for i in range(len(proxies)):
        # results[i].get()
        pool.close()
        pool.join()
    file.close()
