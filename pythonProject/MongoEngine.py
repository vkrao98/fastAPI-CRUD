from mongoengine import StringField, Document

class Docs(Document):
    gtb_rstrnt_name = StringField()
    primary_city = StringField()
    gtb_item_name = StringField()
    state = StringField()
