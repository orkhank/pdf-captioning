from typing import Optional

from pydantic import Field
from pydantic_core import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    This class is used to define the settings for the application.

    Attributes:
        model_config (SettingsConfigDict): Configuration for the settings.
        google_api_key (str): Google API key.
        generative_model_name (str): The name of the generative model to use \
            for image captioning. See\
    [the documentation](https://ai.google.dev/gemini-api/docs/models/gemini)\
            for the available models. The chosen model must support \
            image inputs.
        backoff_max_tries (Optional[int]): The maximum number of attempts to \
            make at generating a caption for an image before giving up. \
            Once exhausted, the exception will be allowed to escape. \
            The default value of None means there is no limit to the \
            number of tries.
        backoff_max_time (Optional[float]): The maximum total amount of time \
            to try for before giving up. Once expired, the exception will be \
            allowed to escape. The default value of None means there is no \
            limit to the amount of time to try for.
    """

    model_config = SettingsConfigDict(
        env_file="config/.env", env_file_encoding="utf-8"
    )

    google_api_key: str
    generative_model_name: str = Field(
        default="gemini-1.5-flash",
        description="The name of the generative model to use for image "
        "captioning. See the documentation at "
        "https://ai.google.dev/gemini-api/docs/models/gemini "
        "for the available models.",
    )
    backoff_max_tries: Optional[int] = Field(
        default=None,
        description="The maximum number of attempts to make at generating a "
        "caption for an image before giving up.",
    )
    backoff_max_time: Optional[float] = Field(
        default=None,
        description="The maximum total amount of time to try for before "
        "giving up. Once expired, the exception will be allowed to "
        "escape.",
    )


try:
    settings = Settings()  # type: ignore
except ValidationError:
    print(
        "Loading settings failed. "
        "The environment variables are not set correctly."
    )
    raise
