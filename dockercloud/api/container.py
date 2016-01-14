from __future__ import absolute_import

from .base import Mutable, StreamingLog, Exec


class Container(Mutable):
    subsystem = "app"
    endpoint = "/container"

    def save(self):
        raise AttributeError("'save' is not supported in 'Container' object. "
                             "Please use the related 'Service' object instead.")

    def start(self):
        return self._perform_action("start")

    def stop(self):
        return self._perform_action("stop")

    def redeploy(self, reuse_volumes=True):
        params = {'reuse_volumes': reuse_volumes}
        return self._perform_action("redeploy", params=params)

    def logs(self, tail, follow, log_handler=StreamingLog.default_log_handler):
        logs = StreamingLog(self.subsystem, self.endpoint, self.pk, tail, follow)
        logs.on_message(log_handler)
        logs.run_forever()

    def execute(self, cmd, handler=Exec.default_message_handler):
        if hasattr(self, "uuid"):
            exec_obj = Exec(self.uuid, cmd)
            exec_obj.on_message(handler)
            exec_obj.run_forever()
