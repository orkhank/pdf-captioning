import functools
import random
from typing import Union

import backoff
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from PIL.Image import Image

from src.settings import settings

from .prompts import PROMPTS


@functools.lru_cache
def get_image_captioning_model():
    genai.configure(api_key=settings.google_api_key)

    model = genai.GenerativeModel(settings.generative_model_name)

    return model


# The `backoff.on_exception` decorator is used to retry the function
# when a `ResourceExhausted` exception is raised. This is useful when
# the API rate limit is exceeded.
@backoff.on_exception(
    backoff.expo,
    ResourceExhausted,
    max_tries=settings.backoff_max_tries,
    max_time=settings.backoff_max_time,
    raise_on_giveup=False,
    jitter=backoff.full_jitter,
)
def caption_image(image: Image) -> Union[str, None]:
    """
    Generate a caption for the given image.

    Args:
        image (PIL.Image.Image): The image to generate a caption for.

    Returns:
        Union[str, None]: The generated caption or None if the caption\
        could not be generated (e.g. due to rate limiting, safety filters,\
        etc.).

    Raises:
        google.api_core.exceptions.*: Any exceptions raised by the API. These\
        exceptions may be due to invalid API keys, unsupported locations, etc.
    """
    model = get_image_captioning_model()
    prompt = random.choice(PROMPTS)  # randomly select a prompt

    response = model.generate_content([prompt, image])

    parts = response.parts
    if not parts:
        return None

    return response.text
