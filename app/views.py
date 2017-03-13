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

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
                schema.validate(raw_dict)
                print raw_dict
                node_dict = raw_dict['data']['attributes']
                node = Nodes(node_dict['hostname'], node_dict['ipaddr'],node_dict['is_active'])
                node.add(node)
                query = Nodes.query.get(node.id)
                results = schema.dump(query).data
                return results, 201

        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 403
                return resp

        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 403
                return resp

api.add_resource(NodesList, '/nodes')
