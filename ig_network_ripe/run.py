# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from core.error import InvalidTarget


class IG_Network_Ripe(Task):
    """
    Get ripe inetnums
    """
    target = ''

    def _get_soup(self, session, data):
        """
        Getting soup object from post request
        """
        return BeautifulSoup(
            session.post(
                'https://apps.db.ripe.net/search/full-text.html',
                headers={'User-Agent': 'Mozilla/5.0'},
                data=data
            ).content)

    def _get_state(self, raw):
        """
        Getting javax.faces.ViewState from html page
        """
        return raw.find('input', attrs={'name': 'javax.faces.ViewState', 'type': 'hidden'}).attrMap['value']

    def _collect_data_from_page(self, raw, res):
        """
        Collecting data from page
        """
        form = raw.find('div', attrs={'id': 'form'})
        for tag in form.find('fieldset').findAll('div')[1].findAll('a'):
            text = tag.text.replace('inetnum: ', '')
            res.append(text)
            self._write_result(text)

    def main(self, *args):
        """
        Main function
        """
        if not self.target:
            raise InvalidTarget('No target specified.')

        self._check_stop()

        results = []
        advanced_form_data = {
            'home_search': 'home_search',
            'home_search:searchform_q:': '',
            'home_search:switchMode': 'home_search:switchMode'
        }
        action_form_data = {
            'home_search': 'home_search',
            'home_search:doSearch': 'Search',
            'home_search:searchform_q': self.target,
            'home_search:searchTypeSubview:typeSelectBox': '1',
            'home_search:advancedSearch:selectObjectType': 'inetnum',
        }
        page_form = {
            'resultsView:paginationView:paginationForm': 'resultsView:paginationView:paginationForm',
            'resultsView:paginationView:paginationForm:main:last:last': '>>'
        }
        session = requests.Session()

        # first visit on the site (get javax.faces.ViewState)
        soup = self._get_soup(session, {})
        advanced_form_data.update({'javax.faces.ViewState': self._get_state(soup)})

        # select Advanced Search
        soup = self._get_soup(session, advanced_form_data)
        action_form_data.update({'javax.faces.ViewState': self._get_state(soup)})

        # get first page of results
        soup = self._get_soup(session, action_form_data)
        page_form.update({'javax.faces.ViewState': self._get_state(soup)})

        # collect data from first page
        self._collect_data_from_page(soup, results)

        # go to last page
        soup = self._get_soup(session, page_form)
        page_form['javax.faces.ViewState'] = self._get_state(soup)

        # collect data from current page
        self._collect_data_from_page(soup, results)

        # collect data from prev pages
        current = int(soup.find('span', attrs={'id': 'current'}).text)
        del page_form['resultsView:paginationView:paginationForm:main:last:last']
        while current > 2:
            current -= 1
            # find link to previous page in paginator
            paginator = soup.find('form', attrs={'id': 'resultsView:paginationView:paginationForm'})
            for page_link in paginator.findAll('input', attrs={'type': 'submit'}):
                page_link_val = page_link.attrMap['value']
                if page_link_val == unicode(current):
                    page_link_name = page_link.attrMap['name']
                    page_form.update({page_link_name: page_link_val})
                    break
            # get previous page of results
            soup = self._get_soup(session, page_form)
            if page_link_name in page_form.keys():
                del page_form[page_link_name]
            page_form['javax.faces.ViewState'] = self._get_state(soup)
            # collect data from previous page
            self._collect_data_from_page(soup, results)

        self._check_stop()

        if len(results) == 0:
            self._write_result('No RIPE records.')

    def test(self):
        """
        Test function
        """
        self.target = "clariant"
        self.main()

execute_task(IG_Network_Ripe)