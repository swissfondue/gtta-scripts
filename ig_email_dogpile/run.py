# -*- coding: utf-8 -*-

import re
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from dogpile import DogpileParser


class IG_Email_Dogpile(Task):
    """
    Search emails in pages from Dogpile
    """
    results = []

    def add_emails(self, emails):
        """
        Add collected emails
        """
        for email in emails:
            if email not in self.results:
                self._write_result(email)
                self.results.append(email)

    def main(self, *args):
        """
        Main function
        """
        if self.ip:
            return

        dogpiles = DogpileParser('"@%s"' % self.target).process()

        for dog in dogpiles:
            try:
                req = requests.get(dog, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(req.content)
            except:
                continue

            for a in soup.findAll('a'):
                for attr in a.attrs:
                    if attr[0] == 'href':
                        emails = re.findall(r'[\w\.-]+@[\w\.-]+', attr[1])
                        if emails:
                            self.add_emails(emails)
                        break

            for text in filter(lambda x: '@' in x, soup.findAll(text=True)):
                emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
                self.add_emails(emails)

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Dogpile)
