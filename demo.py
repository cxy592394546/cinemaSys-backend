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
api = Api(app, version='1.0', title='Cinema Microservice', description='APIs of Cinema Microservice', )

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

ns = api.namespace('api', path='/api/', description='APIs of Cinema Microservice')

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
    'info': fields.String(required=True, description='Info of the session')
})
cinema_to_delete = api.model("cId", {
    'cinemaId': fields.Integer(required=True, description='The cinema unique identifier'),
})
room_to_delete = api.model("crId", {
    'cinemaId': fields.Integer(required=True, description='The cinema unique identifier'),
    'roomId': fields.Integer(required=True, description='The room unique identifier'),
})
seat_to_delete = api.model("rsId", {
    'roomId': fields.Integer(required=True, description='The room unique identifier'),
    'seatId': fields.Integer(required=True, description='The seat unique identifier'),
})
session_to_delete = api.model("sId", {
    'sessionId': fields.Integer(required=True, description='The session unique identifier'),
})


# GET METHOD
class GetCinemaInfo(Resource):
    @ns.response(200, "Success response", cinema_info)  # 对应解析文档返回值
    def get(self):
        cinema_datas = search(['cinema'], [])
        return get_response(cinema_datas, sta_200)


ns.add_resource(GetCinemaInfo, "/getCinemaInfo", endpoint="getCinemaInfo")


class GetRoomInfo(Resource):
    parser = reqparse.RequestParser()  # 参数模型
    parser.add_argument('cinemaId', type=int, required=True, help="id")

    @ns.expect(parser)  # 用于解析对应文档参数，
    @ns.response(200, "Success response", room_info)  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def get(self):
        # result = []
        args = int(request.args.get("cinemaId"))
        room_datas = search(['room', 'cinema'], [args])
        # for room_data in room_datas:
        #     if room_data["cinemaId"] == args:
        #         result.append(room_data)
        # if len(result) == 0:
        #     return error_response(sta_400)
        return get_response(room_datas, sta_200)


ns.add_resource(GetRoomInfo, "/getRoomInfo", endpoint="getRoomInfo")


class GetSeatInfo(Resource):
    parser = reqparse.RequestParser()  # 参数模型
    parser.add_argument('roomId', type=int, required=True, help="id")

    @ns.expect(parser)  # 用于解析对应文档参数，
    @ns.response(200, "Success response", seat_info)  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def get(self):
        # result = []
        args = int(request.args.get("roomId"))
        seat_datas = search(['seat', 'cinema'], [args])
        # for seat_data in seat_datas:
        #     if seat_data["roomId"] == args:
        #         result.append(seat_data)
        # if len(result) == 0:
        #     return error_response(sta_400)
        return get_response(seat_datas, sta_200)


ns.add_resource(GetSeatInfo, "/getSeatInfo", endpoint="getSeatInfo")


class GetSessionInfo(Resource):
    @ns.response(200, "Success response", session_info)  # 对应解析文档返回值
    def get(self):
        session_datas = search(['session'], [])
        return get_response(session_datas, sta_200)


ns.add_resource(GetSessionInfo, "/getSessionInfo", endpoint="getSessionInfo")


# POST METHOD
class AddCinema(Resource):
    @ns.expect(cinema_info)
    @ns.marshal_with(cinema_info, code=201)
    @ns.response(201, "Created")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def post(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'cinemaId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        cinema_id = request_data['cinemaId']
        insert(['cinema'], [cinema_id, info])
        return normal_response(sta_201)


ns.add_resource(AddCinema, "/addCinema", endpoint="addCinema")


class AddRoom(Resource):
    @ns.expect(room_info)
    @ns.marshal_with(room_info, code=201)
    @ns.response(201, "Created")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def post(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'roomId' not in request_data or 'cinemaId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        cinema_id = request_data['cinemaId']
        room_id = request_data['roomId']
        insert(['room', 'cinema'], [room_id, cinema_id, info])
        return normal_response(sta_201)


ns.add_resource(AddRoom, "/addRoom", endpoint="addRoom")


class AddSeat(Resource):
    @ns.expect(seat_info)
    @ns.marshal_with(seat_info, code=201)
    @ns.response(201, "Created")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def post(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'seatId' not in request_data or 'roomId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        seat_id = request_data['seatId']
        room_id = request_data['roomId']
        insert(['seat', 'room'], [seat_id, room_id, info])
        return normal_response(sta_201)


ns.add_resource(AddSeat, "/addSeat", endpoint="addSeat")


class AddSession(Resource):
    @ns.expect(session_info)
    @ns.marshal_with(session_info, code=201)
    @ns.response(201, "Created")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def post(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'sessionId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        session_id = request_data['sessionId']
        insert(['session'], [session_id, info])
        return normal_response(sta_201)


ns.add_resource(AddSession, "/addSession", endpoint="addSession")


# PUT METHOD
class EditCinemaInfo(Resource):
    @ns.expect(cinema_info)
    @ns.marshal_with(cinema_info)
    @ns.response(200, "Success response")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def put(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'cinemaId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        cinema_id = int(request_data['cinemaId'])
        update(['cinema'], [cinema_id, info])
        return normal_response(sta_200)


ns.add_resource(EditCinemaInfo, "/editCinemaInfo", endpoint="editCinemaInfo")


class EditRoomInfo(Resource):
    @ns.expect(room_info)
    @ns.marshal_with(room_info)
    @ns.response(200, "Success response")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def put(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'roomId' not in request_data or 'cinemaId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        cinema_id = int(request_data['cinemaId'])
        room_id = int(request_data['room_id'])
        update(['room', 'cinema'], [room_id, cinema_id, info])
        return normal_response(sta_200)


ns.add_resource(EditRoomInfo, "/editRoomInfo", endpoint="editRoomInfo")


class EditSeatInfo(Resource):
    @ns.expect(seat_info)
    @ns.marshal_with(seat_info)
    @ns.response(200, "Success response")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def put(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'seatId' not in request_data or 'roomId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        room_id = int(request_data['roomId'])
        seat_id = int(request_data['seat_id'])
        update(['seat', 'room'], [seat_id, room_id, info])
        return normal_response(sta_200)


ns.add_resource(EditSeatInfo, "/editSeatInfo", endpoint="editSeatInfo")


class EditSessionInfo(Resource):
    @ns.expect(room_info)
    @ns.marshal_with(room_info)
    @ns.response(200, "Success response")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def put(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'sessionId' not in request_data or 'info' not in request_data:
            return error_response(sta_400)
        info = request_data['info']
        session_id = int(request_data['sessionId'])
        update(['session'], [session_id, info])
        return normal_response(sta_200)


ns.add_resource(EditSessionInfo, "/editSessionInfo", endpoint="editSessionInfo")


# DELETE METHOD
class DeleteCinema(Resource):
    @ns.expect(cinema_to_delete)
    @ns.marshal_with(cinema_to_delete)
    @ns.response(204, "Deleted")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def delete(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'cinemaId' not in request_data:
            return error_response(sta_400)
        cinema_id = int(request_data['cinemaId'])
        delete(['cinema'], [cinema_id])
        return normal_response(sta_204)


ns.add_resource(DeleteCinema, "/deleteCinema", endpoint="deleteCinema")


class DeleteRoom(Resource):
    @ns.expect(room_to_delete)
    @ns.marshal_with(room_to_delete)
    @ns.response(204, "Deleted")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def delete(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'roomId' not in request_data or 'cinemaId' not in request_data:
            return error_response(sta_400)
        cinema_id = int(request_data['cinemaId'])
        room_id = int(request_data['room_id'])
        delete(["room", 'cinema'], [room_id, cinema_id])
        return normal_response(sta_200)


ns.add_resource(DeleteRoom, "/deleteRoom", endpoint="deleteRoom")


class DeleteSeat(Resource):
    @ns.expect(seat_to_delete)
    @ns.marshal_with(seat_to_delete)
    @ns.response(204, "Deleted")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def delete(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'seatId' not in request_data or 'roomId' not in request_data:
            return error_response(sta_400)
        room_id = int(request_data['roomId'])
        seat_id = int(request_data['seat_id'])
        delete(["seat", 'room'], [seat_id, room_id])
        return normal_response(sta_200)


ns.add_resource(DeleteSeat, "/deleteSeat", endpoint="deleteSeat")


class DeleteSession(Resource):
    @ns.expect(session_to_delete)
    @ns.marshal_with(session_to_delete)
    @ns.response(204, "Deleted")  # 对应解析文档返回值
    @ns.response(400, "Bad Request")
    def delete(self):
        # if request.headers['Content-Type'] == 'application/json':
        request_data = api.payload
        if 'sessionId' not in request_data:
            return error_response(sta_400)
        session_id = int(request_data['sessionId'])
        delete(['session'], [session_id])
        return normal_response(sta_200)


ns.add_resource(DeleteSession, "/deleteSession", endpoint="deleteSession")


if __name__ == '__main__':
    app.run()
