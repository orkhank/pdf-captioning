import argparse
import sys
import time
from typing import Any, Dict, Optional, Sequence

from pypdf import PdfReader

from .image_captioning.image_captioning import caption_image
from .utils import extract_images_from_pdf


def parse_args(args: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        prog="pdf_image_captioner",
        description="caption images in a PDF file using generative AI",
    )

    parser.add_argument(
        "pdf",
        type=str,
        help="the path to the PDF file",
    )

    return vars(parser.parse_args(args))


def main(args: Optional[Sequence[str]] = None) -> int:
    parsed_args = parse_args(args)

    pdf_reader = PdfReader(parsed_args["pdf"])

    images = extract_images_from_pdf(pdf_reader)
    image_captions: Dict[int, Dict[str, str]] = {}

    for page_number, page_images in images.items():
        for image_file in page_images:
            if not image_file.image:
                print(
                    f"[!] Skipping image {image_file.name} on page "
                    f"{page_number} since it could not be loaded"
                )
                continue

            caption = caption_image(image_file.image)

            # sleep for a bit to avoid rate limiting
            time.sleep(5)

            if caption is None:
                print(
                    f"[!] Failed to generate a caption for image "
                    f"{image_file.name} on page {page_number}"
                )
                continue

            image_captions.setdefault(page_number, {}).update(
                {image_file.name: caption}
            )

            print(
                f"Image {image_file.name} on page {page_number} has the "
                f"following caption: {caption}"
            )

    docs = [
        page.extract_text(
            extraction_mode="layout", layout_mode_space_vertically=False
        )
        for page in pdf_reader.pages
    ]

    # add image caption information to the extracted text
    for page_number, captions in image_captions.items():
        for image_name, caption in captions.items():
            docs[page_number] += f"\n\nImage {image_name}: {caption}"

    # print the final document
    for page_number, doc in enumerate(docs):
        print(f"Page {page_number}:\n{doc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
