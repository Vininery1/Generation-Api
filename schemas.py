# schemas.py
from marshmallow import Schema, fields

class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    semester1_grade = fields.Float(required=True)
    semester2_grade = fields.Float(required=True)
    teacher_name = fields.Str(required=True)
    room_number = fields.Str(required=True)
