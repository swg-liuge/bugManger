import urllib.request
import importlib, sys
from html.parser import HTMLParser

tmp = "jiancai"
url = "http://b2b.huangye88.com/chengdu/"+tmp
urlList = [url]
for i in range(2,30):
    urlList.append(url+"/pn"+str(i)+"/")
print(urlList)


def httpHandle(url):
    importlib.reload(sys)
    req = urllib.request.Request(url, headers={
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })
    request = urllib.request.urlopen(req)
    data = request.read()
    response = data.decode("utf-8")
    # print(response)
    # open("/Users/didi/Downloads/response.txt", "w").write(response)
    return response


contactSet = set()


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == "a" and len(attrs) == 3 and attrs[1][0] == "href" and attrs[0][0] == "target" and attrs[2][0] == "rel"\
                and attrs[1][1].endswith("company_contact.html"):
            # print(tag, "====", attrs[0], "=+++", attrs[1], "----",attrs[2])
            contactSet.add(attrs[1][1])


p = MyHTMLParser()
for ur in urlList:
    p.feed(httpHandle(ur))

p.close()
# print(contactSet)


detailList = []


class ContactParser(HTMLParser):

    isUl = False
    isLi = False
    isLabel = False
    # detailList = []

    def handle_starttag(self, tag, attrs):
        if tag == "ul" and len(attrs) == 1 and attrs[0][1] == "con-txt" :
            # print(attrs)
            self.isUl = True
        if tag == "li":
            self.isLi = True
        if tag == "label":
            self.isLabel = True

    def handle_data(self, data):
        if self.isUl and self.isLi and not self.isLabel:
            # print(data)
            detailList.append(data)

    def handle_endtag(self, tag):
        if tag == "ul":
            self.isUl = False
        if tag == "li":
            self.isLi = False
        if tag == "label":
            self.isLabel = False

    # def getDetailList(self):
    #     return self.detailList


c = ContactParser()
print("set  size: ======= ",len(contactSet))
detailFile = open(tmp + ".txt", "a")
for cont in contactSet:
    # print(cont)
    c.feed(httpHandle(cont))
    if len(detailList[1]) == 11:
        for j in range(0,3):
            detailFile.write(detailList[j] + "\t")
        detailFile.write("\n")
    # print(detailList)
    detailList = []
c.close()
detailFile.close()
