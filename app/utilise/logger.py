import io
import sys
from kivy.logger import Logger

class LogCapture(io.StringIO):
    def __init__(self, update_callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_callback = update_callback

    def write(self, msg):
        super().write(msg)
        if self.update_callback:
            self.update_callback(self.getvalue())

def init_logger(update_callback=None):
    log_capture = LogCapture(update_callback)
    sys.stdout = log_capture
    sys.stderr = log_capture
    return log_capture
