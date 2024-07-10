import textwrap
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Dict, List, Tuple

from src.pdf_captioning.utils import ImageCaption


class Formatter(ABC):
    """
    An abstract base class for formatters.
    """

    @abstractmethod
    def format(
        self,
        extracted_text: List[str],
        image_captions: Dict[int, List[ImageCaption]],
    ) -> str:
        pass


class DefaultFormatter(Formatter):
    """
    A default formatter for formatting extracted text and image captions.
    """

    def __init__(self, add_page_numbers: bool = True):
        """
        Initialize the DefaultFormatter.

        Args:
            add_page_numbers (bool): Whether to add page numbers to the\
            formatted extracted data. The page numbers are added at the\
            beginning of each page. Defaults to True.
        """
        super().__init__()

        self.add_page_numbers = add_page_numbers

    def generate_image_captions_attachment(
        self, image_captions_on_page: List[ImageCaption]
    ) -> str:
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

    def add_image_captions_to_docs(
        self, image_captions: Dict[int, List[ImageCaption]], docs: List[str]
    ) -> List[str]:
        attachments: List[Tuple[int, str]] = []

        # add image captions to the extracted text as an attachment
        for page_number, image_captions_on_page in image_captions.items():
            attachment = self.generate_image_captions_attachment(
                image_captions_on_page
            )
            attachments.append((page_number, attachment))

        captioned_docs = deepcopy(docs)
        for page_number, attachment in attachments:
            captioned_docs[page_number] += textwrap.indent(attachment, "    ")

        return captioned_docs

    def format(
        self,
        extracted_text: List[str],
        image_captions: Dict[int, List[ImageCaption]],
    ) -> str:

        captioned_docs = (
            extracted_text
            if image_captions is None
            else self.add_image_captions_to_docs(
                image_captions, extracted_text
            )
        )
        formated_data = ""
        for i, doc in enumerate(captioned_docs, 1):
            formated_data += f"Page {i}\n" if self.add_page_numbers else ""
            formated_data += doc
            formated_data += "\n\n" + "-" * 80 + "\n\n"
        return formated_data
