# -*- coding: utf-8 -*-

import os
import call

SQID_PATH = os.path.join(os.path.dirname(__file__), 'sqid')

def get_injections(url):
    """
    Returns (
        success/failure of Sql Injection call: bool,
        list of avaible sql injections for url: string
    )
    """
    with call.cd(SQID_PATH):
        res, out = call.call([
            "ruby",
            'sqid.rb',
            '--mode', 'c',
            '--crawl', url,
            '--accept-cookies'
        ])

        if not res:
            return (False, '')

        return (True, out)

if __name__ == '__main__':
    print get_injections('http://realestate.ru:80')
