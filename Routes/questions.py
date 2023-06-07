from flask import Blueprint ,request, make_response,jsonify
from Model.models import GroupQuestions, Questions, Groups
from app import Session
from Routes.Authentication.Authentication import token_required
questions_bp=Blueprint('questions', __name__)

@questions_bp.route('/questions')
@token_required
def get_all_questions(current_user):
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
@token_required
def create_question(current_user):
    questions = request.get_json()
    s = Session()
    output =[]
    messages= []

    for question in questions:
        question_text = question['text']
        exist = s.query(Questions).filter(Questions.text == question_text).first()

        if exist is not None:
            messages.append(f'Qustion "{question_text}" is already in the database!')
        else:
            new_question = Questions(text= question_text)
            output.append(new_question)
            messages.append(f'Question {question_text} added to the database!')
    s.bulk_save_objects(output)
    s.commit()
    s.close()

    return jsonify(message= messages)


@questions_bp.route('/questions/<question_id>',methods=['DELETE'])
@token_required
def delete_question_by_id(current_user,question_id):
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
    
@questions_bp.route('/questions/<group_name>')
@token_required
def get_questions_by_group(current_user,group_name):
    s = Session()
    group_id = s.query(Groups.id).where(Groups.name == group_name).first()
    if group_id is None:
        s.close()
        return make_response('The Group does not exists',404)
    else:

        questions=s.query(Questions.text,GroupQuestions.question_id,GroupQuestions.group_id).join(GroupQuestions, Questions.id == GroupQuestions.question_id).where(GroupQuestions.group_id == group_id[0])
        s.close()
        output = []

        for question in questions:
            question_data={}
            question_data['group_id']=question.group_id
            question_data['text']=question.text
            question_data['question_id']=question.question_id
            output.append(question_data)

        return output