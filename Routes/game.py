from flask import Blueprint, jsonify, make_response, request
from Model.models import Game, Groups
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
