# -*- coding: utf-8 -*-

from urlparse import urlsplit, parse_qs
import re
from HTMLParser import HTMLParser
from core.crawler import LinkCrawler
from core import Task, execute_task


class FormsParser(HTMLParser):
    """
    Form parser
    """
    form_attributes = dict()

    def __init__(self):
        """
        Constructor
        """
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        """
        Handle start tag
        """
        at = dict(attrs)

        if tag == "form":
            self.form_attributes = dict()
            self.form_attributes["action"] = None
            self.form_attributes["inputs"] = []

            if "action" in at:
                self.form_attributes["action"] = at["action"]

        if tag in ("input", "select"):
            self.form_attributes["inputs"].append(at)


class Params_Craw(Task):
    """
    Complete parameters from forms and urls, using crawler.py
    """
    urls_set = set()
    forms_urls_set = set()
    form_parser = FormsParser()

    FORM_PATTERN = "(?i)<form([^>]+)>(.+?)</form>"
    INPUT_PATTERN = "(?i)<input(.+?)>"

    def collect_unique_urls(self, url):
        """
        Using as callback function for crawler
        """
        self.urls_set.add(url)

    def collect_params(self, url):
        """ Collecting params from link """
        if url not in self.urls_set:
            splitted_url = urlsplit(url)
            query_params = parse_qs(splitted_url[3])

            if query_params:
                self._write_result(url)

                for key, value in query_params.items():
                    self._write_result("\t" + key + "=" + value[0])
                    self._check_stop()

                self._write_result("")

            self.collect_unique_urls(url)

    def collect_form_params(self, page):
        """ If we have on page form, then outputting that form url and params from there"""
        if page["url"] not in self.forms_urls_set:
            self.forms_urls_set.add(page["url"])

            for item in re.finditer(self.FORM_PATTERN, page["content"], re.S):  # Iterate all forms in page content
                self._check_stop()

                self.form_parser.feed(item.group(0))  # Parsing form action and inputs params with Form_Parser
                form_attributes = self.form_parser.form_attributes

                if not form_attributes["action"]:
                    form_attributes["action"] = page["url"]

                self._write_result("Form: " + form_attributes["action"])

                for input_params in form_attributes["inputs"]:  # Iterating all inputs attributes
                    self._check_stop()

                    if "name" in input_params:
                        name = input_params["name"]
                        value = ""

                        if "value" in input_params:
                            value = input_params["value"]

                        self._write_result("\t%s=%s" % (name, value))

                self._write_result("")

    def main(self, *args):
        """
        Main function
        """
        link_crawler = LinkCrawler()
        link_crawler.stop_callback = self._check_stop
        link_crawler.link_callback = self.collect_params
        link_crawler.link_content_callback = self.collect_form_params

        if not self.proto:
            self.proto = "http"

        if self.host:
            target = self.proto + "://" + self.host + "/"
        else:
            target = self.proto + "://" + self.ip + "/"

        link_crawler.process(target)  # Starting recursive process of link crawling on target

        self._check_stop()

        if not self.produced_output:
            self._write_result("No variables found.")

    def test(self):
        """
        Test function
        """
        self.proto = "http"
        self.host = "gtta.demo.stellarbit.com"
        self.main()

execute_task(Params_Craw)