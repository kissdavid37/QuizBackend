from flask import Blueprint
from Model.models import Questions
from app import Session
questions_bp=Blueprint('questions', __name__)

@questions_bp.route('/questions')
def get_all_questions():
    s=Session()
    questions=s.query(Questions).order_by(Questions.id).all()
    output=[]
    for question in questions:
        question_data={}
        question_data['id']=question.id
        question_data['text']=question.text
        output.append(question_data)
    s.close()
    return output