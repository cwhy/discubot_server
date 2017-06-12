# coding=utf8
import requests

# KEY = '8edce3ce905a4c1dbb965e6b35c3834d'
KEY = 'bbac044c91af490ca7cf197bae3d089b'


def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data, timeout=3.14).json()

        result = ''
        if r['code'] == 100000:
            result = r['text'].replace('<br>', '  ')
            result = result.replace(u'\xa0', u' ')
        elif r['code'] == 200000:
            result = r['url']
        elif r['code'] == 302000:
            for k in r['list']:
                result = result + u"【" + k['source'] + u"】 " +\
                    k['article'] + "\t" + k['detailurl'] + "\n"
        else:
            result = r['text'].replace('<br>', '  ')
            result = result.replace(u'\xa0', u' ')

        return result
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return
