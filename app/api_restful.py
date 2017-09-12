from flask import render_template, jsonify, request
from app import app, db
from models import *

@app.route('/api/device/all', methods=['GET'])
def api_device_all():
    return jsonify(device_list=[i.serialize for i in Device.query.all()])

@app.route('/api/user/all', methods=['GET'])
def api_user_all():
    return jsonify(user_list=[i.serialize for i in User.query.all()])

@app.route('/api/user/count', methods=['GET','POST'])
def api_users_count():
    return jsonify(user_list=[User.query.count()])

@app.route('/api/device/count', methods=['GET','POST'])
def api_devices_count():
    return jsonify(devices_list=[Device.query.count()])

@app.route('/api/user/<user_id>', methods=['GET'])
def api_user_id(user_id):
    return jsonify(user_list=[User.query.get(user_id).serialize])

@app.route('/api/device/<device_id>', methods=['GET'])
def api_device_id(device_id):
    return jsonify(device_list=[Device.query.get(device_id).serialize])

@app.route('/api/device/4user/<user_id>',methods=['GET','POST'])
def api_device_by_user_id(user_id):
    return jsonify(device_list=[i.serialize for i in Device.query.filter_by(user_id=user_id).all()])

@app.route('/api/device/rol/counts', methods=['GET','POST'])
def api_device_rol_counts():
    return jsonify(devices_rol_count_P=Device.query.filter_by(devicerol='P').count(),devices_rol_count_PE=Device.query.filter_by(devicerol='PE').count(),devices_rol_count_CPE=Device.query.filter_by(devicerol='CPE').count())

@app.route('/api/config/group/counts', methods=['GET','POST'])
def api_config_group_counts():
   # return jsonify(config_group_count_STATICROUTE=DeviceConfig.query.filter_by(deviceconfig_group='STATICROUTE').count())
    return jsonify(config_group_count_POSPF=DeviceConfig.query.filter_by(deviceconfig_group='Protocol OSPF').count(),config_group_count_PEIGRP=DeviceConfig.query.filter_by(deviceconfig_group='Protocol EIGRP').count(),config_group_count_PBGP=DeviceConfig.query.filter_by(deviceconfig_group='Protocol BGP').count(),config_group_count_INTERFACE=DeviceConfig.query.filter_by(deviceconfig_group='Interfaces').count(),config_group_count_INTERFACEMPLSIP=DeviceConfig.query.filter_by(deviceconfig_group='Interfaces MPLS IP').count(),config_group_count_INTERFACEVRF=DeviceConfig.query.filter_by(deviceconfig_group='Interfaces VRF').count(),config_group_count_EBGPVRF=DeviceConfig.query.filter_by(deviceconfig_group='eBGP VRF').count(),config_group_count_IBGPMPLS=DeviceConfig.query.filter_by(deviceconfig_group='iBGP MPLS').count(),config_group_count_IBGPEXTENDEDCOMUNITY=DeviceConfig.query.filter_by(deviceconfig_group='iBGP extended community').count(),config_group_count_STATICROUTE=DeviceConfig.query.filter_by(deviceconfig_group='Static Route').count())
