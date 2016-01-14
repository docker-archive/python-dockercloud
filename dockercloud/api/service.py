from __future__ import absolute_import

from .base import Mutable, Taggable, Triggerable, StreamingLog


class Service(Mutable, Taggable, Triggerable):
    subsystem = "app"
    endpoint = "/service"

    def start(self):
        return self._perform_action("start")

    def stop(self):
        return self._perform_action("stop")

    def redeploy(self, reuse_volumes=True):
        params = {'reuse_volumes': reuse_volumes}
        return self._perform_action("redeploy", params=params)

    def scale(self):
        return self._perform_action("scale")

    def logs(self, tail, follow, log_handler=StreamingLog.default_log_handler):
        logs = StreamingLog(self.subsystem, self.endpoint, self.pk, tail, follow)
        logs.on_message(log_handler)
        logs.run_forever()
