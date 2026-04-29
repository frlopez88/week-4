from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

patients = Blueprint("patients", __name__)

@patients.route("/")
def get_patients():
    try:
        conn= get_connection()
        cur = conn.cursor(cursor_factory = RealDictCursor)
        cur.execute("""
                        select * from hospital.patients
                """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
    except Exception as e :
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify(rows)
    
@patients.route("/", methods=["POST"])
def create_doctor():
    try:
        conn= get_connection()
        cur = conn.cursor()
        data = request.get_json()
        cur.execute("""
                    insert into hospital.patients
                    (ssn, name, birth_of_date)
                    values 
                    (%s, %s, %s)
            """, (data["ssn"], data["name"], data["birth_of_date"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
       return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Created"}), 201
    
@patients.route("/<string:id>", methods=["PUT"])
def update_doctor(id):
    try:
        conn= get_connection()
        cur = conn.cursor()
        data = request.get_json()
        print(data)
        cur.execute("""
                    update hospital.patients
                    set name = %s ,
                        birth_of_date = %s
                    where ssn = %s
            """, (data["name"], data["birth_of_date"], id))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
        return jsonify({"message": f"{e}"}), 500
    else:
        return jsonify({"message": "Object Updated"}), 201
    
@patients.route("/<string:id>", methods=["DELETE"])
def delete_doctor(id):
    try:
        conn= get_connection()
        cur = conn.cursor()
        cur.execute("""
                    delete from hospital.patients
                    where ssn = %s
            """, (id, ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Deleted"}), 201