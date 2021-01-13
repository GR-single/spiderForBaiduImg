import requests
import re
import os

url = 'http://image.baidu.com/search/acjson'
keyword = input('关键词:')
wenjianjia = input('文件夹名字:')
wenjianqianzhui = input('文件前缀:')
startPage = int(input('起始页码:'))
goalNum = int(input('目标数量:'))
if not os.path.exists(wenjianjia):
    os.mkdir(wenjianjia)
headers={
    'user-agent':'edge',
    'connection':'keep-alive',
    'host':'image.baidu.com'
}
p = {
'tn':'resultjson_com',
'ipn':'rj',
'ct':'201326592',
'is':'',
'fp':'result',
'queryWord':keyword,
'cl':2,
'lm':-1,
'ie':'utf-8',
'oe':'utf-8',
'adpicid':'',
'st':'',
'z':'',
'ic':'',
'hd':'',
'latest':'',
'copyright':'',
'word':keyword,
's':'',
'se':'',
'tab':'',
'width':'',
'height':'',
'face':'',
'istype':'',
'qc':'',
'nc':1,
'fr':'',
'expermode':'',
'force':'', 
'pn':30,
'rn':30
}
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}
char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
char_table = {ord(key): ord(value) for key, value in char_table.items()}

def jieMa(prestr):
    realstr = ''
    for key, value in str_table.items():
        prestr = prestr.replace(key, value)
    realstr=prestr.translate(char_table)
    return realstr

def zhaoDX(wenjianjia,wenjianqianzhui):

    filenames = os.listdir(wenjianjia)
    print(len(filenames))

    maxIndex = 0
    for i in filenames:
        if i[:len(wenjianqianzhui)+1] == wenjianqianzhui+'_':
            if int(i[len(wenjianqianzhui)+1:i.find('.')]) > maxIndex:
                maxIndex = int(i[len(wenjianqianzhui)+1:i.find('.')])

    minIndex = maxIndex
    for i in filenames:
        if i[:len(wenjianqianzhui)+1] == wenjianqianzhui+'_':
            if int(i[len(wenjianqianzhui)+1:i.find('.')]) < minIndex:
                minIndex = int(i[len(wenjianqianzhui)+1:i.find('.')])

    m = [minIndex,maxIndex]
    return m

page = 0
urlList = []
while (page*30 < goalNum) and (len(urlList) < goalNum):
    p['pn'] = (page+startPage-1)*30
    try:
        r = requests.get(url,headers=headers,params=p)
        print(r.status_code)
        data = r.json()['data']
        for info in data:
            jiBenXinXi = []
            jiBenXinXi.append(info['type'])
            jiBenXinXi.append(jieMa(info['objURL']))
            urlList.append(jiBenXinXi)
            if len(urlList) >= goalNum:
                break
    except:
        print('获取url出错')
        pass
    page += 1
print('图片链接数:',len(urlList))
startIndex = zhaoDX(wenjianjia=wenjianjia,wenjianqianzhui=wenjianqianzhui)[1]+1
jiXu = input('确定下载吗(y/n):')

i = startIndex
if jiXu == 'y':
    zhuangTaiMa = 200
    for urlInfo in urlList:
        try:
            pr = requests.get(urlInfo[1],timeout=10)
            zhuangTaiMa = pr.status_code
            pr.raise_for_status()
            path = './'+wenjianjia+'/'
            filename = wenjianqianzhui+'_'+str(i)+'.'+urlInfo[0]
            with open(path+filename,'wb') as f:
                f.write(pr.content)
                i += 1
        except:
            print('failed:',zhuangTaiMa,urlInfo[1])
            print('get:',i - startIndex)
            pass

print(i - startIndex,'finished')