import requests
from bs4 import BeautifulSoup
from config_to_parser import BASE_URL_KYYM as BASE_URL


def last_article_id():
    """
    Return id of last article for web newspaper Kyym
    :return:
    """

    count = 2008
    url = BASE_URL + str(count)
    page_status = requests.get(url).status_code
    stop_page_status = 404

    while page_status != stop_page_status:
        url = BASE_URL + str(count)
        page_status = requests.get(url).status_code
        count += 1

    count -= 2

    return count


def get_article_content(url):
    """
    Get content of one Kyym article by url
    :param url: str, url
    :return: None, if not 200 status code returned
    """
    page = requests.get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text)
        try:
            content = soup.find('section', {'class': 'article-content'}).text
            return content
        except Exception as exc:
            print(exc)


    else:
        return None


def parser(start_count, finish_count, output='parser_output.txt', print_each=2):
    """Parsing articles from kyym newspaper website and writes it to specified output file

    :param start_count: int, starting from this article id
    :param finish_count: int, finishing on this article id
    :param output: str, where to write output
    :param print_each: print process progress for each N article
    :return: int, counter - how many articles parsed
    """

    text_file = open(output, 'a')
    counter = 0
    for i in range(finish_count - start_count):
        idx = start_count + i
        url = "http://kyym.ru/sonunnar/" + str(idx)
        content = get_article_content(url)
        if content is not None:
            text_file.write(content + '\n')
            counter += 1

        if start_count % print_each == 0:
            print(idx)

    text_file.close()

    return counter
