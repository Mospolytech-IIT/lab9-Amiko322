'''
Лабораторная работа №9
'''

from fastapi import FastAPI, Depends, Form, Response
from fastapi.responses import FileResponse
from requests import Session
from context.context import User, Post, ssesion

app = FastAPI()

def get_service_db():
    '''Db'''
    db_context = ssesion()

    try:
        yield db_context
    finally:
        db_context.close()

@app.get("/")
def get_file_index():
    '''Задание 1'''
    return FileResponse(r"index.html")

@app.post("/create-user", status_code=201)
def create_user(
    username: str = Form(),
    email: str = Form(),
    password: str = Form(),
    db_context: Session = Depends(get_service_db)
):
    '''Задание 2'''
    user = User(username=username, email=email, password=password)
    db_context.add(user)
    db_context.commit()
    db_context.refresh(user)
    return user

@app.get("/users", status_code=200)
def get_users(db_context: Session = Depends(get_service_db)):
    '''Задание 3'''
    return db_context.query(User).all()

@app.post("/update-user-email", status_code=200)
def update_user(
    user_id: int,
    response: Response,
    email = Form(),
    db_context: Session = Depends(get_service_db)
):
    '''Задание 4'''
    user = db_context.query(User).filter(User.id == user_id).first()

    if not user:
        response.status_code = 404
        return { "message" : "не найдено" }

    user.email = email
    db_context.commit()
    db_context.refresh(user)
    return user

@app.post("/delete-users", status_code=200)
def delete_user(
    user_id: int,
    response: Response,
    db_context: Session = Depends(get_service_db)
):
    '''Задание 5'''
    user = db_context.query(User).filter(User.id == user_id).first()

    if not user:
        response.status_code = 404
        return { "message" : "не найдено" }

    db_context.delete(user)
    db_context.commit()
    return { "message": "delete user" }

@app.get("/posts", status_code=200)
def read_posts(db_context: Session = Depends(get_service_db)):
    '''Задание 6'''
    return db_context.query(Post).all()

@app.post("/create-post", status_code=201)
def create_post(
    response: Response,
    user_id: int = Form(),
    title: str = Form(),
    content: str = Form(),
    db_context: Session = Depends(get_service_db)
):
    '''Задание 7'''
    user = db_context.query(User).filter(User.id == user_id).first()

    if not user:
        response.status_code = 404
        return { "message" : "не найдено" }

    post = Post(title=title, content=content, user_id=user_id)
    db_context.add(post)
    db_context.commit()
    db_context.refresh(post)
    return post

@app.post("/update-content-post", status_code=200)
def update_post(
    post_id: int,
    response: Response,
    content: str = Form(),
    db_context: Session = Depends(get_service_db)
):
    '''Задание 8'''
    post = db_context.query(Post).filter(Post.id == post_id).first()

    if not post:
        response.status_code = 404
        return { "message" : "не найдено" }

    post.content = content
    db_context.commit()
    db_context.refresh(post)
    return post

@app.post("/delete-post", status_code=200)
def delete_post(
    post_id: int,
    response: Response,
    db_context: Session = Depends(get_service_db)
):
    '''Задание 9'''
    post = db_context.query(Post).filter(Post.id == post_id).first()

    if not post:
        response.status_code = 404
        return { "message" : "не найдено" }

    db_context.delete(post)
    db_context.commit()
    return { "message": "delete post" }
