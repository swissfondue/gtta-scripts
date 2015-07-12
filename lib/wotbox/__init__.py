# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser


class Wotbox(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'http://www.wotbox.com'
    STATIC_PATH = '/url?j=1&l=UvqjX2rTnAB5&g=765566099'

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('a', attrs={'rel': 'nofollow'})
        for tag in tags:
            try:
                v = tag.get('onclick')[11:-3]
                redirect_path = self.STATIC_PATH + ('&v=%s' % v)
                redirect_script = self._get_soup(path=redirect_path)
                string = redirect_script.script.text.split('\n')[1]
                self.results.add(string[7:-3])
            except:
                continue

    def _extract_next_link(self, soup):
        """
        Exctract next link
        :param soup:
        :return:
        """
        next_link = None
        paginator = soup.find('td', attrs={'class': 'prevnext'})
        if paginator:
            next_link = filter(lambda x: not x.text == 'Next', paginator.findAll('a'))[0]
        return next_link

    def process(self):
        """
        Get results by target from source
        :return:
        """
        # get form params
        soup = self._get_soup()

        params = {
            'q': self.target,
            'la': soup.find('input', attrs={'name': 'la'}),
            'gl': soup.find('input', attrs={'name': 'gl'}),
            'j': soup.find('input', attrs={'id': 'j1'}),
        }

        # get soup with redirect and parse it
        path = '/search?'
        soup = self._get_soup(path=path, params=params)
        string = soup.script.text.split('\n')[1]

        # use it
        soup = self._get_soup(path=string[7:-3])
        self._collect_results_from_soup(soup)

        next_link = self._extract_next_link(soup)

        while next_link:
            next_url = next_link.get('href')

            soup = self._get_soup(path='/' + next_url)
            self._collect_results_from_soup(soup)

            next_link = self._extract_next_link(soup)

        return self.results