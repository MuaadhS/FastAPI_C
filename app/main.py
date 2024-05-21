from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


## This line is not needed since we are using alembic
#models.Base.metadata.create_all(bind=engine)



#Create an instance
app = FastAPI()

# the domain that can access our APIs. "*" means all
origins = ["*"]

# CORs
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello and welcome"}


# start server -> uvicorn main:app (python file name: FastAPI instance)
# to restart server ctrl+c then start it again
# uvicorn main:app --reload to update without termination good in development env not production env

### Get all posts
'''
@app.get("/posts", response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    return posts
'''

### Create post

'''
@app.post("/create_post")
# extract the values from body and save it as dict in payload
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"Post": f"The title is {payload['title']} and the content is {payload['content']}"}
'''
'''
@app.post("/create_post")
# reference class Post into variable post
def create_post(new_post: Post):
    # new_post will contain the body of the post
    print(f"The title is {new_post.title}")
    print(f"The content is {new_post.content}")
    print(f"Publish state is {new_post.publish}")
    print(f"The rating is {new_post.rating}")
    # convert to dict using pydantic model function
    print(new_post.dict())
    #print(type(new_post))
    return {"data": "new post"}
'''

### CRUD

'''
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post) # default status code for a specific operation
# reference class Post into variable post
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #               (post.title, post.content, post.published))

    #new_post = cursor.fetchone()

    #save changes
    #conn.commit()

    #new_post = models.Post(title=post.title,
    #                       content=post.content,
    #                       published=post.published)

    #more efficient alterantive to fill the fields
    #unfolding posts dict
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# checks if the id exists in the posts
def post_id(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/posts/{id}", response_model= schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    #post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    #post = post_id(id)
    #print(post)
    # if no post found return response status code
    # status code for exception
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id {id} was not found"}

    return post
'''


'''
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
'''


'''
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # to delete we need to remove index from the array
    #my_posts.pop(index)
    #print(id)
    #index = find_index_post(id)
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    #deleted_post = cursor.fetchone()

    #conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {id} does not exist")
    #my_posts.pop(index)

    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model= schemas.Post)#, status_code=status.HTTP_205_RESET_CONTENT) # default status code for a specific operation
# reference class Post into variable post
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #               (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()

    #conn.commit()
    #index = find_index_post(id)


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    #db.refresh(post)

    #post_dict = post.dict()
    #post_dict["id"] = id
    #my_posts[index] = post_dict

    return post_query.first()
'''


### USERS

'''
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model= schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()


    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id {id} was not found")

    return user
'''