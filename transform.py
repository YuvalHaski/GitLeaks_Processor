import json
import sys

from pydantic import BaseModel, ValidationError

from utils.error_handling import ErrorHandler
from utils.logger import logger

error_handler = ErrorHandler()


class Finding(BaseModel):
    filename: str
    line_range: str
    description: str


class Output(BaseModel):
    findings: list[Finding]


def transform_gitleaks_output(raw_data):
    """Transform Gitleaks JSON output to the required format."""
    logger.info("Transforming Gitleaks raw result to new format...")
    try:
        findings = [
            Finding(
                filename=finding["File"],
                line_range=f"{finding['StartLine']}-{finding['EndLine']}",
                description=finding["Description"],
            )
            for finding in raw_data
        ]
        return Output(findings=findings)
    except KeyError as e:
        error_handler.handle_error(e, 2, f"KeyError: Missing key {e} in finding.")
        sys.exit(2)


def process_gitleaks_result(input_path, output_path):
    """Read Gitleaks output, transform it, and save the formatted results."""
    with open(input_path, "r") as f:
        raw_data = json.load(f)
    transformed = transform_gitleaks_output(raw_data)
    if transformed:
        with open(output_path, "w") as f:
            json.dump(transformed.model_dump(), f, indent=4)
        logger.info(f"Transformed output saved to {output_path}")
        print(json.dumps(transformed.model_dump(), indent=4))
    else:
        logger.error("Failed to transform Gitleaks output.")
