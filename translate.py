# coding=utf-8
import urllib
import urllib2
import json
import time
import hashlib
import datetime


class YouDaoFanyi:
    def __init__(self, appKey, appSecret):
        self.url = 'https://openapi.youdao.com/api/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",
        }
        self.appKey = appKey  # 应用id
        self.appSecret = appSecret  # 应用密钥
        self.langFrom = 'auto'   # 翻译前文字语言,auto为自动检查
        self.langTo = 'auto'     # 翻译后文字语言,auto为自动检查

    def getUrlEncodedData(self, queryText):
        '''
        将数据url编码
        :param queryText: 待翻译的文字
        :return: 返回url编码过的数据
        '''
        salt = str(int(round(time.time() * 1000)))  # 产生随机数 ,其实固定值也可以,不如"2"
        sign_str = self.appKey + queryText + salt + self.appSecret
        sign = hashlib.md5(sign_str).hexdigest()
        payload = {
            'q': queryText,
            'from': self.langFrom,
            'to': self.langTo,
            'appKey': self.appKey,
            'salt': salt,
            'sign': sign
        }

        # 注意是get请求，不是请求
        data = urllib.urlencode(payload)
        return data

    def parseHtml(self, html):
        '''
        解析页面，输出翻译结果
        :param html: 翻译返回的页面内容
        :return: None
        '''
        data = json.loads(html)
        print '-' * 10
        #print data
        translationResult = data['translation']
        if isinstance(translationResult, list):
            translationResult = translationResult[0]
        #print unicode(translationResult)
        if "basic" in data:
            youdaoResult = "\n".join(data['basic']['explains'])
            #print '有道词典结果'.decode("utf-8")
            print youdaoResult
        print '-' * 10

    def translate(self, queryText):
        htmlname = ".//word//" + queryText + ".html"
        file_output = open(htmlname, "w")
        data = self.getUrlEncodedData(queryText)  # 获取url编码过的数据
        target_url = self.url + '?' + data    # 构造目标url
        request = urllib2.Request(target_url, headers=self.headers)  # 构造请求
        response = urllib2.urlopen(request)  # 发送请求
        html = response.read()
        self.parseHtml(html)    # 解析，显示翻译结果
        file_output.write(html)
        file_output.close()

def get_curr_time():
    t = datetime.datetime.now()
    str_time = ("%04d-%02d-%02d_%02d_%02d_%02d") % (t.year, t.month, t.day, t.hour, t.minute, t.second)
    return str_time

if __name__ == "__main__":
    appKey = '563540997db75bd6'  # 应用id
    appSecret = 'h1dzpEtweTzaz31YtL8K4C13EZHp34h4'  # 应用密钥
    fanyi = YouDaoFanyi(appKey, appSecret)
    
    file_output = open("log.txt", "a+")
    
    L_ok = []
    L_error = []
    
    L_list1 = []
    
    with open("list3.txt", "r") as file_list1:
        
        for line in file_list1:
            line = line.replace("\n", "")
            L_list1.append(line)
    
    count = 1
    for item_line in L_list1:
        print u"以下单词是否认识:"
        print str(count) + "." + item_line, 
        raw_input()
        fanyi.translate(item_line)
        print u"Y or N", 
        feedback = raw_input()
        if (feedback == 'Y' or feedback == "y"):
            L_ok.append(item_line)
        elif (feedback == "N" or feedback == "n"):
            file_output.write(get_curr_time())
            file_output.write("\t")
            file_output.write(item_line)
            file_output.write("\n")
            file_output.flush()
            L_error.append(item_line)
        else:
            file_output.write(get_curr_time())
            file_output.write("\t")
            file_output.write(item_line)
            file_output.write("\n")
            file_output.flush()
            L_error.append(item_line)
        print ""
        count += 1
        
    print (u"认识的单词率为 %f") % (float(len(L_ok)) / float(len(L_list1)))
    print "\n"
    print "\n"
    print u"进行以下错题练习吧:"
    while (len(L_error) > 0):
        
        for item_line in L_error:
            print u"以下单词是否认识:"
            print str(count) + "." + item_line, 
            raw_input()
            fanyi.translate(item_line)
            print u"Y or N", 
            feedback = raw_input()
            if (feedback == 'Y' or feedback == "y"):
                L_error.remove(item_line)
            elif (feedback == "N" or feedback == "n"):
                pass
            print ""
            count += 1
        
        
        
        
        
        
        
        
        
        
        
        
        