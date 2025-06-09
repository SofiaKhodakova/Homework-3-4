from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"

class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType

class Timestamp(BaseModel):
    id: int
    timestamp: int

dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

@app.get("/", summary="Root", operation_id="root__get")
def root():
    return {}

@app.post("/post", response_model=Timestamp, summary="Get Post", operation_id="get_post_post_post")
def get_post_post():
    new_timestamp = int(datetime.now().timestamp())
    new_id = len(post_db)
    timestamp = Timestamp(id=new_id, timestamp=new_timestamp)
    post_db[new_id] = timestamp
    return timestamp

@app.get("/dog", response_model=List[Dog], summary="Get Dogs", operation_id="get_dogs_dog_get")
def get_dogs(kind: DogType | None = None):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())

@app.post("/dog", response_model=Dog, summary="Create Dog", operation_id="create_dog_dog_post")
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=400, detail="PK already exists")
    dogs_db[dog.pk] = dog
    return dog

@app.get("/dog/{pk}", response_model=Dog, summary="Get Dog By Pk", operation_id="get_dog_by_pk_dog__pk__get")
def get_dog_by_pk(pk: int):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dogs_db[pk]

@app.patch("/dog/{pk}", response_model=Dog, summary="Update Dog", operation_id="update_dog_dog__pk__patch")
def update_dog(pk: int, dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    if pk != dog.pk:
        raise HTTPException(status_code=400, detail="PK's do not match")
    dogs_db[pk] = dog
    return dog
