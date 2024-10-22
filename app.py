# app.py
from flask import Flask, request, jsonify
from flasgger import Swagger
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
swagger = Swagger(app)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/students', methods=['GET'])
def get_students():
    """
    Retrieve a list of students
    ---
    responses:
      200:
        description: A list of students
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: John Doe
                  age:
                    type: integer
                    example: 20
                  semester1_grade:
                    type: number
                    format: float
                    example: 8.5
                  semester2_grade:
                    type: number
                    format: float
                    example: 7.5
                  teacher_name:
                    type: string
                    example: Mr. Smith
                  room_number:
                    type: string
                    example: A101
    """
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    cursor.close()
    
    students = []
    for row in rows:
        student = {
            'id': row[0],
            'name': row[1],
            'age': row[2],
            'semester1_grade': row[3],
            'semester2_grade': row[4],
            'teacher_name': row[5],
            'room_number': row[6]
        }
        students.append(student)
    
    return jsonify(students)

@app.route('/student', methods=['POST'])
def add_student():
    """
    Add a new student
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: JSON object containing student details
        schema:
          type: object
          properties:
            name:
              type: string
              example: John Doe
            age:
              type: integer
              example: 20
            semester1_grade:
              type: number
              format: float
              example: 8.5
            semester2_grade:
              type: number
              format: float
              example: 7.5
            teacher_name:
              type: string
              example: Mr. Smith
            room_number:
              type: string
              example: A101
    responses:
      200:
        description: Student added successfully
    """
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO students (name, age, semester1_grade, semester2_grade, teacher_name, room_number) VALUES (%s, %s, %s, %s, %s, %s)', 
                   (data['name'], data['age'], data['semester1_grade'], data['semester2_grade'], data['teacher_name'], data['room_number']))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Student added successfully!'})

@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    """
    Update an existing student
    ---
    parameters:
      - in: path
        name: id
        required: true
        description: The ID of the student to update
        schema:
          type: integer
      - in: body
        name: body
        required: true
        description: JSON object containing the student details to update
        schema:
          type: object
          properties:
            name:
              type: string
              example: John Doe
            age:
              type: integer
              example: 20
            semester1_grade:
              type: number
              format: float
              example: 8.5
            semester2_grade:
              type: number
              format: float
              example: 7.5
            teacher_name:
              type: string
              example: Mr. Smith
            room_number:
              type: string
              example: A101
    responses:
      200:
        description: Student updated successfully
    """
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE students SET name=%s, age=%s, semester1_grade=%s, semester2_grade=%s, teacher_name=%s, room_number=%s WHERE id=%s', 
                   (data['name'], data['age'], data['semester1_grade'], data['semester2_grade'], data['teacher_name'], data['room_number'], id))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Student updated successfully!'})

@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    """
    Delete a student
    ---
    parameters:
      - in: path
        name: id
        required: true
        description: The ID of the student to delete
        schema:
          type: integer
    responses:
      200:
        description: Student deleted successfully
    """
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM students WHERE id=%s', (id,))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Student deleted successfully!'})

@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    """
    Get student by ID
    ---
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
          example: 1
    responses:
      200:
        description: Student found successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: John Doe
                age:
                  type: integer
                  example: 20
                semester1_grade:
                  type: number
                  format: float
                  example: 8.5
                semester2_grade:
                  type: number
                  format: float
                  example: 7.5
                teacher_name:
                  type: string
                  example: Mr. Smith
                room_number:
                  type: string
                  example: A101
      404:
        description: Student not found
    """
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM students WHERE id = %s', (id,))
    student = cursor.fetchone()
    cursor.close()

    if student:
        student_data = {
            'id': student[0],
            'name': student[1],
            'age': student[2],
            'semester1_grade': student[3],
            'semester2_grade': student[4],
            'teacher_name': student[5],
            'room_number': student[6]
        }
        return jsonify(student_data)
    else:
        return jsonify({'message': 'Student not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)


