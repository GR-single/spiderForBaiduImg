import os

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
zuixiao,zuida = zhaoDX('CIJI_IMG','HS')
print(zuixiao,zuida)