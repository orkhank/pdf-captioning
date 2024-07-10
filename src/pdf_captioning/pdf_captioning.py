import time
from typing import Dict, List, Optional

from pypdf import PdfReader

from src.image_captioning.image_captioning import ImageCaptioner
from src.pdf_captioning.utils import ImageCaption, extract_images_from_pdf


def generate_image_captions(
    pdf_reader: PdfReader,
    image_captioner: ImageCaptioner,
    *,
    seconds_to_sleep_between_requests: Optional[float] = None,
) -> Dict[int, List[ImageCaption]]:
    """
    Generate captions for images found in the PDF file.


    Args:
        pdf_reader (PdfReader): The PDF reader to use for extracting\
        images from the PDF file.
        image_captioner (ImageCaptioner): The image captioner to use for\
        generating captions for images.
        seconds_to_sleep_between_requests (Optional[float]): The number of\
        seconds to sleep between requests to the image captioning service.\
        This is useful to avoid rate limiting. Defaults to None.

    Returns:
        Dict[int, List[ImageCaption]]: A dictionary mapping page numbers\
        to a list of image captions found on that page.
    """
    images = extract_images_from_pdf(pdf_reader.pages)
    image_captions: Dict[int, List[ImageCaption]] = {}

    for page_number, page_images in images.items():
        for image_file in page_images:
            if not image_file.image:
                print(
                    f"[!] Skipping image {image_file.name} on page "
                    f"{page_number} since it could not be loaded"
                )
                continue

            caption = image_captioner.caption_image(image_file.image)

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

    return image_captions
