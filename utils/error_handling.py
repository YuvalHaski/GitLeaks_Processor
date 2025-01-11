import re
import json
from pydantic import BaseModel
from .logger import logger

from . import ERROR_KEYWORDS


class CommandError(BaseModel):
    exit_code: int
    error_message: str


class CommandErrorExc(Exception):
    def __init__(self, exit_code: int, error_message: str):
        self.error_data = CommandError(exit_code=exit_code, error_message=error_message)
        super().__init__(self.error_data.error_message)


class ErrorHandler:
    def __init__(self, formatted_output_file="/code/formatted_output.json"):
        self.formatted_output_file = formatted_output_file
        self.logger = logger

    @staticmethod
    def clean_message(error_message: str) -> str:
        ansi_escape_pattern = re.compile(r'\x1b\[[0-9;]*m')
        return ansi_escape_pattern.sub('', error_message)

    def handle_error(self, error, exit_code: int, custom_message=None, raise_error=False):
        error_message = custom_message or str(error)
        self.logger.error(f"Error occurred: {error_message}")
        self.save_error_to_file(exit_code, error_message)

        if raise_error:
            raise error

    def extract_errors(self, error_message: str) -> str:
        cleaned_message = self.clean_message(error_message)
        extracted_lines = [
            line.split(keyword, 1)[1].strip()
            for line in cleaned_message.splitlines()
            for keyword in ERROR_KEYWORDS
            if keyword in line
        ]
        return "\n".join(extracted_lines) if extracted_lines else cleaned_message

    def save_error_to_file(self, exit_code: int, error_message: str):
        error_data = CommandError(exit_code=exit_code,
                                  error_message=self.extract_errors(error_message))
        try:
            with open(self.formatted_output_file, "w") as f:
                json.dump(error_data.model_dump(), f, indent=4)
            self.logger.error(f"Error details saved to {self.formatted_output_file}")
        except Exception as e:
            self.logger.error(f"Failed to save error to file: {e}")
