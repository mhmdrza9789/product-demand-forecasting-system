import sys
import traceback
from typing import Optional


class CustomException(Exception):
    def __init__(self, error_message: str, error_details: Optional[object] = None):

        if error_details:
            _, _, exc_tb = sys.exc_info()
        else:
            exc_tb = None

        if exc_tb:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
        else:
            file_name = "<unknown>"
            line_number = -1

        self.error_message = error_message
        self.file_name = file_name
        self.line_number = line_number

        if exc_tb:
            self.traceback_str = "".join(traceback.format_tb(exc_tb))
        else:
            self.traceback_str = ""

        super().__init__(self.__str__())

    def __str__(self):
        return f"Error in [{self.file_name}] at line [{self.line_number}] : {self.error_message}\n{self.traceback_str}"
