# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import check_cms

class CMSDetectionTask(gtta.Task):
    """
    CMS Detection checker
    """
    def main(self):
        """
        Main function
        """
        target = '%s://%s' % (
            self.proto or 'http',
            self.host or self.ip
        )

        ok, cms = check_cms.get_cms_type(target)

        if not ok:
            self._write_result('CMS-Explorer calling error!')

        self._write_result(cms)

gtta.execute_task(CMSDetectionTask)
