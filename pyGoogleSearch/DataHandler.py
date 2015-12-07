# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re

__author__ = 'donnalley'


class DataHandler:
    def __init__(self, dataframe, get_content=False):
        self.dataframe = dataframe
        self.get_content = get_content
        self.source = dataframe['source']
        if self.source == 'google':
            self.related_queries = self.dataframe['related_queries']

    def grab_links(self):
        links = []
        for item in self.dataframe['results']:
            link = item['link']
            links.append(link)

            if self.source in ['google', 'google news']:
                additional_links = item['additional_links'].values()
                if len(additional_links) > 0:
                    for additional_link in additional_links:
                        # skip if invalid link
                        if additional_link['link'][:4] != 'http':
                            continue
                        links.append(additional_link['link'])
        return links

    def aggregate_data(self):
        if self.source == 'google':
            output_dataframe = get_web_data(self.dataframe, self.get_content)
        elif self.source == 'google news':
            output_dataframe = get_news_data(self.dataframe, self.get_content)
        elif self.source == 'google scholar':
            output_dataframe = get_scholar_data(self.dataframe, self.get_content)
        else:
            raise AttributeError("Invalid source")
        return output_dataframe


# HELPER FUNCTIONS ################################
def encode(list_object):
    output = []
    for item in list_object:
        item = item.encode('utf-8')
        output.append(item)
    return output


def decode(list_object):
    output = []
    for item in list_object:
        item = item.decode()
        output.append(item)
    return output


def get_web_data(datasource, get_content):
    output_dataframe = []
    if get_content:
        headings = ['URL', 'Link Text', 'Link Info', 'Ranking', 'Content']
    else:
        headings = ['URL', 'Link Text', 'Link Info', 'Ranking']
    output_dataframe.append(headings)

    additional_links = []
    for rank, item in enumerate(datasource['results'], 1):
        link = item['link']
        link_text = item['link_text']
        link_info = item['link_info']
        if get_content:
            content = collect_content(link)
            data = [link, link_text, link_info, rank, content]
        else:
            data = [link, link_text, link_info, rank]
        output_dataframe.append(data)

        values = item['additional_links'].values()
        if values:
            for value in values:
                additional_links.append(value)

    for additional_link in additional_links:
        link = additional_link['link']
        link_text = additional_link['link_text']
        if get_content:
            content = collect_content(link)
            data = [link, link_text, 'Additional Link', 'NA', content]
        else:
            data = [link, link_text, 'Additional Link', 'NA']
        output_dataframe.append(data)

    return output_dataframe


def get_news_data(datasource, get_content):
    output_dataframe = []
    if get_content:
        headings = ['URL', 'Link Text', 'Link Info', 'Source', 'Time', 'Ranking', 'Content']
    else:
        headings = ['URL', 'Link Text', 'Link Info', 'Source', 'Time', 'Ranking']
    output_dataframe.append(headings)

    additional_links = []
    for rank, item in enumerate(datasource['results'], 1):
        link = item['link']
        link_text = item['link_text']
        link_info = item['link_info']
        time = item['time']
        source = item['source']
        if get_content:
            content = collect_content(link)
            data = [link, link_text, link_info, source, time, rank, content]
        else:
            data = [link, link_text, link_info, source, time, rank]
        output_dataframe.append(data)

        values = item['additional_links'].values()
        if values:
            for value in values:
                additional_links.append(value)

    for additional_link in additional_links:
        link = additional_link['link']
        link_text = additional_link['link_text']
        source = additional_link['source']
        time = additional_link['time']
        if get_content:
            content = collect_content(link)
            data = [link, link_text, 'Additional Link', source, time, 'NA', content]
        else:
            data = [link, link_text, 'Additional Link', source, time, 'NA']
        output_dataframe.append(data)

    return output_dataframe


def get_scholar_data(datasource, get_content):
    output_dataframe = []
    if get_content:
        headings = ['URL', 'Title', 'Excerpt', 'Citations', 'Year', 'Rank', 'Content']
    else:
        headings = ['URL', 'Title', 'Excerpt', 'Citations', 'Year', 'Rank']
    output_dataframe.append(headings)
    for rank, item in enumerate(datasource['results'], 1):
        link = item['link']
        title = item['title']
        excerpt = item['excerpt']
        citations = item['citations']
        year = item['year']
        if get_content:
            content = collect_content(link)
            data = [link, title, excerpt, citations, year,  rank, content]
        else:
            data = [link, title, excerpt, citations, year,  rank]
        output_dataframe.append(data)
    return output_dataframe


def collect_content(link):
    if '.pdf' in link:
        content = 'Error: PDF'
    else:
        try:
            html = requests.get(link, headers={'user-agent': 'Mozilla/5.0'}).text
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.find_all(text=True)
            content = filter(visible, text)
            content = ' '.join(content)
            content = content.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
            content = clean_html(content)
        except (requests.HTTPError, requests.ConnectionError, ValueError):
            content = 'Error: 404 not found'
    return content


def clean_html(html_text):
    # Remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(<!--\1-->)", "", html_text.strip())
    # Remove html comments. This has to be done before removing regular tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # deal with whitespace
    cleaned = re.sub(r" ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    # elif re.match('<!--.*-->', str(element.encode('ascii', errors='ignore'))):
    elif re.match('<!--.*-->', element):
        return False
    # elif re.match('\n', str(element.encode('ascii', errors='ignore'))):
    elif re.match('\n', element):
        return False
    return True

####################################################
