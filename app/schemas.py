from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime
from typing import Optional

'''
# This class will validate that the body has title as str and content as str
# We'll need to make a schema that has title as str, content as str
class Post(BaseModel):
    title: str
    content: str
    # The default value for publish would be true unless something else was sent
    published: bool = True
    # the default for rating is None but if a value is received it must be an int
    #rating: Optional[int] = None
'''

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class User(BaseModel):
    id: int
    email: str
    created_at: datetime


    class Config:
        # deprecated
        #orm_mode = True
        from_attributes = True


# This is to make the response displays only the specified fields
# title, content and published are inhereted
class Post(PostBase):
    id: int
    #title: str
    #content: str
    #published: bool
    created_at: datetime
    owner_id: int
    # relationship from models.py
    # User is a class name above
    owner: User

    class Config:
        # deprecated
        #orm_mode = True
        from_attributes = True

# post with votes has different schema after join, so we need to create a valid schema
class PostOut(BaseModel):
    Post: Post # references the previous class
    votes: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

'''
class User(BaseModel):
    id: int
    email: str
    created_at: datetime


    class Config:
        orm_mode = True
'''

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)