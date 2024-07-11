from pymongo import MongoClient
from pydantic import BaseModel,Field
from typing import List
from fastapi import FastAPI, status, Path


client=MongoClient()


class Book(BaseModel):
   bookID: int
   title: str
   author:str
   publisher: str


app = FastAPI()

DB = "test"
BOOK_COLLECTION = "book"


@app.post("/add_new", status_code=status.HTTP_201_CREATED)
def add_book(b1: Book):
   """Post a new message to the specified channel."""
   with MongoClient() as client:
      book_collection = client[DB][BOOK_COLLECTION]
      result = book_collection.insert_one( b1.dict() )
      ack = result.acknowledged
      return {"insertion": ack}


@app.get("/books", response_model=List[str])
def get_books():
   """Get all books in list form."""
   with MongoClient() as client:
      book_collection = client[DB][BOOK_COLLECTION]
      booklist = book_collection.distinct("title")
      return booklist
      

@app.get("/books/{id}",  response_model=Book )
def get_books( id:int ):
   """Get all books in list form."""
   with MongoClient() as client:
      book_collection = client[DB][BOOK_COLLECTION]
      b1 = book_collection.find_one({"bookID": id})
      return b1


@app.get("/hello/{name}/{age}")
async def hello(*, name: str=Path( ..., min_length=3 , max_length=10), age: int = Path(..., ge=1, le=100)):
   return {"name": name, "age":age}



class student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   marks: List[int] = []
   percent_marks: float

class percent(BaseModel):
   id:int
   name :str = Field(None, title="name of student", max_length=10)
   percent_marks: float

@app.post("/marks", response_model=percent)
async def get_percent(s1:student):

   s1.percent_marks=sum(s1.marks)/2

   return s1