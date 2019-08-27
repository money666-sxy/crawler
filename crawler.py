import requests
import re
import urllib


url = "https://m.weibo.cn/api/container/getIndex"
#请求的url

headers = {
    "Host": "m.weibo.cn",
    "Referer": "https://m.weibo.cn/u/1739928273",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "Accept":'application/json, text/plain, */*',
    "X-Requested-With":"XMLHttpRequest",
}
#请求头

params = {
          "type": "uid",
          "value": "1739928273",
          "containerid": "1076031739928273",
          "page": "1"}
#请求携带的参数

for i in range(10):
    params['page'] = str(i)
    res = requests.get(url,headers=headers,params=params)
    cards  = res.json().get("data").get("cards")
    #获取carads下的所有项

    for card in cards:
        if card.get("card_type") == 9:
            text = card.get("mblog").get("text")
            # kw = urllib.request.quote(text)
            # old_kw = re.sub("%0A","",kw)
            # new_kw = urllib.request.unquote(old_kw)
            # %0A  这串数字对应的就是这个回车字符
            pattern = re.compile(r"<.*?>|转发微博|查看图片")
            #这里就是把<>符号内的都匹配出来
            text = re.sub(pattern,"",text)
            print(text)
