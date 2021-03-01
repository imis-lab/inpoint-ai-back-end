from typing import Optional
from pydantic import BaseModel, Field


class DiscourseItem(BaseModel):
    userId: str = Field(...)
    text: str = Field(...)
    parentId: Optional[str] = Field(None)

    class Config:
        schema_extra = {
            'example': {
                'userId': "603527d6e1b3b909c07ad834",
                'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vestibulum lorem dolor, '
                        'sit amet porta velit pellentesque vitae. Pellentesque viverra eu mi vitae porta. Nam arcu '
                        'libero, laoreet vitae lacus id, condimentum tincidunt mi. Maecenas sem diam, pulvinar id '
                        'gravida at, lacinia ac odio. Donec elit lacus, iaculis id suscipit in, sollicitudin vel ex. '
                        'Nunc feugiat, felis et ullamcorper commodo, arcu erat gravida tortor, sit amet feugiat '
                        'lectus dolor sit amet magna. Mauris nec dapibus elit, sed auctor lacus.',
                'parentId': '603527d6e1b3b909c07ad834'
            }
        }


class UpdateDiscourseItem(BaseModel):
    userId: Optional[str] = Field(None)
    text: Optional[str] = Field(None)
    parentId: Optional[str] = Field(None)

    class Config:
        schema_extra = {
            'example': {
                'userId': "603527d6e1b3b909c07ad834",
                'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vestibulum lorem dolor, '
                        'sit amet porta velit pellentesque vitae. Pellentesque viverra eu mi vitae porta. Nam arcu '
                        'libero, laoreet vitae lacus id, condimentum tincidunt mi. Maecenas sem diam, pulvinar id '
                        'gravida at, lacinia ac odio. Donec elit lacus, iaculis id suscipit in, sollicitudin vel ex. '
                        'Nunc feugiat, felis et ullamcorper commodo, arcu erat gravida tortor, sit amet feugiat '
                        'lectus dolor sit amet magna. Mauris nec dapibus elit, sed auctor lacus.',
                'parentId': '603527d6e1b3b909c07ad834'
            }
        }