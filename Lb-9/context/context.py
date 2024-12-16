'''
Context
'''

from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    sessionmaker
)
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine
)

engine = create_engine("sqlite:///./database.db", connect_args={"check_same_thread": False})

ssesion = sessionmaker(bind=engine)

db_context = ssesion()

class Base(DeclarativeBase):
    '''Base Class'''
    pass # pylint: disable=unnecessary-pass

class User(Base):
    '''Model'''
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    posts = relationship("Post", back_populates="user")

class Post(Base):
    '''Model'''
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")

Base.metadata.create_all(bind=engine)

db_context.add_all([
    User(username="Kirill", email="kirill@gmail.com", password="qwerty"),
    User(username="Ivan1337", email="ivanko@gmail.com", password="qwerty1234"),
    User(username="Sidr1337", email="petya.sidrov@gmail.com", password="sidr123"),
])
db_context.commit()

db_context.add_all([
    Post(title="Все о Земле", content="Земля - планета", user_id = 1),
    Post(title="Все о Марсе", content="Марс - планета", user_id = 2),
    Post(title="Все о Венере", content="Венера - планета", user_id = 3)
])
db_context.commit()
