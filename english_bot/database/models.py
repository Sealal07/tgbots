from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True) #Telegram ID
    username = Column(String, nullable=True)
    correct_answers = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    current_level = Column(String, default='A1') #?

class PersonalWord(Base):
    __tablename__ ='personal_dictionary'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    word = Column(String)
    translation = Column(String)
    learned_count = Column(Integer, default=0)
    is_learned = Column(Boolean, default=False)

class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    translate = Column(String)
    example = Column(String, nullable=True)

class Idiom(Base):
    __tablename__ = 'idioms'
    id = Column(Integer, primary_key=True)
    phrase = Column(String)
    translate = Column(String)
    example = Column(String)

class TestQuestion(Base):
    __tablename__ = 'test_questions'
    id = Column(Integer, primary_key=True)
    level = Column(String)
    question_text = Column(String)
    options = Column(String)
    correct_option = Column(Integer)