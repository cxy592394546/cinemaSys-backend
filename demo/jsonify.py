#!/usr/bin/python

from flask import jsonify

sta_200 = {'code': 200, 'message': 'Successful.'}
sta_201 = {'code': 201, 'message': 'Created.'}
sta_204 = {'code': 204, 'message': 'No Content.'}
sta_400 = {'code': 400, 'message': 'Bad request.'}
sta_403 = {'code': 403, 'message': 'You can not do this.'}
sta_404 = {'code': 404, 'message': 'Not found.'}


def get_response(result, status_dic):
    return jsonify({'result': result, 'status': status_dic})


def normal_response(status_dic):
    return jsonify({'status': status_dic})


def error_response(status_dic):
    return jsonify({'status': status_dic})
