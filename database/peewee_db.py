from datetime import datetime
from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField, ForeignKeyField, DateTimeField
from config import DB_PATH

db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    user_name = CharField(null=True)
    first_name = CharField(null=True)

class History(BaseModel):
    request_id = AutoField()
    user = ForeignKeyField(User, backref="histories", null=False)
    results = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return 'Номер запроса перевода: <b>{request_id}</b>;\nДата и время запроса: <b>{created_at}</b>;\nРезультат запроса:\n[\n{results}]\n'.format(
            request_id=self.request_id,
            created_at=self.created_at,
            results=self.results
        )

def create_models():
    db.create_tables(BaseModel.__subclasses__())