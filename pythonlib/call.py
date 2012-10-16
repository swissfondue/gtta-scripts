# -*- coding: utf-8 -*-

import subprocess
import os

try:
    from subprocess import check_output
except ImportError:
    def check_output(*args, **kwargs):
        out, err = subprocess.Popen(
            *args,
            stdout=subprocess.PIPE,
            **kwargs
        ).communicate()
        return (out or '') + (err or '')


def call(cmd):
    """
    Calls command and returns (Success: Bool, output)
    """
    try:
        return True, check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        return True, err.output
    except OSError as err:
        return False, ''


def cd(path):
    """
    Returns directory changing ContextManager instance
    """
    class DirChanger(object):

        def __enter__(self):
            self.cwd = os.getcwd()
            os.chdir(path)

        def __exit__(self, ex, *args):
            return ex == None

    return DirChanger()
