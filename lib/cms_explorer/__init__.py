# -*- coding: utf-8 -*-

import os
from core import call

_CMS_LIST = (
    "drupal",
    "wordpress",
    "joomla",
    "mambo"
)

_CMS_EXPLORER_PATH = os.path.join(os.path.dirname(__file__), "cms-explorer")


def get_cms_type(url):
    """
    Returns (
        success/failure of CMS-Explorer call: bool,
        type of CMS for url: string
    )
    """
    with call.cd(_CMS_EXPLORER_PATH):
        for cms in _CMS_LIST:
            res, out = call.call([
                "perl",
                "cms-explorer.pl",
                "-url", url,
                "-type", cms,
                "-verbosity", "1"
            ])

            if not res:
                return False, ""

            if out.find("Installed:") >= 0:
                output = "%s Detected\n%s" % ( cms.capitalize(), out )
                return True, output

    return True, "Nothing found."

if __name__ == "__main__":
    print get_cms_type("http://www.ubuntu.com")
