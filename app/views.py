# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, make_response
from app.models import Nodes, NodesSchema, db
from flask_restful import Api, Resource

from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

nodes = Blueprint('nodes',__name__)
schema = NodesSchema()
api = Api(nodes)

class NodesList(Resource):
    def get(self):
        nodes_query = Nodes.query.all()
        results = schema.dump(nodes_query,many=True).data
        #results = schema.dump(nodes_query,many=True).data
        return results


api.add_resource(NodesList, '/nodes')
