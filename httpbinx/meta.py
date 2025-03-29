"""
This module defines the metadata for API tags used in the FastAPI application.
These tags are used to organize and categorize different endpoints in the API documentation.
"""
from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str = Field(..., description='The name of the tag')
    description: str = Field(..., description='A brief description of the tag')


class TagsMetadata(BaseModel):
    tags: List[Tag] = Field(..., description='List of API tags')


TAGS_METADATA = TagsMetadata(
    tags=[
        Tag(name='HTTP Methods', description='Testing different HTTP verbs'),
        Tag(name='Auth', description='Auth methods'),
        Tag(name='Status codes', description='Generates responses with given status code'),
        Tag(name='Request inspection', description='Inspect the request data'),
        Tag(name='Response inspection', description='Inspect the response data like caching and headers'),
        Tag(name='Response formats', description='Returns responses in different data formats'),
        Tag(name='Dynamic data', description='Generates random and dynamic data'),
        Tag(name='Cookies', description='Creates, reads and deletes Cookies'),
        Tag(name='Images', description='Returns different image formats'),
        Tag(name='Redirects', description='Returns different redirect responses'),
        Tag(name='Anything', description='Returns anything that is passed to request'),
    ]
)


@lru_cache
def get_tags_metadata() -> List[dict]:
    """
    Returns the tags metadata in the format expected by FastAPI.
    """
    return [tag.model_dump() for tag in TAGS_METADATA.tags]
