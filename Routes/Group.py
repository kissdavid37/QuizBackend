from flask import Blueprint, jsonify, make_response, request
from sqlalchemy.sql.expression import func
from Model.models import GroupQuestions, Groups, Questions
from app import Session


group_bp = Blueprint('group', __name__)


# random string from frontend
@group_bp.route('/group', methods=['POST'])
def create_group():
    data = request.get_json()
    s = Session()
    group_name = data['name']
    new_group = Groups(name=group_name)
    group = s.query(Groups).where(Groups.name == group_name).first()

    if group is not None:
        s.close()
        return make_response('The group name is already taken!')
    else:
        s.add(new_group)
        s.commit()
        group_id = s.query(Groups.id).where(Groups.name == data['name']).first()[0]
        print(group_id)
        s.close()
        generate_group_questions(group_id)

        return data

@group_bp.route('/group/<group_name>', methods=['GET'])
def get_group_by_name(group_name):
    s = Session()
    group = s.query(Groups).where(Groups.name == group_name).first()
    s.close()
    if group is None:
        return make_response('Group does not exist!')
    
    else:
        return jsonify(name=group.name)

@group_bp.route('/group',methods=['GET'])
def get_all_groups():
    s = Session()
    output = []
    groups = s.query(Groups).order_by(Groups.id).all()
    s.close()

    if not groups:
        return make_response("No Groups found")
    
    for group in groups:
        groups_data = {'id': group.id, 'name': group.name}
        output.append(groups_data)

    return output

@group_bp.route('/group/<group_name>', methods=['DELETE'])
def delete_group_by_name(group_name):
    s = Session()
    group = s.query(Groups.name).where(Groups.name == group_name).first()

    if group is None:
        s.close()
        return make_response('No group with this name!')
    s.delete(s.query(Groups).where(Groups.name == group_name).first())
    s.commit()
    s.close()

    return jsonify(message = 'The group is deleted')


def generate_group_questions(group_id):
    s = Session()
    questions=s.query(Questions).order_by(func.newid()).limit(10)
    group_questions=[]
    for question in questions:
        new_group_questions = GroupQuestions(group_id = group_id, question_id=question.id)
        group_questions.append(new_group_questions)
    s.bulk_save_objects(group_questions)
    s.commit()

    s.close()