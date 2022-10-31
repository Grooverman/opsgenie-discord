#!/usr/bin/env python
# encoding: utf-8
import json
from pprint import pformat
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from urllib3 import PoolManager


# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)


def SendToDiscord(webhook_id, token, message):
    protocol = 'https'
    domain = 'discord.com'
    path = '/api/webhooks/' + str(webhook_id) + '/' + token
    url = protocol + '://' + domain + path
    pool = PoolManager()

    alert_url = ''
    alert_title = (message['alert']['message'] or message['alert']['description'])
    alert_description = (message['alert']['description'] or message['alert']['message'])
    encoded_data = json.dumps(
            {'embeds':[{
                'color': 16711680,
                'title': alert_title,
                'url': alert_url,
                'fields': [
                    {'name': 'Description',
                    'value': alert_description,
                    'inline': True}]
                }]}
            ).encode('utf-8')

    r = pool.request('POST',
            url,
            body=encoded_data,
            headers={'Content-Type': 'application/json'})

    print ('Response Status:', r.status)
    # Header of the response
    print ('Header: ',r.headers['content-type'])
    # Content of the response
    print ('Python: ',len(r.data), r.data )

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Reception(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self, webhook_id, token):
        return jsonify({'message': 'Method not supported.'})

    # corresponds to POST request
    def post(self, webhook_id, token):
        print(pformat(webhook_id))
        print(pformat(token))
        data = request.get_json()
        print(pformat(data))
        SendToDiscord(webhook_id, token, data)

# adding the defined resources along with their corresponding urls
api.add_resource(Reception, '/<int:webhook_id>/<token>')


# driver function
if __name__ == '__main__':
    app.run(debug = True, port=5002)

