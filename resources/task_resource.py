from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.task import Task
import mlab

class TaskListRest(Resource):
    @jwt_required()
    def get(self):
        task = Task.objects()
        return mlab.listjson(task)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("local_id", type = str, location ="json")
        parser.add_argument("name",type = str, location = "json")
        parser.add_argument("color",type = str, location = "json")
        parser.add_argument("done",type = bool, location = "json")


        body = parser.parse_args()

        local_id = body["local_id"]
        name = body["name"]
        color = body["color"]
        done = body["done"]

        task = Task(name = name, local_id = local_id, color = color, done = False)
        task.save()

        return mlab.itemjson(task)


class TaskRes(Resource):
    @jwt_required()
    def get(self,task_id):
        task = Task.objects(local_id = task_id)
        return mlab.itemjson(task)
    @jwt_required()
    def delete(self,task_id):
        task = Task.objects(local_id = task_id)
        if task == None:
            return {"Delete": "Task not found"}
        else:
            task.delete()
            return {"Delete": "Successful"}
    @jwt_required()
    def put(self,task_id):
        parse = reqparse.RequestParser()
        parse.add_argument(name="local_id", type=str, location="json")
        parse.add_argument(name="name", type=str, location="json")
        parse.add_argument(name="color", type=str, location="json")
        parse.add_argument(name="done", type=bool, location="json")

        body = parse.parse_args()

        local_id = body["local_id"]
        name = body["name"]
        color = body["color"]
        done = body["done"]

        task = Task.objects().with_id(task_id)
        task.update(local_id = local_id, name = name, color = color, done = done)
        update_task = Task.objects.with_id(task_id)

        return mlab.itemjson(update_task)