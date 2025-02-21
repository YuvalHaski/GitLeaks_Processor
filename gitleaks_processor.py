import subprocess
import sys

from utils.error_handling import ErrorHandler, CommandErrorExc
from utils import ERROR_KEYWORDS
from utils.logger import logger
from transform import process_gitleaks_result

error_handler = ErrorHandler()


def run_command(command, allowed_exit_codes=(0, 1)):
    """Executes a shell command and handles errors based on exit codes and STDERR content."""
    logger.info(f"Running command: {' '.join(command)}")
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # check for error conditions based on exit code and error keywords in stderr
    if process.returncode not in allowed_exit_codes or any(keyword in process.stderr for keyword in ERROR_KEYWORDS):
        error_message = error_handler.extract_errors(process.stderr).splitlines()[0].strip()
        raise CommandErrorExc(exit_code=process.returncode, error_message=error_message)

    return


def parse_arguments(args, flag="--report-path", default_value="/code/output.json"):
    """Parse a specific argument from the command-line arguments."""
    if flag in args:
        idx = args.index(flag)
        if idx + 1 <= len(args):
            return args[idx + 1]
    args += [flag, default_value]
    return default_value


def process_source(args, transform_function, raw_output_file, formatted_output_file):
    """Handles execution of command and transformation of gitleaks raw output"""
    try:
        run_command(args)
        transform_function(raw_output_file, formatted_output_file)

    except CommandErrorExc as e:
        # specific command-related error with an extracted exit code
        error_handler.handle_error(e, e.error_data.exit_code, e.error_data.error_message)
        sys.exit(e.error_data.exit_code)
    except FileNotFoundError as e:
        # handle missing files with a dedicated error message
        error_handler.handle_error(e, 1, "Gitleaks output file not found.")
        sys.exit(1)
    except Exception as e:
        # catch all remaining errors
        error_handler.handle_error(e, 2, f"Unexpected error: {e}")
        sys.exit(2)


def main(formatted_output_file="/code/formatted_output.json"):
    try:
        args = sys.argv[1:]
        raw_output_file = parse_arguments(args)

        process_source(args, process_gitleaks_result, raw_output_file, formatted_output_file)
    except Exception as e:
        error_handler.handle_error(e, 2, f"Unexpected error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
