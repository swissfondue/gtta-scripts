# -*- coding: utf-8 -*-
import re


def parse_soup(soup):
    """
    Method return collected from soup emails
    :param soup:
    :return:
    """
    emails = set()
    pattern = re.compile(r'[\w\.-]+@[\w\.-]+')

    # looking at links
    for a in soup.findAll('a'):
        try:
            href = filter(lambda x: x[0] == 'href', a.attrs)[0][1]
            emails.update(pattern.findall(href))
        except:
            continue

    # looking at text
    for text in filter(lambda x: '@' in x, soup.findAll(text=True)):
        emails.update(pattern.findall(text))

    return emails