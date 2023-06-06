from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import and_
from Model.models import Game, GroupMember, Groups, Users, Answers
from app import Session

game_bp = Blueprint('game', __name__)

@game_bp.route('/game', methods = ['POST'])
def create_game():
    s = Session()
    data = request.get_json()
    group_id = data['group_id']
    #should remove after authentication
    user_id = data['user_id']
    question_id = data['question_id']
    user_answer = data['user_answer']

    new_game = Game(group_id = group_id, question_id =question_id, user_id= user_id, user_answer=user_answer)
    s.add(new_game)
    s.commit()
    s.close

    return data

@game_bp.route('/game/<group_name>', methods=['POST'])
def answer_question(group_name):
    s = Session()
    s2=Session()
    data = request.get_json()
    user_id = data['user_id']
    question_id = data['question_id']
    user_answer = data['user_answer']

    isCorrect = s2.query(Answers.is_correct).where(Answers.id == user_answer).first()[0]
    s2.close()
    group = s.query(Groups).where(Groups.name == group_name).first()
    id = s.query(Groups.id).where(Groups.name == group_name).first()[0]
    member = s.query(GroupMember).where(and_(GroupMember.group_id ==id,GroupMember.user_id ==user_id)).first()
    if member is None:
        s.close()
        return make_response('You are not in this group!',409)
    
    elif group is None:
        s.close()
        return make_response('There is no group with this name',404)
    
    else:
        new_game = Game(group_id = id, question_id= question_id, user_id= user_id, user_answer = user_answer,answer_points=isCorrect)
        s.add(new_game)
        s.commit()
        s.close

        return data
