from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import ProgrammingLanguages

app = FastAPI()


class LanguageSchema(BaseModel):
    name: str
    creator: str
    year: int
    paradigm: str

    model_config = ConfigDict(from_attributes=True)



@app.get("/languages", response_model=list[LanguageSchema])
def Languages(db: Annotated[Session, Depends(get_db)]):
    languages = db.execute(
        select(
            ProgrammingLanguages.name,
            ProgrammingLanguages.creator,
            ProgrammingLanguages.year,
            ProgrammingLanguages.paradigm,
        )
    ).all()

    if not languages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database is empty",
        )

    return languages


@app.get("/languages/year/{year}", response_model=list[LanguageSchema])
def Year(year: int, db: Annotated[Session, Depends(get_db)]):
    languages = db.scalars(
        select(ProgrammingLanguages).where(ProgrammingLanguages.year == year)
    ).all()

    if not languages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No languages found for the year {year}",
        )

    return languages


@app.get("/languages/name/{name}", response_model=LanguageSchema)
def languageName(name: str, db: Annotated[Session, Depends(get_db)]):
    language = db.scalars(
        select(ProgrammingLanguages).where(ProgrammingLanguages.name.ilike(f"%{name}%"))
    ).first()

    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Language {name} not found"
        )

    return language


@app.get("/languages/paradigm/{paradigm}", response_model=list[LanguageSchema])
def languageParadigm(paradigm: str, db: Annotated[Session, Depends(get_db)]):
    language = db.scalars(
        select(ProgrammingLanguages).where(
            ProgrammingLanguages.paradigm.ilike(f"%{paradigm}%")
        )
    ).all()

    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No languages found for the year {paradigm}",
        )

    return language
