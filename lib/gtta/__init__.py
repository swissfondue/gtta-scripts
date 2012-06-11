# -*- coding: utf-8 -*-

from threading import Thread, Event
from Queue import Queue
from sys import argv, exit
from socket import inet_aton
from error import NotEnoughArguments, TaskTimeout, NoDataReturned, InvalidTargetFile

class Task(Thread):
    """
    Base class for all tasks
    """
    TIMEOUT        = 60    # task timeout
    DNS_TIMEOUT    = 10    # DNS request timeout
    SOCKET_TIMEOUT = 2     # socket timeout
    HTTP_TIMEOUT   = 30    # HTTP timeout
    SMTP_TIMEOUT   = 10    # SMTP timeout
    PARSE_FILES    = True  # read & parse all input files by default

    def __init__(self):
        """
        Constructor
        """
        super(Task, self).__init__()

        self.host    = None
        self.ip      = None
        self.proto   = None
        self.port    = None
        self.lang    = None
        self._stop   = Event()
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
        self.produced_output = True

        if self._result:
            self._result.write(str, '\n')
            self._result.flush()

        else:
            print str

    def stop(self):
        """
        Thread stop function
        """
        self._stop.set()

    def _parse_input(self):
        """
        Parses input arguments
        """
        output_arguments = []

        if len(argv) < 3:
            raise NotEnoughArguments('At least 2 command line arguments should be specified.')

        # parse the first file with hostname or IP
        lines = open(argv[1], 'r').read().split('\n')
        lines = map(lambda x: x.replace('\r', ''), lines)

        if len(lines) < 4:
            raise InvalidTargetFile('Target file should contain at least 4 lines.')

        if not lines[0]:
            raise InvalidTargetFile('Target file should contain either host name or IP address of the target host on the 1st line.')

        try:
            inet_aton(lines[0])
            self.ip = lines[0]

        except:
            self.host = lines[0]

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

        # open output file
        self.result = open(argv[2], 'w')

        # parse the remaining arguments
        for arg in argv[3:]:
            if self.PARSE_FILES:
                lines = open(arg, 'r').read().split('\n')
                lines = map(lambda x: x.replace('\r', ''), lines)
                output_arguments.append(lines)

            else:
                output_arguments.append(arg)

        return output_arguments

    def run(self):
        """
        Run a task
        """
        try:
            arguments = self._parse_input()
            self.main(*arguments)

        except TaskTimeout:
            pass

        except Exception, e:
            error_str = e.__class__.__name__

            if str(e):
                error_str += ': %s' % str(e)

            self._write_result(error_str)

def execute_task(task_class):
    """
    Executes task and controls its execution
    """
    try:
        task = task_class()
        task.start()
        task.join(task.TIMEOUT)

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

    exit()
