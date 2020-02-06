#fixes the url based on two different styles of url
def url_fixer(url):
    if(url.find("page") != -1):
        first = url[0:url.find("?") + 1]
        second = url[url.find("id="):]
        return [(first + second),1]
    return [url,0]
