from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

wards = Blueprint("wards", __name__)

@wards.route("/")
def get_wards():
    try:
        conn= get_connection()
        cur = conn.cursor(cursor_factory = RealDictCursor)
        cur.execute("""
                        select * from hospital.wards
                """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
    except Exception as e :
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify(rows)
    
@wards.route("/", methods=["POST"])
def create_doctor():
    try:
        conn= get_connection()
        cur = conn.cursor()
        data = request.get_json()
        cur.execute("""
                    insert into hospital.wards
                    (ward_name)
                    values 
                    (%s)
            """, (data["ward_name"], ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
       return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Created"}), 201
    
@wards.route("/<int:id>", methods=["PUT"])
def update_doctor(id):
    try:
        conn= get_connection()
        cur = conn.cursor()
        data = request.get_json()
        print(data)
        cur.execute("""
                    update hospital.wards
                    set ward_name = %s
                    where ward_id = %s
            """, (data["ward_name"],  id))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
        return jsonify({"message": f"{e}"}), 500
    else:
        return jsonify({"message": "Object Updated"}), 201
    
@wards.route("/<int:id>", methods=["DELETE"])
def delete_doctor(id):
    try:
        conn= get_connection()
        cur = conn.cursor()
        cur.execute("""
                    delete from hospital.wards
                    where ward_id = %s
            """, (id, ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e :
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Deleted"}), 201