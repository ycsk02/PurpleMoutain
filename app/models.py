# -*- coding: utf-8 -*-

from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()

class CRUD():

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class Nodes(db.Model,CRUD):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(250), nullable=False)
    ipaddr = db.Column(db.String(250), nullable=False)
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    is_active = db.Column(db.Boolean, server_default="false", nullable=False)

    def __init__(self,hostname,is_active):
        self.hostname = hostname
        self.is_active = is_active
"""
create table nodes(
    id int(11) NOT NULL AUTO_INCREMENT,
    hostname varchar(250) COLLATE utf8_bin DEFAULT NULL,
    ipaddr varchar(250) COLLATE utf8_bin DEFAULT NULL,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""


class NodesSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    hostname = fields.String(validate=not_blank)
    ipaddr = fields.String(validate=not_blank)
    is_active = fields.Boolean()


     #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/nodes/"
        else:
            self_link = "/nodes/{}".format(data['id'])
        return {'self': self_link}


    class Meta:
        type_ = 'nodes'
