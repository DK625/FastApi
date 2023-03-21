from flask_restful import Resource

from ..controllers import user_controller


class todo_list(Resource):
    def post(self):
        return user_controller.create_new_list()

    def get(self):
        return user_controller.get_todo_list()

    def delete(self):
        return user_controller.delete_list()


class todo(Resource):
    def post(self):
        return user_controller.create_new_todo()

    def get(self):
        return user_controller.get_todo()

    def delete(self):
        return user_controller.delete_todo()

    def put(self):
        return user_controller.update_todo()


class Login(Resource):
    def post(self):
        return user_controller.handle_loging()


class sign_up(Resource):
    def post(self):
        return user_controller.sign_up()
