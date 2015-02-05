# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT
from tempfile import NamedTemporaryFile
from os import unlink
from re import match
from core import Task, execute_task
from core.error import NotEnoughArguments

class Metasploit(Task):
    """
    Metasploit wrapper
    """
    TEST_TIMEOUT = 600
    WORKING_DIR = "/opt/metasploit"
    PARSE_FILES = False

    def _prepare_resource(self, resource, *args):
        """
        Prepare resource
        """
        target = '%s://%s' % (self.proto or 'http', self.target)

        resource = open(resource, "r").read().split("\n")
        resource = map(lambda x: x.replace('\r', ''), resource)
        resource = "\n".join(resource + ["run", "exit -y"])
        resource = resource.replace("@target", target)

        ctr = 0

        for arg in args:
            if not arg:
                continue

            value = arg[0]
            resource = resource.replace("@arg%d" % ctr, value)

            ctr += 1

        resource_file = NamedTemporaryFile(delete=False)
        resource_file.write(resource)
        resource_file.file.flush()

        return resource_file.name

    def main(self, *args):
        """
        Main function
        """
        self._check_stop()

        if not args:
            raise NotEnoughArguments("At least 1 input (metasploit script) should be specified")

        out_file = NamedTemporaryFile(delete=False).name

        try:
            resource_file = self._prepare_resource(args[0], args[1:])

            try:
                output = Popen(
                    "app/msfconsole -r%s -o%s -q" % (resource_file, out_file),
                    stdout=PIPE,
                    stderr=STDOUT,
                    shell=True,
                    cwd=self.WORKING_DIR,
                    env={
                        "HOME": self.WORKING_DIR
                    }
                ).communicate()[0]

                out_data = open(out_file, "r").read()

                if out_data:
                    found_run = False

                    for line in out_data.split("\n"):
                        if not found_run:
                            if match(r"^resource \(%s\)> run" % resource_file, line):
                                found_run = True

                            continue

                        if match(r"^resource \(%s\)>" % resource_file, line):
                            continue

                        self._write_result(line)

                elif output:
                    self._write_result(output)

            finally:
                try:
                    unlink(resource_file)
                except:
                    pass

        finally:
            try:
                unlink(out_file)
            except:
                pass

        self._check_stop()

        if not self.produced_output:
            self._write_result("No result.")

    def test(self):
        """
        Test function
        """
        self.target = "google.com"

        script = NamedTemporaryFile(delete=False)
        script.write("\n".join([
            "use auxiliary/scanner/ssh/ssh_login",
            "set rhosts @target",
            "set userpass_file @arg0",
            "set threads 3",
        ]))
        script.file.flush()

        passwords = NamedTemporaryFile(delete=False)
        passwords.write("test:123\nhello:world\n")
        passwords.file.flush()

        try:
            self.main(script.name, passwords.name)
        finally:
            try:
                unlink(script.name)
                unlink(passwords.name)
            except:
                pass

execute_task(Metasploit)
