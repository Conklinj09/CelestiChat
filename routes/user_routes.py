from flask import Blueprint, request, jsonify
from models import db
from models.user import User

user_bp = Blueprint('users', __name__)

@user_bp.route('/add', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully"})

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{ "id": user.id, "name": user.name, "email": user.email} for user in users])