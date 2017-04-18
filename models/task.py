from mongoengine import *

class Task(Document):
      local_id = StringField();
      name = StringField();
      color = StringField();
      done = BooleanField();