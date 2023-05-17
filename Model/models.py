from sqlalchemy import *
from sqlalchemy.orm import declarative_base

Base=declarative_base()
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,nullable=False,unique=True)
    public_id = Column(String(250),unique=True)
    username = Column(String(50),unique=True,nullable=False)
    password = Column(String(100),nullable=False)
    admin = Column(Integer,nullable=False)

    def __init__(self,id,publicId,username,password,admin):
        self.id = id
        self.public_id = publicId
        self.username = username
        self.password = password
        self.admin = admin

class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer,primary_key=True,nullable=False,unique=True)
    group_id = Column(Integer,ForeignKey('groups.id'))
    question_id = Column(Integer,ForeignKey('questions.id'),nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    user_answer = Column(Integer,ForeignKey('answers.id'))

    def __init__(self,id,groupId,questionId,userId,userAnswer):
        self.id = id
        self.group_id = groupId
        self.question_id = questionId
        self.user_id = userId
        self.user_answer = userAnswer

class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer,primary_key=True,nullable=False,unique=True)
    name = Column(String(100),nullable=False,unique=True)

    def __init__(self,name):
        self.name = name

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    text = Column (String(250), unique=True,nullable=False)

    def __init__(self, id, text):
        self.id = id
        self.text = text

class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer,primary_key=True, nullable=False, unique=True)
    question_id = Column(Integer,ForeignKey('questions.id'), nullable=False)
    text = Column(String(250),nullable=False,unique=True)
    is_correct = Column(Integer, nullable=False)

    def __init__(self,id,questionId,text,isCorrect):
        self.id = id
        self.question_id = questionId
        self.text = text
        self.is_correct = isCorrect

class Points(Base):
    __tablename__ = 'points'
    id = Column(Integer,primary_key=True, nullable=False, unique=True)
    user_id = Column(String(250),ForeignKey('users.public_id'),unique=True,nullable=False)
    total_points = Column(Integer)