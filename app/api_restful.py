from flask import render_template, jsonify, request
from app import app, db
from models import *

@app.route('/api/device/all', methods=['GET'])
def api_device_all():
    return jsonify(device_list=[i.serialize for i in Device.query.all()])

@app.route('/api/user/all', methods=['GET'])
def api_user_all():
    return jsonify(user_list=[i.serialize for i in User.query.all()])

@app.route('/api/user/<user_id>', methods=['GET'])
def api_user_id(user_id):
    return jsonify(user_list=[User.query.get(user_id).serialize])

@app.route('/api/device/<device_id>', methods=['GET'])
def api_device_id(device_id):
    return jsonify(device_list=[Device.query.get(device_id).serialize])

@app.route('/api/device/4user/<user_id>',methods=['GET'])
def api_device_by_user_id(user_id):
    return jsonify(device_list=[i.serialize for i in Device.query.filter_by(user_id=user_id).all()])