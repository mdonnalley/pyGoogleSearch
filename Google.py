from time import sleep as wait
from bs4 import BeautifulSoup
import requests
import collections
import re

__author__ = 'donnalley'


class Google(object):
    def __init__(self, query='hello world', num=10, start=0, sleep=True, recent=None, pages=1):
        self.query = '+'.join(query.split(' '))
        self.num = num
        self.start = start
        self.sleep = sleep
        self.recent = recent
        self.pages = pages
        self.headers = {'user-agent': 'Mozilla/5.0'}
        self.big_soup = BeautifulSoup("<html><body></body></html>")

    def search(self):
        urls = []
        for page in range(0, self.pages):
            url = UrlGenerator(self.query, self.num, (self.start + (10*page)), self.recent).web_url
            urls.append(url)

        for url in urls:
            if self.sleep:
                wait(1)
            soup = BeautifulSoup(requests.get(url, headers=self.headers).text)
            self.big_soup.body.append(soup.body)

        results = self.scrape_search_result(self.big_soup)
        related_queries = self.scrape_related_queries(self.big_soup)

        raw_total_results = self.big_soup.find('div', attrs={'class': 'sd'}).string
        total_results = int(raw_total_results.replace('About ', '').replace(' results', '').replace(',', ''))

        data = collections.OrderedDict()
        data['source'] = 'google'
        data['expected_num'] = self.num * self.pages
        data['received_num'] = len(results)
        data['first_page_url'] = urls[0]
        data['related_queries'] = related_queries
        data['total_results'] = total_results
        data['results'] = results

        return data

    @staticmethod
    def scrape_search_result(soup):
        results = []
        raw_results = soup.find_all('li', attrs={'class': 'g'})
        for result in raw_results:
            link = result.find('a').get('href')[7:].split('&sa', 1)[0]
            # skip if invalid link
            if link[:4] != 'http':
                continue

            link_text = result.find('a').get_text()
            link_info = result.find('span', attrs={'class': 'st'}).get_text()

            additional_links = dict()

            raw_additional_links = result.find('div', attrs={'class': 'osl'})
            if raw_additional_links is not None:
                for item in raw_additional_links.find_all('a'):
                    additional_link_text = item.get_text()
                    additional_link = item.get('href')[7:].split('&sa', 1)[0]
                    additional_links[additional_link_text] = {'link': additional_link.encode('ascii', errors='ignore'),
                                                              'link_text': link_text.encode('ascii', errors='ignore')}

            links_data = {'link': link.encode('ascii', errors='ignore'),
                          'link_text': link_text.encode('ascii', errors='ignore'),
                          'link_info': link_info.encode('ascii', errors='ignore'),
                          'additional_links': additional_links,
                          }

            results.append(links_data)
        return results

    @staticmethod
    def scrape_related_queries(soup):
        related_queries = []
        raw_related = soup.find_all('p', attrs={'class': '_Bmc'})
        for related in raw_related:
            related_query = related.a.get_text()
            if related_query not in related_queries:
                related_queries.append(related_query)
            else:
                continue
        return related_queries

    def search_news(self):
        urls = []
        for page in range(0, self.pages):
            url = UrlGenerator(self.query, self.num, (self.start + (10*page)), self.recent).news_url
            urls.append(url)

        for url in urls:
            if self.sleep:
                wait(1)
            soup = BeautifulSoup(requests.get(url, headers=self.headers).text)
            self.big_soup.body.append(soup.body)

        results = self.scrape_news_result(self.big_soup)

        raw_total_results = self.big_soup.find('div', attrs={'class': 'sd'}).string
        total_results = int(raw_total_results.replace('About ', '').replace(' results', '').replace(',', ''))

        data = collections.OrderedDict()
        data['source'] = 'google news'
        data['expected_num'] = self.num * self.pages
        data['received_num'] = len(results)
        data['first_page_url'] = urls[0]
        data['total_results'] = total_results
        data['results'] = results

        return data

    @staticmethod
    def scrape_news_result(soup):
        raw_results = soup.find_all('li', attrs={'class': 'g'})
        results = []

        for result in raw_results:
            link = result.find('a').get('href')[7:].split('&sa', 1)[0]
            # skip if invalid link
            if link[:4] != 'http':
                continue

            link_text = result.find('a').get_text().encode('ascii', errors='ignore')
            link_info = result.find('div', attrs={'class': 'st'}).get_text().encode('ascii', errors='ignore')
            raw_source = result.find('span', attrs={'class': 'f'}).get_text().split(' - ')
            source = raw_source[0].encode('ascii', errors='ignore')
            time = raw_source[1].encode('ascii', errors='ignore')

            additional_links = dict()
            raw_additional_links = result.find_all('a')[1:]
            if raw_additional_links is not None:
                for item in raw_additional_links:
                    key = item.get_text().encode('ascii', errors='ignore')
                    if key == '':
                        continue
                    additional_link = item.get('href')[7:].split('&sa', 1)[0]
                    raw_source = item.find_next('span').get_text()
                    if ' - ' in raw_source:
                        raw_source = raw_source.encode('ascii', errors='ignore').split(' - ')
                        source = raw_source[0]
                        time = raw_source[1]
                    else:
                        source = raw_source
                        time = 'NA'
                    additional_links[key] = {'link': additional_link.encode('ascii', errors='ignore'),
                                             'link_text': key.encode('ascii', errors='ignore'),
                                             'source': source.encode('ascii', errors='ignore'),
                                             'time': time.encode('ascii', errors='ignore')}

            links_data = {'link': link.encode('ascii', errors='ignore'),
                          'link_text': link_text.encode('ascii', errors='ignore'),
                          'link_info': link_info.encode('ascii', errors='ignore'),
                          'additional_links': additional_links,
                          'source': source.encode('ascii', errors='ignore'),
                          'time': time.encode('ascii', errors='ignore'),
                          }
            results.append(links_data)
        return results

    def search_scholar(self):
        urls = []
        for page in range(0, self.pages):
            url = UrlGenerator(self.query, self.num, (self.start + (10*page)), self.recent).scholar_url
            urls.append(url)

        for url in urls:
            if self.sleep:
                wait(1)
            soup = BeautifulSoup(requests.get(url, headers=self.headers).text)
            self.big_soup.body.append(soup.body)

        results = self.scrape_scholar_result(self.big_soup)

        data = collections.OrderedDict()
        data['source'] = 'google scholar'
        data['expected_num'] = self.num * self.pages
        data['received_num'] = len(results)
        data['first_page_url'] = urls[0]
        data['results'] = results

        return data

    @staticmethod
    def scrape_scholar_result(soup):
        containers = soup.find_all('div', class_='gs_ri')
        results = []

        for container in containers:
            try:
                link = container.find('a').get('href')
            except (AttributeError, TypeError):
                link = 'No link'
            # skip if invalid link
            if link[:4] != 'http':
                continue

            try:
                title = container.find('h3').a.text.encode('ascii', errors='ignore')
            except AttributeError:
                title = container.find('h3').text.encode('ascii', errors='ignore').replace('[CITATION][C] ', '')

            try:
                excerpt = container.find('div', class_='gs_rs').text.encode('ascii', errors='ignore')
            except AttributeError:
                excerpt = ''

            try:
                year = container.find('div', class_='gs_a').text.encode('ascii', errors='ignore')
                year = re.sub(r'\D', '', year)
                if len(year) != 4:
                    year = 'NA'
            except AttributeError:
                year = 'NA'

            try:
                citations = container.find('div', class_='gs_fl').a.text.encode('ascii', errors='ignore').replace(
                    'Cited by ', '')
                if citations.isdigit() is False:
                    citations = 0
            except AttributeError:
                citations = 0

            links_data = {'link': link.encode('ascii', errors='ignore'),
                          'title': title.encode('ascii', errors='ignore'),
                          'excerpt': excerpt.encode('ascii', errors='ignore'),
                          'year': int(year),
                          'citations': int(citations)
                          }

            results.append(links_data)
        return results


class UrlGenerator(Google):
    def __init__(self, query='hello world', num=10, start=0, recent=None):
        Google.__init__(self, query, num, start, recent)
        self.num = str(self.num)
        self.start = str(self.start)

    # https://www.google.com/search?q=hello+world&num=3&start=0
    @property
    def web_url(self):
        url = 'https://www.google.com/search?q=' + self.query + '&num=' + self.num + '&start=' + self.start
        if self.recent in ['h', 'd', 'w', 'm', 'y']:
            url += '&tbs=qdr:' + self.recent
        return url

    # https://www.google.co.in/search?q=hello+world&tbm=nws#q=hello+world&tbas=0&tbm=nws
    @property
    def news_url(self):
        url = 'https://www.google.com/search?q=' + self.query + '&num=' + self.num + '&start=' + self.start
        url += '&tbm=nws#q=' + self.query + '&tbas=0&tbs=sbd:1&tbm=nws'
        if self.recent in ['h', 'd', 'w', 'm', 'y']:
            url += '&tbs=qdr:' + self.recent
        return url

    # https://scholar.google.com/scholar?&q=hello+world&num=10&start=0
    @property
    def scholar_url(self):
        url = 'https://scholar.google.com/scholar?&q=' + self.query + '&num=' + self.num + '&start=' + self.start
        return url
