from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Dummy(Resource):
    def get(self):
        return 'Hi!'

api.add_resource(Dummy,'/1')

if __name__ == '__main__':
    app.run()
