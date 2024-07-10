import functools

import google.generativeai as genai

from src.settings import settings


@functools.lru_cache
def get_google_gen_model(**kwargs) -> genai.GenerativeModel:
    """
    Initialize and return the google generative model.
    The model is cached to avoid reinitializing it multiple times.
    The google API key is set to the value in the settings.
    The model name is set to "gemini-1.5-flash" by default.

    Args:
        **kwargs: Keyword arguments to pass to the `gen
        ai.GenerativeModel` constructor.

    Returns:
        genai.GenerativeModel: The (cached) generative model.
    """
    genai.configure(api_key=settings.google_api_key)

    # set the model name if not provided
    if kwargs.get("model_name", None) is None:
        kwargs["model_name"] = "gemini-1.5-flash"

    model = genai.GenerativeModel(**kwargs)

    return model
