# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from core.error import NoHostName


class IG_Network_Ripe(Task):
    """
    Get ripe inetnums
    """

    def main(self, *args):
        """
        Main function
        """
        if not self.term:
            raise NoHostName('No term specified.')

        self._check_stop()

        def _get_state(raw):
            """
            Getting javax.faces.ViewState from html page
            """
            return raw.find('input', attrs={'name': 'javax.faces.ViewState', 'type': 'hidden'}).attrMap['value']

        def _collect_data_from_page(raw):
            """
            Collecting data from page
            """
            form = raw.find('div', attrs={'id': 'form'})
            for tag in form.find('fieldset').findAll('div')[1].findAll('a'):
                results.append(tag.text.replace('inetnum: ', ''))

        results = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        advanced_form_data = {
            'home_search': 'home_search',
            'home_search:searchform_q:': '',
            'home_search:switchMode': 'home_search:switchMode'
        }
        action_form_data = {
            'home_search': 'home_search',
            'home_search:doSearch': 'Search',
            'home_search:searchform_q': 'clariant',
            'home_search:searchTypeSubview:typeSelectBox': '1',
            'home_search:advancedSearch:selectObjectType': 'inetnum',
        }
        page_form = {
            'resultsView:paginationView:paginationForm': 'resultsView:paginationView:paginationForm',
            'resultsView:paginationView:paginationForm:main:last:last': '>>'
        }
        session = requests.Session()

        # first visit on the site (get javax.faces.ViewState)
        soup = BeautifulSoup(
            session.post(
                'https://apps.db.ripe.net/search/full-text.html',
                headers=headers,
                data={}
            ).content)
        advanced_form_data.update({'javax.faces.ViewState': _get_state(soup)})

        # select Advanced Search
        soup = BeautifulSoup(
            session.post(
                'https://apps.db.ripe.net/search/full-text.html',
                headers=headers,
                data=advanced_form_data
            ).content)
        action_form_data.update({'javax.faces.ViewState': _get_state(soup)})

        # get first page of results
        soup = BeautifulSoup(
            session.post(
                'https://apps.db.ripe.net/search/full-text.html',
                headers=headers,
                data=action_form_data
            ).content)
        page_form.update({'javax.faces.ViewState': _get_state(soup)})

        # go to last page
        soup = BeautifulSoup(
            session.post(
                'https://apps.db.ripe.net/search/full-text.html',
                headers=headers,
                data=page_form
            ).content)
        page_form['javax.faces.ViewState'] = _get_state(soup)

        # collect data from current page
        _collect_data_from_page(soup)

        # collect data from prev pages
        current = int(soup.find('span', attrs={'id': 'current'}).text)
        del page_form['resultsView:paginationView:paginationForm:main:last:last']
        while current > 1:
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
            soup = BeautifulSoup(
                session.post(
                    'https://apps.db.ripe.net/search/full-text.html',
                    headers=headers,
                    data=page_form
                ).content)
            if page_link_name in page_form.keys():
                del page_form[page_link_name]
            page_form['javax.faces.ViewState'] = _get_state(soup)
            # collect data from previous page
            _collect_data_from_page(soup)

        self._check_stop()

        if len(results) == 0:
            self._write_result('No RIPE records.')
        else:
            # begin by first page
            results.reverse()
            for res in results:
                self._write_result(res)

    def test(self):
        """
        Test function
        """
        self.term = "clariant"
        self.main()

execute_task(IG_Network_Ripe)