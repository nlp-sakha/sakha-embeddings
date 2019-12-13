import requests
from bs4 import BeautifulSoup
from config_to_parser import BASE_URL_ILTYMEN as BASE_URL


def get_html(url):
    r = requests.get(url)
    return r.text


def get_urls_rubriki(html):
    soup = BeautifulSoup(html, "lxml")
    the_urls_rubriki = str(soup.find_all('div', class_='entry')).split('ахсаана')[1]
    urls_rubriki = the_urls_rubriki.split('"')[1:][::2]
    return urls_rubriki


def get_urls_articles(html):
    soup = BeautifulSoup(html, "lxml")
    the_urls_articles = soup.find('div', class_='col-md-12').find_all('a')[::8]
    urls_articles = str(the_urls_articles).split('"')[1:][::2]
    return urls_articles


def get_article_content(url):
    page = requests.get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "lxml")
        try:
            content = soup.find('div', class_ ='entry').text
            return content
        except Exception as exc:
            print(exc)
    else:
        return None


def parser(start_count, finish_count, output='parser_output.txt', print_each=2):
    urls_rubriki = get_urls_rubriki(get_html(BASE_URL))
    print(urls_rubriki)
    count = 0
    for i in urls_rubriki:
        html = get_html(i)
        urls = list(filter(lambda x: 'http' in x, get_urls_articles(html)))
        print(urls)

        for url in urls:
            text_file = open(output,'a')
            content = get_article_content(url)
            if content is not None:
                text_file.write(content+'\n')
            text_file.close()
            count += 1
        print(count)
    return count

"""
if __name__ == '__main__':
    parsed = parser(output='parser_output.txt')
    print('RESULT: {} articles parsed from iltymen'.format(parsed))
"""