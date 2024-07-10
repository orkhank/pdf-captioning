import argparse
import sys
from typing import Any, Dict, Optional, Sequence

from pypdf import PdfReader

from src.image_captioning.image_captioning import ImageCaptioner
from src.pdf_captioning.formatting import DefaultFormatter
from src.pdf_captioning.pdf_captioning import generate_image_captions


def parse_args(args: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        prog="pdf_image_captioner",
        description="Extract text from a PDF file and generate "
        "captions for images.",
    )

    pdf_reader_args = parser.add_argument_group("PDF Reader Arguments")
    pdf_reader_args.add_argument(
        "pdf",
        type=str,
        help="the path to the PDF file to extract text from and generate "
        "image captions for.",
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
    image_captions = generate_image_captions(
        pdf_reader=pdf_reader,
        image_captioner=ImageCaptioner(),
        seconds_to_sleep_between_requests=parsed_args[
            "seconds_to_sleep_between_requests"
        ],
    )
    from pprint import pprint
    pprint(image_captions)

    extracted_text = [
        page.extract_text(
            extraction_mode="layout", layout_mode_space_vertically=False
        )
        for page in pdf_reader.pages
    ]

    extracted_data = DefaultFormatter().format(extracted_text, image_captions)

    if parsed_args["output"]:
        with open(parsed_args["output"], "w", encoding="utf-8") as f:
            f.write(extracted_data)

    else:
        print(extracted_data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
