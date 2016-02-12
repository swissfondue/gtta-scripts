# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Network_Ripe(Task):
    """
    Get ripe inetnums
    """
    target = ""
    results = []

    def _get_soup(self, session, data):
        """
        Get soup object from post request
        """
        content = session.post(
            "https://apps.db.ripe.net/search/full-text.html",
            headers={"User-Agent": "Mozilla/5.0"},
            data=data
        ).content

        return BeautifulSoup(content)

    def _get_state(self, raw):
        """
        Get javax.faces.ViewState from html page
        """
        tag = raw.find("input", attrs={"name": "javax.faces.ViewState", "type": "hidden"})
        return tag.get("value") if tag else None

    def _collect_data_from_page(self, raw):
        """
        Collect data from page
        """
        try:
            a_tags = raw.find("div", attrs={"id": "results"}).findAll("a")
        except:
            return

        for tag in a_tags:
            text = tag.text.replace("inetnum: ", "").replace(" ", "")

            if text not in self.results:
                self.results.append(text)
                self._write_result(text)

    def main(self, *args):
        """
        Main function
        """
        advanced_form_data = {
            "home_search": "home_search",
            "home_search:searchform_q:": "",
            "home_search:switchMode": "home_search:switchMode"
        }

        action_form_data = {
            "home_search": "home_search",
            "home_search:doSearch": "Search",
            "home_search:searchform_q": self.target,
            "home_search:advancedSearch:typeSelectBox": "1",
            "home_search:advancedSearch:selectObjectType": "inetnum",
        }

        page_form = {
            "resultsView:paginationView:dpaginationForm": "resultsView:paginationView:dpaginationForm",
            "resultsView:paginationView:dpaginationForm:main:last:last": ">>"
        }

        session = requests.Session()

        # first visit the site (get javax.faces.ViewState)
        soup = self._get_soup(session, {})
        advanced_form_data.update({"javax.faces.ViewState": self._get_state(soup)})

        # select Advanced Search
        soup = self._get_soup(session, advanced_form_data)
        action_form_data.update({"javax.faces.ViewState": self._get_state(soup)})

        # get first page of results
        soup = self._get_soup(session, action_form_data)
        page_form.update({"javax.faces.ViewState": self._get_state(soup)})

        # collect data from first page
        self._collect_data_from_page(soup)

        # go to last page
        soup = self._get_soup(session, page_form)
        page_form["javax.faces.ViewState"] = self._get_state(soup)

        # collect data from current page
        self._collect_data_from_page(soup)

        # collect data from prev pages
        try:
            current = soup.find("span", attrs={"id": "current"}).text
            current = int(current.strip().replace("[", "").replace("]", ""))
        except:
            return

        del page_form["resultsView:paginationView:dpaginationForm:main:last:last"]

        while current > 2:
            current -= 1

            # find link to previous page in paginator
            paginator = soup.find("form", attrs={"id": "resultsView:paginationView:dpaginationForm"})

            if paginator:
                for page_link in paginator.findAll("input", attrs={"type": "submit"}):
                    page_link_val = page_link.get("value")

                    if page_link_val == unicode(current):
                        page_link_name = page_link.get("name")
                        page_form.update({page_link_name: page_link_val})

                        break

            # get previous page of results
            soup = self._get_soup(session, page_form)

            if page_link_name in page_form.keys():
                del page_form[page_link_name]

            page_form["javax.faces.ViewState"] = self._get_state(soup)

            self._collect_data_from_page(soup)

    def test(self):
        """
        Test function
        """
        self.target = "clariant"
        self.main()

execute_task(IG_Network_Ripe)
