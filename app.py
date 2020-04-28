from bs4 import BeautifulSoup
import requests
import json

MAIN_DOMAIN = 'https://www.vaqueiro.pt'
MAIN_URI = '/receitas/carne?recipes=0'

def get_data(uri):
    # find article detail
    r = requests.get(MAIN_DOMAIN + uri)
    soup = BeautifulSoup(r.text, "lxml")

    new_item = {}
    new_item["title"] = soup.find("h1", {'class': 'col-xs-12 col-md-8 field-title'}).text
    new_item["cooktime"] = soup.find("span", {'class': 'recipe-specs-value field-cooktime'}).text
    new_item["preparationtime"] = soup.find("span", {'class': 'recipe-specs-value field-preparationtime'}).text
    new_item["servings"] = soup.find("span", {'class': 'recipe-specs-value field-servings'}).text
    new_item["ingredients"] = soup.find("div", {'class': 'check-list field-ingredientstext'}).text
    new_item["instructions"] = soup.find("div", {'class': 'field-instructionstext'}).text

    return new_item


def crawl_site():
    result = []

    # find articles
    r = requests.get(MAIN_DOMAIN + MAIN_URI)

    # json_data = {
    #     "category": "",
    #     "range": "13",
    #     "page": "1",
    #     "theme": "",
    #     "type": ""
    # }
    # r = requests.post(url, json=json_data)

    soup = BeautifulSoup(r.text, "lxml")
    item_links = soup.find("ul", {'class': 'items'})

    for item in item_links.findAll('a'):
        new_item = {}

        # find title
        title = item.text

        # find url
        url = item['href']

        # data from url
        data = get_data(url)

        print(data)

        # # looping through article link
        # for idx, news in enumerate(item_links):
        #     news_dict = {}
        #
        #     # find news title
        #     title_news = news.find('a', {'class': 'article__link'}).text
        #
        #     # find urll news
        #     url_news = news.find('a', {'class': 'article__link'}).get('href')
        #
        #     # find news content in url
        #     req_news = requests.get(url_news)
        #     soup_news = BeautifulSoup(req_news.text, "lxml")
        #
        #     # find news content
        #     news_content = soup_news.find("div", {'class': 'read__content'})
        #
        #     # find paragraph in news content
        #     p = news_content.find_all('p')
        #     content = ' '.join(item.text for item in p)
        #     news_content = content.encode('utf8', 'replace')

        # wrap in dictionary
        # new_item['url'] = url
        # new_item['title'] = title

        result.append(data)

    return result

crawl = crawl_site()

with open("carne.json", "w") as f:
    json.dump(crawl, f)
