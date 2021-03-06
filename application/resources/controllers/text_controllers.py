from application.resources.controllers.user_input import user_fields, download_fields
from application.resources.generator.text_generator import InteractionModel
from application.resources.generator.download_model import download_model
from flask_restplus import Resource
from application import api

downloader = api.namespace('downloadmodel', description='Operations to download Model')
generater = api.namespace('generatetext', description='Operations related to Text Generation')


@generater.route('/', endpoint='/generatetext')
class GeneratorController(Resource):
    @generater.doc('list_todo')
    def get(self):
        return 'Generation GET method Called'

    @generater.expect(user_fields, validate=False)
    @generater.doc(responses={
        200: 'Words Generated',
        400: 'Validation Error'
    })
    def post(self):
        json_data = api.payload
        out = json_data['Input Data']
        cls_obj = InteractionModel()
        genrated_data = cls_obj.interact_model(out)
        print(genrated_data)
        return genrated_data


@downloader.route('/', endpoint='/downloadmodel')
class DownloadController(Resource):

    @downloader.expect(download_fields, validate=False)
    @downloader.doc(responses={
        200: 'Model Downloaded',
        400: 'Validation Error'
    })
    def post(self):
        json_data = api.payload
        out = json_data['Model Name']
        return download_model(out)
