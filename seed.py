import csv

from database import Base, engine, sessionLocal
from models import ProgrammingLanguages

Base.metadata.create_all(bind=engine)


db = sessionLocal()

with open("programming_languages.csv",encoding="utf-8",newline="") as file:
    row_reader = csv.reader(file)

    for name,creator,year,paradigm in row_reader:

        language = ProgrammingLanguages(
            name=name,
            creator=creator,
            year=year,
            paradigm=paradigm
        )

        db.add(language)
        db.commit()


print('All languages inserted successfully')
db.close()