from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

doctors = Blueprint("doctors", __name__)

@doctors.route("/")
def get_doctors():
    try:
        conn= get_connection()
        cur = conn.cursor(cursor_factory = RealDictCursor)
        cur.execute("""
                        select * from hospital.doctors
                """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
    except Exception as e :
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify(rows)
    
@doctors.route("/", methods=["POST"])
def create_doctor():
    try:
        conn= get_connection()
        cur = conn.cursor()
        data = request.get_json()
        cur.execute("""
                    insert into hospital.doctors
                    (name, medical_speciality)
                    values 
                    (%s, %s)
            """, (data["name"], data["medical_speciality"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
       return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Created"}), 201
    
@doctors.route("/<int:id>", methods=["PUT"])
def update_doctor(id):
    try:
        conn= get_connection()
        cur = conn.cursor()
        data = request.get_json()
        print(data)
        cur.execute("""
                    update hospital.doctors
                    set name = %s ,
                        medical_speciality = %s
                    where staff_id = %s
            """, (data["name"], data["medical_speciality"], id))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
        return jsonify({"message": f"{e}"}), 500
    else:
        return jsonify({"message": "Object Updated"}), 201
    
@doctors.route("/<int:id>", methods=["DELETE"])
def delete_doctor(id):
    try:
        conn= get_connection()
        cur = conn.cursor()
        cur.execute("""
                    delete from hospital.doctors
                    where staff_id = %s
            """, (id, ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Deleted"}), 201