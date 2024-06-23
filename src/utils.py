from typing import Dict, List
from pypdf import PdfReader
from pypdf._utils import ImageFile


def extract_images_from_pdf(
    pdf_reader: PdfReader,
) -> Dict[int, List[ImageFile]]:
    images: Dict[int, List[ImageFile]] = {}

    for page in pdf_reader.pages:
        # sanity check
        assert (
            page.page_number is not None
        ), "Expected page number to be set, but got None"

        if page.images:
            print(
                f"[+] Found a total of {len(page.images)} images "
                f"in page {page.page_number}"
            )
        else:
            print(f"[!] No images found on page {page.page_number}")

        images[page.page_number] = page.images

    return images
