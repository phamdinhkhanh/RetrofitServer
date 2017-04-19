from flask import Flask
import mlab
from models.task import Task
from flask_restful import Api
from resources.task_resource import *
from mongoengine import Document, StringField
from flask_jwt import JWT,jwt_required
from login import jwt_init,RegisterRes, LoginCredentials
from models.user import User

mlab.connect()
#Flask co chuc nang tao framework cho app
app = Flask(__name__)
api = Api(app)
jwt = jwt_init(app)
app.config["SECRET_KEY"] = "MY SECRET KEY"

# all_tasks = User.objects()
# for task in all_tasks:
#     print(mlab.itemjson(task))

# for user in User.objects(username = "khanh"):
#     print(mlab.itemjson(user))

@app.route('/')
def hello_world():
    return 'Hello World!'

api.add_resource(TaskListRest,"/tasks")
api.add_resource(TaskRes,"/tasks/<task_id>")
api.add_resource(RegisterRes,"/register")
api.add_resource(LoginCredentials,"/login")

if __name__ == '__main__':
    app.run()
