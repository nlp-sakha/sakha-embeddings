import requests
from bs4 import BeautifulSoup
from config_to_parser import BASE_URL_EDERSAAS as BASE_URL

STOP_PHRASES = ['WhatsApp нөҥүө сонуҥҥун ыыт',
                '\t\t\t\t\t\t\t\t\t\tСайт матырыйаалларын ааптар көҥүлэ суох ылар бобуллар.']

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

        main_section = ''
        for div in soup.find_all('div', {'class': 'media-materials clearfix'}):
            main_section += str(div)

        link_text = []

        soup1 = BeautifulSoup(main_section)

        for a in soup1.find_all('a', href=True):
            link_text.append(a['href'])

        link_text = list(set(link_text))

        for links in link_text:
            page = requests.get(links)
            if page.status_code == 200:
                soup = BeautifulSoup(page.text)
                content = soup.find('div', {'class': 'post-text clearfix'}).text
                content_in_list = content.split('\n')
                x = len(content_in_list)
                # deleting stop phrases
                for phrase in STOP_PHRASES:
                    if phrase in content_in_list: content_in_list.remove(phrase)
                del_elem = 3
                while del_elem <= 7:
                    del content_in_list[x - del_elem]
                    del_elem += 1
                    if x - del_elem == 0: break
                content = ' '.join(content_in_list)
                text_file.write(content + '\n')

        start_count += 1

        if start_count % 2 == 0:
            print(start_count)

    text_file.close()

    counter = (start_count - real_start_count) * 10

    return counter
