from flask import Flask, request
from flask_restful import Resource, Api
from storage_key_value import StorageTempFile


storage = StorageTempFile()


app = Flask(__name__)
api = Api(app, prefix='/api/v1/storage/json')


class GetAllValues(Resource):
    def get(self):
        data = storage.get_values()
        print(data)
        for k, v in data.items():
            if v:
                data[k] = ', '.join(v)
        return data


api.add_resource(GetAllValues, '/all', endpoint='getallvalues')


class GetValue(Resource):
    def get(self):
        args = request.args
        key = args['key']
        value = storage.get_value(key)
        return {key: value}


api.add_resource(GetValue, '/read',  endpoint='getvalue')


class SetValue(Resource):
    def get(self):
        args = request.args
        key = args.get('key')
        value = args.get('val')
        storage.set_value(key, value)
        return f'Success add data {{{key}: {value}}}'


api.add_resource(SetValue, '/write',  endpoint='setvalue')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
