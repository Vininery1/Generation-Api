# models.py
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class Student(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'semester1_grade', 'semester2_grade', 'teacher_name', 'room_number')
