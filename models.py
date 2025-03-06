from peewee import *
import datetime
class Tag(Model):
    id = AutoField()
    name = TextField()


class Record(Model):
    id = AutoField()
    created_at = DateTimeField(default=datetime.datetime.now)
    query = TextField()
    output = TextField()
    tags = ManyToManyField(Tag, backref="records")

RecordTagThrough=Record.tags.get_through_model()
class UnTaggedRecord(Model):
    id=AutoField()
    record=ForeignKeyField(Record)

def bind_db(db):
    for i in globals().values():
        if isinstance(i,type) and issubclass(i,Model) and i!=Model:
            i.bind(db)
            i.create_table()

