from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

appointments = Blueprint("appointments", __name__)

@appointments.route("/")
def get_appointments():
    try:
        conn= get_connection()
        cur = conn.cursor(cursor_factory = RealDictCursor)
        cur.execute("""
                        select a.*, 
                        b.name patient_name , 
                        c.name doctor_name
                from hospital.appointments a
                inner join hospital.patients b on a.ssn = b.ssn
                inner join hospital.doctors c on a.staff_id = c.staff_id
                """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
    except Exception as e :
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify(rows)
    
@appointments.route("/", methods=["POST"])
def create_doctor():
    try:
        conn= get_connection()
        cur = conn.cursor()
        data = request.get_json()
        cur.execute("""
                    insert into hospital.appointments
                    (status, appointment_date, ssn, staff_id)
                    values 
                    (%s, %s, %s, %s)
            """, (data["status"],data["appointment_date"], data["ssn"] , data["staff_id"]))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
       return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Created"}), 201
    
@appointments.route("/<int:id>", methods=["PUT"])
def update_doctor(id):
    try:
        conn= get_connection()
        cur = conn.cursor()
        data = request.get_json()
        print(data)
        cur.execute("""
                    update hospital.appointments
                    set status = %s, 
                        appointment_date = %s,
                        ssn = %s,
                        staff_id = %s
                    where appointment_id = %s
            """, (data["status"],data["appointment_date"], data["ssn"] , data["staff_id"], id))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
        return jsonify({"message": f"{e}"}), 500
    else:
        return jsonify({"message": "Object Updated"}), 201
    
@appointments.route("/<int:id>", methods=["DELETE"])
def delete_doctor(id):
    try:
        conn= get_connection()
        cur = conn.cursor()
        cur.execute("""
                    delete from hospital.appointments
                    where appointment_id = %s
            """, (id, ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Deleted"}), 201