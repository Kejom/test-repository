import requests
import bs4


def pagescheck(page):
    content = requests.get(page[1])
    soup = bs4.BeautifulSoup(content.text, 'html.parser')
    body = soup.find('body')
    pagelength = 0
    for string in body.strings:
        pagelength += len(string)
    return {"pageid": page[0],"url": page[1], "length": pagelength}
