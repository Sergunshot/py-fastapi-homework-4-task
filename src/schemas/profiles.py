from datetime import date
from typing import Annotated

from fastapi import UploadFile, Form, File, HTTPException
from pydantic import BaseModel, field_validator, HttpUrl

from validation import (
    validate_name,
    validate_image,
    validate_gender,
    validate_birth_date
)

from src.database.models.accounts import GenderEnum


class ProfileRequestSchema(BaseModel):
    first_name: Annotated[str, Form(...)]
    last_name: Annotated[str, Form(...)]
    gender: Annotated[GenderEnum, Form(...)]
    date_of_birth: Annotated[date, Form(...)]
    info: Annotated[str, Form(...)]
    avatar: Annotated[UploadFile, File(...)]

    @classmethod
    def as_form(
        cls,
        first_name: Annotated[str, Form()],
        last_name: Annotated[str, Form()],
        gender: Annotated[GenderEnum, Form()],
        date_of_birth: Annotated[date, Form()],
        info: Annotated[str, Form()],
        avatar: Annotated[UploadFile, File()]
    ):

        validate_name(first_name)
        validate_name(last_name)
        validate_gender(gender)
        validate_birth_date(date_of_birth)

        if not info.strip():
            raise ValueError("Info field cannot be empty or contain only spaces.")

        validate_image(avatar)

        return cls(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            info=info,
            avatar=avatar
        )


class ProfileResponseSchema(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: str
