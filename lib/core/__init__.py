# -*- coding: utf-8 -*-

import re
from threading import Thread, Event
from sys import argv, exit, stdout
from os import killpg, getpgrp
from os.path import isdir
from signal import SIGTERM
from socket import inet_aton
from time import sleep
from lxml import etree
from error import NotEnoughArguments, TaskTimeout, NoDataReturned, InvalidTargetFile
from netaddr import IPNetwork, IPRange

SANDBOX_IP = "192.168.66.66"


class ResultTable(object):
    """
    Result table class
    """
    TAG_MAIN = 'gtta-table'
    TAG_ROW = 'row'
    TAG_CELL = 'cell'
    TAG_COLUMNS = 'columns'
    TAG_COLUMN = 'column'

    ATTR_NAME = 'name'
    ATTR_WIDTH = 'width'

    def __init__(self, columns):
        """
        Constructor
        """
        self._columns = columns
        self._rows = []

    def add_row(self, row):
        """
        Add row
        """
        self._rows.append(row)

    def render(self):
        """
        Render to tags
        """
        table = etree.Element(self.TAG_MAIN)
        columns = etree.SubElement(table, self.TAG_COLUMNS)

        for column in self._columns:
            etree.SubElement(columns, self.TAG_COLUMN, name=column['name'], width=unicode(column['width']))

        for row in self._rows:
            row_element = etree.SubElement(table, self.TAG_ROW)

            for cell in row:
                cell_element = etree.SubElement(row_element, self.TAG_CELL)
                cell_element.text = cell

        return etree.tostring(table)


class Task(Thread):
    """
    Base class for all tasks
    """
    DEFAULT_TIMEOUT = 60 * 60 * 24  # 1 Day
    TEST_TIMEOUT = 30   # test task timeout
    DNS_TIMEOUT = 10    # DNS request timeout
    SOCKET_TIMEOUT = 2  # socket timeout
    HTTP_TIMEOUT = 30   # HTTP timeout
    SMTP_TIMEOUT = 10   # SMTP timeout
    PARSE_FILES = True  # read & parse all input files by default
    EXPAND_TARGETS = True  # expand ip networks and ip ranges
    SYSTEM_LIBRARY_PATH = "/opt/gtta/scripts/system/lib"
    USER_LIBRARY_PATH = "/opt/gtta/scripts/lib"

    def __init__(self):
        """
        Constructor
        """
        super(Task, self).__init__()

        self.arguments = None
        self.targets = None
        self.target = None
        self.host = None
        self.ip = None
        self.proto = None
        self.port = None
        self.timeout = None
        self.lang = None
        self.test_mode = False
        self.error = False
        self._stop = Event()
        self._result = None

        self.produced_output = False

    def _check_stop(self):
        """
        Check if thread should be stopped
        """
        if self._stop.isSet():
            raise TaskTimeout

    def _write_result(self, str):
        """
        Write result to result file or print it to output
        """
        if not str:
            return

        self.produced_output = True

        if self._result:
            self._result.write(str.encode('utf-8'))
            self._result.write('\n')
            self._result.flush()

        else:
            print str.encode('utf-8')
            stdout.flush()

    def _expand_targets(self):
        targets = []

        for target in self.targets:
            # IP network
            if re.match('^\d+\.\d+\.\d+\.\d+\/(3[0-2]|2[0-9]{1}|[01]?[0-9])$', target):
                for ip in IPNetwork(target):
                    targets.append('%s' % ip)
            else:
                # IP range
                if re.match('^\d+\.\d+\.\d+\.\d+\-\d+\.\d+\.\d+\.\d+$', target):
                    scope = target.split('-')

                    for ip in IPRange(scope[0], scope[1]):
                        targets.append('%s' % ip)

        self.targets = targets

    def stop(self):
        """
        Thread stop function
        """
        self._stop.set()

    def parse_input(self):
        """
        Parses input arguments
        """
        self.arguments = []

        if len(argv) < 3:
            raise NotEnoughArguments('At least 2 command line arguments should be specified.')

        # parse the first file with hostname or IP
        lines = open(argv[1], 'r').read().split('\n')
        lines = map(lambda x: x.replace('\r', ''), lines)

        if len(lines) < 5:
            raise InvalidTargetFile('Target file should contain at least 5 lines.')

        if not lines[0]:
            raise InvalidTargetFile('Target file should contain either host name or IP address of the target host on the 1st line.')

        self.targets = lines[0].split(',')

        if self.EXPAND_TARGETS:
            self._expand_targets()

        self.proto = lines[1]

        try:
            if lines[2]:
                self.port = int(lines[2])
            else:
                self.port = 0

        except ValueError:
            self.port = 0

        if not lines[3]:
            raise InvalidTargetFile('Target file should contain language name on the 4th line.')

        self.lang = lines[3]

        try:
            if len(lines[4]) > 0:
                self.timeout = int(lines[4])
            else:
                self.timeout = self.DEFAULT_TIMEOUT

        except ValueError:
            self.timeout = self.DEFAULT_TIMEOUT

        # open output file
        self._result = open(argv[2], 'w')

        # parse the remaining arguments
        for arg in argv[3:]:
            if self.PARSE_FILES:
                lines = open(arg, 'r').read().split('\n')
                lines = map(lambda x: x.replace('\r', ''), lines)
                self.arguments.append(lines)

            else:
                self.arguments.append(arg)

    def _get_library_path(self, library):
        """
        Get library path
        """
        path = None

        if isdir("%s/%s" % (self.SYSTEM_LIBRARY_PATH, library)):
            path = self.SYSTEM_LIBRARY_PATH
        elif isdir("%s/%s" % (self.USER_LIBRARY_PATH, library)):
            path = self.USER_LIBRARY_PATH

        if not path:
            raise Exception("Library not exists: %s" % library)

        return "%s/%s" % (path, library)

    def test(self):
        """
        Test the task
        """
        raise Exception("Test not implemented.")

    def main(self, *args):
        """
        Main function
        """
        raise Exception("Main function not implemented.")

    def run(self):
        """
        Run a task
        """
        try:
            if self.test_mode:
                self.test()
                self.produced_output = True
            else:
                for target in self.targets:
                    self.target = target
                    
                    try:
                        inet_aton(target)
                        self.ip = target

                    except:
                        self.host = target

                    self.main(self.arguments)

        except TaskTimeout:
            pass

        except Exception, e:
            error_str = e.__class__.__name__

            if str(e):
                error_str += ': %s' % str(e)

            self._write_result(error_str)
            self.error = True


def execute_task(task_class):
    """
    Executes task and controls its execution
    """
    task = task_class()

    if len(argv) == 2 and argv[1] == "--test":
        task.test_mode = True

    try:
        if not task.test_mode:
            task.parse_input()

        task.start()

        if task.test_mode:
            timeout = task.TEST_TIMEOUT
        else:
            timeout = task.timeout

        if timeout == 0:
            timeout = None

        task.join(timeout)

        if task.isAlive():
            task.stop()
            raise TaskTimeout

        if not task.produced_output:
            raise NoDataReturned

    except TaskTimeout:
        task._write_result('Task has timed out.')

    except NoDataReturned:
        task._write_result('No data returned.')

    except Exception, e:
        output = e.__class__.__name__

        if str(e):
            output += ': %s' % str(e)

        task._write_result(output)
        task.error = True

    # if background task is still alive, commit a suicide
    if task.isAlive():
        # sleep before flush
        sleep(5)
        stdout.flush()

        group_id = getpgrp()
        killpg(group_id, SIGTERM)

    if task.error:
        print "Task completed with errors."
        exit(1)

    exit()
