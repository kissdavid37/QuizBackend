from flask import Blueprint, jsonify, make_response, request
from Model.models import Answers, Questions
from app import Session

answer_bp= Blueprint('answer', __name__)

@answer_bp.route('/answer', methods=['GET'])
def get_all_answer():
    s = Session()
    output = []
    answers = s.query(Answers).order_by(Answers.question_id).all()
    s.close()

    if not answers:
        return make_response('No answers found!')
    else:
        for answer in answers:
            answers_data = {'id':answer.id, 'question_id': answer.question_id,'text':answer.text, 'is_correct':answer.is_correct}
            output.append(answers_data)
        return output

@answer_bp.route('/answer/<question_id>', methods=['GET'])
def get_questions_answer(question_id):
    s = Session()
    answers = s.query(Answers).where(Answers.question_id == question_id).all()
    s.close()
    output = []

    if not answers:
        return make_response('No answers for this question!')
    else:
        for answer in answers:
            answers_data = {'id': answer.id, 'question_id': answer.question_id, 'text': answer.text, 'is_correct': answer.is_correct}
            output.append(answers_data)
        return output

@answer_bp.route('/answer/<question_id>', methods=['POST'])
def create_answer_for_question(question_id):
    s = Session()
    answers=request.get_json()
    question = s.query(Questions).where(Questions.id == question_id).first()
    if question is None:
        s.close()
        return jsonify(message = 'No question found with this Id')

    elif s.query(Answers).where(Answers.question_id == question_id).count() >= 4:
        s.close()
        return jsonify(message = 'You reached the maximum count of answers for one question!')

    else:
        output = []
        for answer in answers:
            answer_no = answer['no']
            answer_text = answer['text']
            answer_is_correct = answer['is_correct']
            new_answer = Answers(question_id = question_id, text = answer_text, is_correct = answer_is_correct)
            output.append(new_answer)

        s.bulk_save_objects(output)
        s.commit()
        s.close()
        return answers