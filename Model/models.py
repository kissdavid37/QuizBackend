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
    question_id = Column(Integer,ForeignKey('questions.id'))
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    user_answer = Column(Integer,ForeignKey('answers.id'))

    def __init__(self,group_id,question_id,user_id,user_answer):
        self.group_id = group_id
        self.question_id = question_id
        self.user_id = user_id
        self.user_answer = user_answer

class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer,primary_key=True,nullable=False,unique=True)
    name = Column(String(100),nullable=False,unique=True)

    def __init__(self,name):
        self.name = name

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True,autoincrement=True, nullable=False, unique=True)
    text = Column (String(250), unique=True,nullable=False)

    def __init__(self, text):
        self.text = text

class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer,primary_key=True, nullable=False, unique=True)
    question_id = Column(Integer,ForeignKey('questions.id'), nullable=False)
    text = Column(String(250),nullable=False)
    is_correct = Column(Integer, nullable=False)

    def __init__(self,question_id,text,is_correct):
        self.question_id = question_id
        self.text = text
        self.is_correct = is_correct

class Points(Base):
    __tablename__ = 'points'
    id = Column(Integer,primary_key=True, nullable=False, unique=True)
    user_id = Column(String(250),ForeignKey('users.public_id'),unique=True,nullable=False)
    total_points = Column(Integer)

class GroupQuestions(Base):
    __tablename__ = 'group_questions'
    id = Column(Integer, primary_key=True,autoincrement=True, nullable=False, unique=True)
    group_id = Column (Integer,ForeignKey('groups.id'))
    question_id = Column (Integer,ForeignKey('questions.id'))

    def __init__(self, group_id,question_id):
        self.group_id = group_id
        self.question_id=question_id

class GroupMember(Base):
    __tablename__ = 'group_member'
    id = Column(Integer, primary_key=True,autoincrement=True, nullable=False, unique=True)
    group_id = Column (Integer,ForeignKey('groups.id'))
    user_id = Column (Integer,ForeignKey('users.id'))

    def __init__(self, group_id,user_id):
        self.group_id = group_id
        self.user_id=user_id