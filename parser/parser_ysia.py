import requests
from bs4 import BeautifulSoup
from config_to_parser import BASE_URL_YSIA as BASE_URL


def get_html(url):
    r = requests.get(url)
    return r.text


def get_last_page(html):
    soup = BeautifulSoup(html, "lxml")
    the_last_page = soup.find('div', class_='page-nav td-pb-padding-side').find_all('a', class_='last')[0].get('href')
    last_page = int(the_last_page.split('/')[-2])
    return last_page


def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")
    news_url = soup.find_all('a', class_='comment-count')
    url = []
    for add in news_url:
        try:
            url.append(add.get('href'))
        except:
            url.append('')
    return url


def get_article_content(url):
    page = requests.get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "lxml")
        try:
            content = soup.find('div', class_ ='td-post-content').text
            return content
        except Exception as exc:
            print(exc)
    else:
        return None


def parser(start_count, finish_count, output='parser_output.txt', print_each=2):
    last_page = get_last_page(get_html(BASE_URL))
    count = 0
    for i in range(1, last_page + 1):
        GEN_URL = BASE_URL+'page/'+str(i)
        html = get_html(GEN_URL)
        urls = get_page_data(html)

        for url in urls:
            text_file = open(output,'a')
            content = get_article_content(url)
            if content is not None:
                text_file.write(content+'\n')
            text_file.close()
            count += 1
        print(count)
    return count