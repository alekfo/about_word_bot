from datetime import datetime
from peewee import *
from config import DB_PATH

db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    user_name = CharField(null=True)
    first_name = CharField(null=True)
    mailing_flag = BooleanField(default=False)
    lang_for_mailing = CharField(null=False)

class History(BaseModel):
    request_id = AutoField()
    user = ForeignKeyField(User, backref="histories", null=False)
    results = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return 'Дата и время запроса: <b>{created_at}</b>;\nРезультат запроса:\n<i>{results}</i>\n'.format(
            request_id=self.request_id,
            created_at=self.created_at,
            results=self.results
        )

def create_models():
    """
    Функция для создания таблицы базы данных на основе созданных моделей
    :return: None
    """

    db.create_tables(BaseModel.__subclasses__())