from flask import Blueprint, jsonify, make_response, request
from Model.models import Groups
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
        s.close()
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
    s=Session()
    output=[]
    groups=s.query(Groups).order_by(Groups.id).all()
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

