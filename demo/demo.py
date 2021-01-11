#! /usr/bin/python

from flask import Flask, request
from flask_cors import CORS
from flask_restplus import Api, Resource, fields, reqparse

from jsonify import *
from db_insert import *
from db_update import *
from db_delete import *
from db_search import *

app = Flask(__name__)
cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})

api = Api(app, version='1.0', title='Cinema Microservice', description='APIs of Cinema Microservice', )

ns = api.namespace('api', path='/v1/', description='APIs of Cinema Microservice')

cinema_info = api.model('Cinema', {  # 返回值模型
    'cinemaId': fields.Integer(required=True, description='The cinema unique identifier'),
    'info': fields.String(required=True, description='Info of the cinema')
})
room_info = api.model('Room', {
    'cinemaId': fields.Integer(required=True, description='The cinema unique identifier'),
    'roomId': fields.Integer(required=True, description='The room unique identifier'),
    'info': fields.String(required=True, description='Info of the room')
})
seat_info = api.model('Seat', {
    'roomId': fields.Integer(required=True, description='The room unique identifier'),
    'seatId': fields.Integer(required=True, description='The seat unique identifier'),
    'info': fields.String(required=True, description='Info of the seat')
})
session_info = api.model('Session', {
    'sessionId': fields.Integer(required=True, description='The session unique identifier'),
    'roomId': fields.Integer(required=True, description='The room unique identifier'),
    'movieId': fields.Integer(required=True, description='The movie unique identifier'),
    'time': fields.String(required=True, description='Time of the session')
})
cinema_to_insert = api.model('cinemaInsert', {  # 返回值模型
    'cinemaId': fields.Integer(readonly=True, required=True, description='The cinema unique identifier'),
    'info': fields.String(required=True, description='Info of the cinema')
})
room_to_insert = api.model('roomInsert', {
    'roomId': fields.Integer(readonly=True, required=True, description='The room unique identifier'),
    'cinemaId': fields.Integer(required=True, description='The cinema unique identifier'),
    'info': fields.String(required=True, description='Info of the room')
})
seat_to_insert = api.model('seatInsert', {
    'seatId': fields.Integer(readonly=True, required=True, description='The seat unique identifier'),
    'roomId': fields.Integer(required=True, description='The room unique identifier'),
    'info': fields.String(required=True, description='Info of the seat')
})
session_to_insert = api.model('sessionInsert', {
    'sessionId': fields.Integer(readonly=True, required=True, description='The session unique identifier'),
    'roomId': fields.Integer(required=True, description='The room unique identifier'),
    'movieId': fields.Integer(required=True, description='The movie unique identifier'),
    'time': fields.String(required=True, description='Time of the session'),
})
cinema_to_delete = api.model("cId", {
    'cinemaId': fields.Integer(required=True, description='The cinema unique identifier'),
})
room_to_delete = api.model("crId", {
    'roomId': fields.Integer(required=True, description='The room unique identifier'),
})
seat_to_delete = api.model("rsId", {
    'seatId': fields.Integer(required=True, description='The seat unique identifier'),
})
session_to_delete = api.model("sId", {
    'sessionId': fields.Integer(required=True, description='The session unique identifier'),
})


# Cinema Model
class Cinema(Resource):
    @ns.response(200, "Success response", cinema_info)  # 对应解析文档返回值
    def get(self):
        cinema_datas = search(['cinema'], [])
        return get_response(cinema_datas, sta_200)
    
    @ns.expect(cinema_to_insert)
    @ns.response(201, "Created")
    @ns.response(400, "Bad Request")
    def post(self):
        request_data = api.payload
        if 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        insert(['cinema'], [info])
        return normal_response(sta_201)

    @ns.expect(cinema_info)
    @ns.response(200, "Success response")
    @ns.response(400, "Bad Request")
    def put(self):
        request_data = api.payload
        if 'cinemaId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        cinema_id = int(request_data['cinemaId'])
        update(['cinema'], [cinema_id, info])
        return normal_response(sta_200)

    @ns.expect(cinema_to_delete)
    @ns.response(204, "Deleted")
    @ns.response(400, "Bad Request")
    def delete(self):
        request_data = api.payload
        if 'cinemaId' not in request_data:
            return error_response(sta_400)
        cinema_id = int(request_data['cinemaId'])
        delete(['cinema'], [cinema_id])
        return normal_response(sta_204)

ns.add_resource(Cinema, "/cinema", endpoint="Cinema")


# Room Model
class Room(Resource):
    parser = reqparse.RequestParser()  # 参数模型
    parser.add_argument('cinemaId', type=int, required=True, help="id")
    @ns.expect(parser)  # 用于解析对应文档参数，
    @ns.response(200, "Success response", room_info)  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def get(self):
        args = int(request.args.get("cinemaId"))
        room_datas = search(['room', 'cinema'], [args])
        return get_response(room_datas, sta_200)

    @ns.expect(room_to_insert)
    @ns.response(201, "Created")
    @ns.response(400, "Bad Request")
    def post(self):
        request_data = api.payload
        if 'cinemaId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        cinema_id = request_data['cinemaId']
        insert(['room', 'cinema'], [cinema_id, info])
        return normal_response(sta_201)

    @ns.expect(room_info)
    @ns.response(200, "Success response")
    @ns.response(400, "Bad Request")
    def put(self):
        request_data = api.payload
        if 'roomId' not in request_data or 'cinemaId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        cinema_id = int(request_data['cinemaId'])
        room_id = int(request_data['roomId'])
        update(['room', 'cinema'], [room_id, cinema_id, info])
        return normal_response(sta_200)

    @ns.expect(room_to_delete)
    @ns.response(204, "Deleted")
    @ns.response(400, "Bad Request")
    def delete(self):
        request_data = api.payload
        if 'roomId' not in request_data:
            return error_response(sta_400)
        room_id = int(request_data['roomId'])
        delete(["room"], [room_id])
        return normal_response(sta_200)


ns.add_resource(Room, "/room", endpoint="Room")


# Seat Model
class Seat(Resource):
    parser = reqparse.RequestParser()  # 参数模型
    parser.add_argument('roomId', type=int, required=True, help="id")
    @ns.expect(parser)  # 用于解析对应文档参数，
    @ns.response(200, "Success response", seat_info)  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def get(self):
        # result = []
        args = int(request.args.get("roomId"))
        seat_datas = search(['seat', 'room'], [args])
        return get_response(seat_datas, sta_200)

    @ns.expect(seat_to_insert)
    @ns.response(201, "Created")
    @ns.response(400, "Bad Request")
    def post(self):
        request_data = api.payload
        if 'roomId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        room_id = request_data['roomId']
        insert(['seat', 'room'], [room_id, info])
        return normal_response(sta_201)

    @ns.expect(seat_info)
    @ns.response(200, "Success response")
    @ns.response(400, "Bad Request")
    def put(self):
        request_data = api.payload
        if 'seatId' not in request_data or 'roomId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        room_id = int(request_data['roomId'])
        seat_id = int(request_data['seatId'])
        update(['seat', 'room'], [seat_id, room_id, info])
        return normal_response(sta_200)

    @ns.expect(seat_to_delete)
    @ns.response(204, "Deleted")
    @ns.response(400, "Bad Request")
    def delete(self):
        request_data = api.payload
        if 'seatId' not in request_data:
            return error_response(sta_400)
        seat_id = int(request_data['seatId'])
        delete(["seat"], [seat_id])
        return normal_response(sta_200)


ns.add_resource(Seat, "/seat", endpoint="Seat")


# Session Model
class Session(Resource):
    @ns.response(200, "Success response", session_info)  # 对应解析文档返回值
    def get(self):
        session_datas = search(['session'], [])
        return get_response(session_datas, sta_200)
    
    @ns.expect(session_to_insert)
    @ns.response(201, "Created")
    @ns.response(400, "Bad Request")
    def post(self):
        request_data = api.payload
        if 'roomId' not in request_data or 'movieId' not in request_data or 'time' not in request_data:
            return error_response(sta_400)
        room_id = request_data['roomId']
        movie_id = request_data['movieId']
        time = request_data['time']
        insert(['session', 'room', 'movie', 'time'], [room_id, movie_id, time])
        return normal_response(sta_201)

    @ns.expect(session_info)
    @ns.response(200, "Success response")
    @ns.response(400, "Bad Request")
    def put(self):
        request_data = api.payload
        if 'sessionId' not in request_data or 'roomId' not in request_data \
                or 'movieId' not in request_data or 'time' not in request_data:
            return error_response(sta_400)
        room_id = request_data['roomId']
        movie_id = request_data['movieId']
        session_id = int(request_data['sessionId'])
        time = request_data['time']
        update(['session', 'room', 'movie', 'time'], [session_id, room_id, movie_id, time])
        return normal_response(sta_200)

    @ns.expect(session_to_delete)
    @ns.response(204, "Deleted")
    @ns.response(400, "Bad Request")
    def delete(self):
        request_data = api.payload
        if 'sessionId' not in request_data:
            return error_response(sta_400)
        session_id = int(request_data['sessionId'])
        delete(['session'], [session_id])
        return normal_response(sta_200)


ns.add_resource(Session, "/session", endpoint="Session")


if __name__ == '__main__':
    app.run()
