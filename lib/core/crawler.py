# -*- coding: utf-8 -*-

import re
import urlparse
import requests


def have_same_base(this, that):
    """
    Have some base
    """
    this = urlparse.urlsplit(this)[1]
    that = urlparse.urlsplit(that)[1]

    return this == that


class LinkCrawler(object):
    """
    URL-redirects crawler
    """
    A_TAG_PATTERN = """(?i)<a([^>]+)>(.+?)</a>"""
    LINK_PATTERN = """href=[\'"]?([^\'" >]+)"""

    def __init__(self, recursive=True):
        """
        Constructor
        """
        self._recursive = recursive

        nop = lambda: None
        skip = lambda arg: None

        self.link_callback = skip
        self.link_content_callback = skip
        self.ext_link_callback = skip
        self.redirect_callback = skip
        self.error_callback = skip
        self.nonhtml_callback = skip
        self.stop_callback = nop

        # external links detection strategy
        self.ext_link_test = have_same_base

    def process(self, url):
        """
        Iterate the external links from url
        """
        cache = set()

        def populate(url):
            try:
                resp = requests.get(url, headers={"User-agent": "Mozilla/5.0"}, verify=False)
            except Exception:
                return

            # handle redirects
            if any(r.status_code in (301, 302) for r in resp.history):
                if self.redirect_callback(url):
                    return

            # handle errors
            if resp.status_code >= 400:
                if self.error_callback("%03d: %s" % (resp.status_code, url)):
                    return

            # handle non-html
            if not resp.headers.get("content-type", "").startswith("text/html"):
                self.nonhtml_callback(url)
                return

            # parse pages
            self.link_content_callback(dict(url=url, content=resp.text))

            for item in re.finditer(self.LINK_PATTERN, resp.text):
                link = urlparse.urljoin(url, item.group(1))

                # populate all parsed link (if not cached)
                if link not in cache:
                    if self.ext_link_test(url, link):
                        cache.add(link)
                        self.link_callback(link)

                        self.stop_callback()  # check for stopping

                        if self._recursive:
                            populate(link)
                    else:
                        self.ext_link_callback(link)

        populate(url)
