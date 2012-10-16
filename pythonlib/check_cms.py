# -*- coding: utf-8 -*-

import os
import call

CMS = (
    'drupal',
    'wordpress',
    'joomla',
    'mambo'
)

CMS_EXPLORER_PATH = os.path.join(
    os.path.dirname(__file__), 'cms-explorer')

def _call_cms_explorer(url, cms):
    """
    Call CMS explorer
    """
    return call.call([
        './cms-explorer.pl',
        '-url', url,
        '-type', cms,
        '-verbosity', '1'
    ])

def get_cms_type(url):
    """
    Returns (
        success/failure of CMS-Explorer call: bool,
        type of CMS for url: string
    )
    """
    with call.cd(CMS_EXPLORER_PATH):
        for cms in CMS:
            res, out = _call_cms_explorer(url, cms)

            if not res:
                return (False, '')

            if out.find('Installed:') >= 0:
                return (True, cms)

    return (True, 'Unknown type')

if __name__ == '__main__':
    print get_cms_type('http://www.ubuntu.com')
