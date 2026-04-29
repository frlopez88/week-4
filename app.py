from flask import Flask, jsonify
from database import init_db
from routes.doctors import doctors
from routes.patients import patients
from routes.wards import wards
from routes.appointments import appointments

init_db()

app = Flask(__name__)
app.register_blueprint(doctors, url_prefix="/doctors")
app.register_blueprint(patients, url_prefix="/patients")
app.register_blueprint(wards, url_prefix="/wards")
app.register_blueprint(appointments, url_prefix="/appointments")


@app.route("/")
def home():
    return jsonify({"message": "Server Online"})


if __name__ == "__main__":
    app.run(debug=True)