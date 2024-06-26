import argparse
import sys
from typing import Any, Dict, Optional, Sequence

from pypdf import PdfReader

from .utils import (extract_images_from_pdf, format_extracted_data,
                    generate_image_captions)


def parse_args(args: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        prog="pdf_image_captioner",
        description="Extract text from a PDF file and generate "
        "captions for images.",
    )

    parser.add_argument(
        "pdf",
        type=str,
        help="the path to the PDF file",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="the path to the output file. If not provided, the extracted "
        "data will be printed to the standard output.",
    )
    parser.add_argument(
        "--seconds-to-sleep-between-requests",
        "-s",
        type=float,
        default=1.0,
        help="the number of seconds to sleep between requests to the image "
        "captioning service. This is useful to avoid rate limiting. "
        "Defaults to %(default)s seconds.",
    )

    return vars(parser.parse_args(args))


def main(args: Optional[Sequence[str]] = None) -> int:
    parsed_args = parse_args(args)

    pdf_reader = PdfReader(parsed_args["pdf"])

    images_files = extract_images_from_pdf(pdf_reader)
    image_captions = generate_image_captions(
        images_files,
        seconds_to_sleep_between_requests=parsed_args[
            "seconds_to_sleep_between_requests"
        ],
    )

    docs = [
        page.extract_text(
            extraction_mode="layout", layout_mode_space_vertically=False
        )
        for page in pdf_reader.pages
    ]

    # add image caption information to the extracted text
    extracted_data = format_extracted_data(docs, image_captions)

    if parsed_args["output"]:
        with open(parsed_args["output"], "w", encoding="utf-8") as f:
            f.write(extracted_data)

    else:
        print(extracted_data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
