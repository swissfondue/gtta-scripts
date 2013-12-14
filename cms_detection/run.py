# -*- coding: utf-8 -*-

import core
import cms_explorer

class CMSDetectionTask(core.Task):
    """
    CMS Detection checker
    """
    def main(self, *args):
        """
        Main function
        """
        target = '%s://%s' % (
            self.proto or 'http',
            self.host or self.ip
        )

        ok, cms = cms_explorer.get_cms_type(target)

        if not ok:
            self._write_result('CMS-Explorer call error!')

        self._write_result(cms)

core.execute_task(CMSDetectionTask)
