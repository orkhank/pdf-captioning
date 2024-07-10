from typing import Dict, List, NamedTuple

from pypdf._utils import ImageFile
from pypdf import PageObject


def extract_images_from_pdf(
    pdf_pages: List[PageObject],
) -> Dict[int, List[ImageFile]]:
    """
        Extract images from PDF pages.

        Args:
            pdf_pages (List[PageObject]): A list of \
            `PageObject<pypdf.PageObject>` objects representing the pages of a\
            PDF file.

        Returns:
            Dict[int, List[ImageFile]]: A dictionary mapping page numbers to a\
            list of `ImageFile<pypdf._utils.ImageFile>` objects containing\
            images found on that page.
    """
    images: Dict[int, List[ImageFile]] = {}

    for page in pdf_pages:
        # sanity check
        assert (
            page.page_number is not None
        ), "Expected page number to be set, but got None"

        images[page.page_number] = page.images

    return images


class ImageCaption(NamedTuple):
    """
    A named tuple representing an image caption.

    Attributes:
        image_name (str): The name of the image.
        caption (str): The caption for the image.
    """

    image_name: str
    caption: str
