import requests
from bs4 import BeautifulSoup
from config_to_parser import BASE_URL_SAKHA_SIRE as BASE_URL


def parser(start_count, finish_count, output='parser_output.txt', print_each=2):
    """Parsing articles from eder saas newspaper website and writes it to specified output file

    :param start_count: int. start page
    :param finish_count: int, end page
    :param output: str, where to write output
    :param print_each:print process progress for each N article
    :return: int, counter - how many pages parsed

    On Page 10 articles
    """

    text_file = open(output, 'a')
    real_start_count = start_count
    start_count = start_count
    while start_count <= finish_count:
        SITE_URL = BASE_URL + str(start_count)
        page = requests.get(SITE_URL)
        soup = BeautifulSoup(page.text)
        main_section = soup.find('section', {'id': 'content'})
        link_text = []

        for a in main_section.find_all('a', {'class': 'more-link'}, href=True, text=True):
            link_text.append(a['href'])

        link_text = list(set(link_text))

        for links in link_text:
            page = requests.get(links)
            if page.status_code == 200:
                soup = BeautifulSoup(page.text)
                # TODO: add try
                content = soup.find('div', {'class': 'entry clearfix'}).text
                content_in_list = content.split(' ')
                if len(content_in_list) < 3:
                    continue
                # deleting last elements in the list since it generally contains author info
                content_in_list = content_in_list[:-2]
                content = ' '.join(content_in_list)

                text_file.write(content + '\n')

        start_count += 1

        if start_count % 2 == 0:
            print(start_count)

    text_file.close()

    counter = (start_count - real_start_count) * 10

    return counter
