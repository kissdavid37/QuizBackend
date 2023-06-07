from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import and_
from sqlalchemy.sql.expression import func
from Model.models import Game, GroupMember, GroupQuestions, Groups, Questions, Users
from app import Session
from Routes.Authentication.Authentication import token_required


group_bp = Blueprint('group', __name__)


# random string from frontend
@group_bp.route('/group', methods=['POST'])
@token_required
def create_group(current_user):
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
@token_required
def get_group_by_name(current_user,group_name):
    s = Session()
    group = s.query(Groups).where(Groups.name == group_name).first()
    s.close()
    if group is None:
        return make_response('Group does not exist!')
    
    else:
        return jsonify(name=group.name)

@group_bp.route('/group',methods=['GET'])
@token_required
def get_all_groups(current_user):
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
@token_required
def delete_group_by_name(current_user,group_name):
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

@group_bp.route('/group/<group_name>', methods=['POST'])
@token_required
def join_group(current_user,group_name):
    s = Session()
    data = request.get_json()
    public_id = data['public_id']
    print(public_id)
    group=s.query(Groups.id).where(Groups.name == group_name).first()
    if group is None:
        s.close()
        return make_response('This group does not exists',404)
    user_id = s.query(Users.id).where(Users.public_id ==public_id).first()[0]
    group_user = s.query(GroupMember).where(and_(GroupMember.group_id == group[0], GroupMember.user_id == user_id)).first()

    if group_user is not None:
        s.close()
        return make_response('This user is already in this group!',409)
    
    else:
        new_member=GroupMember(group_id= group[0], user_id= user_id)
        s.add(new_member)
        s.commit()
        s.close()

        return data


    