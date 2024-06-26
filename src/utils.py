import textwrap
import time
from copy import deepcopy
from typing import Dict, List, NamedTuple, Optional, Tuple

from pypdf import PdfReader
from pypdf._utils import ImageFile

from .image_captioning.image_captioning import caption_image


def extract_images_from_pdf(
    pdf_reader: PdfReader,
) -> Dict[int, List[ImageFile]]:
    """
    Extract images from a PDF file.

    Args:
        pdf_reader (PdfReader): The PDF reader object.

    Returns:
        Dict[int, List[ImageFile]]: A dictionary mapping page numbers to a\
        list of images found on that page.
    """
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
            print(f"[-] No images found on page {page.page_number}")

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


def generate_image_captions(
    images: Dict[int, List[ImageFile]],
    *,
    seconds_to_sleep_between_requests: Optional[float] = None,
) -> Dict[int, List[ImageCaption]]:
    """
    Generate captions for images.

    Args:
        images (Dict[int, List[ImageFile]]): A dictionary mapping page numbers\
        to a list of images found on that page.

        seconds_to_sleep_between_requests (Optional[float]): The number of\
        seconds to sleep between requests to the image captioning service.\
        This is useful to avoid rate limiting. Defaults to None.

    Returns:
        Dict[int, List[ImageCaption]]: A dictionary mapping page numbers to a\
        list of image captions found on that page.
    """
    image_captions: Dict[int, List[ImageCaption]] = {}

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
            if seconds_to_sleep_between_requests:
                time.sleep(seconds_to_sleep_between_requests)

            if caption is None:
                print(
                    f"[!] Failed to generate a caption for image "
                    f"{image_file.name} on page {page_number}"
                )
                continue

            # save the caption
            image_captions_on_current_page = image_captions.setdefault(
                page_number, []
            )
            image_captions_on_current_page.append(
                ImageCaption(image_file.name, caption)
            )

            print(
                f"Image {image_file.name} on page {page_number} has the "
                f"following caption: {caption}"
            )

    return image_captions


def add_image_captions_to_docs(
    image_captions: Dict[int, List[ImageCaption]], docs: List[str]
) -> List[str]:
    attachments: List[Tuple[int, str]] = []

    # add image captions to the extracted text as an attachment
    for page_number, image_captions_on_page in image_captions.items():
        attachment = generate_image_captions_attachment(image_captions_on_page)
        attachments.append((page_number, attachment))

    captioned_docs = deepcopy(docs)
    for page_number, attachment in attachments:
        captioned_docs[page_number] += textwrap.indent(attachment, "    ")

    return captioned_docs


def generate_image_captions_attachment(image_captions_on_page):
    attachment = textwrap.dedent(
        f"""
        \n
        ---------------- <start of attachment> ----------------

        This page contains {len(image_captions_on_page)} images.
        The following are the name of each image and its caption:\n
        """
    )
    for image_caption in image_captions_on_page:
        attachment += f"- {image_caption.image_name}\n"
        attachment += textwrap.indent(
            textwrap.fill(image_caption.caption, width=53), "     "
        )
        attachment += "\n\n"
    attachment += (
        "\n\n----------------- <end of attachment> -----------------\n\n"
    )
    return attachment


def format_extracted_data(
    extracted_text: List[str],
    image_captions: Optional[Dict[int, List[ImageCaption]]] = None,
    *,
    add_page_numbers: bool = True,
) -> str:
    """
    Combine the extracted text and image captions into a single formatted
    string.

    Args:
        extracted_text (List[str]): A list of strings, where each string\
        represents the extracted text from a page.

        image_captions (Optional[Dict[int, List[ImageCaption]]]): A dictionary\
        mapping page numbers to a list of image captions. Defaults to None.

        add_page_numbers (bool): Whether to add page numbers to the formatted\
        extracted data. Defaults to True.

    Returns:
        str: The formatted extracted data.
    """

    captioned_docs = (
        extracted_text
        if image_captions is None
        else add_image_captions_to_docs(image_captions, extracted_text)
    )
    formated_data = ""
    for i, doc in enumerate(captioned_docs, 1):
        formated_data += f"Page {i}\n" if add_page_numbers else ""
        formated_data += doc
        formated_data += "\n\n" + "-" * 80 + "\n\n"
    return formated_data
