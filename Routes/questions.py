from flask import Blueprint ,request, make_response,jsonify
from Model.models import GroupQuestions, Groups, Questions
from app import Session
questions_bp=Blueprint('questions', __name__)

@questions_bp.route('/questions')
def get_all_questions():
    s = Session()
    questions=s.query(Questions).order_by(Questions.id).all()
    output = []

    for question in questions:
        question_data={}
        question_data['id']=question.id
        question_data['text']=question.text
        output.append(question_data)
    s.close()

    return output

@questions_bp.route('/questions',methods=['POST'])
def create_question():
    data = request.get_json()
    new_question = Questions(text=data['text'])
    s = Session()
    question=s.query(Questions).where(Questions.text == data['text']).first()

    if question is not None:
        s.close()

        return make_response('This question is already in database!',409)
    
    else:
        s.add(new_question)
        s.commit()
        s.close()

        return jsonify(message='Question added to database!')

@questions_bp.route('/questions/<question_id>',methods=['DELETE'])
def delete_question_by_id(question_id):
    s=Session()
    question=s.query(Questions).where(Questions.id == question_id).first()

    if question is None:
        s.close()
        return jsonify(message = 'This question does not exists')
    
    else:
        s.delete(s.query(Questions).where(Questions.id == question_id).first())
        s.commit()
        s.close()

        return jsonify(message = 'Successfully deleted!' )
    
@questions_bp.route('/questions/<group_id>')
def get_questions_by_group(group_id):
    s = Session()
    questions=s.query(GroupQuestions).where(GroupQuestions.group_id == group_id)
    output = []

    for question in questions:
        question_data={}
        question_data['group_id']=question.group_id
        question_data['question_id']=question.question_id
        output.append(question_data)
    s.close()

    return output