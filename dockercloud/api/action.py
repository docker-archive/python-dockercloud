from __future__ import absolute_import

from .base import Immutable, StreamingLog


class Action(Immutable):
    subsystem = 'audit'
    endpoint = "/action"

    @classmethod
    def _pk_key(cls):
        return 'uuid'

    def logs(self, tail, follow, log_handler=StreamingLog.default_log_handler):
        logs = StreamingLog(self.subsystem, self.endpoint, self.pk, tail, follow)
        logs.on_message(log_handler)
        logs.run_forever()

    def cancel(self):
        return self._perform_action("cancel")

    def retry(self):
        return self._perform_action("retry")
