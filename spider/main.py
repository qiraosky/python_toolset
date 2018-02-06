import urlreader.browserReader as reader

url = "https://www.baidu.com"
status,text=reader.readText(url)

print status
print text