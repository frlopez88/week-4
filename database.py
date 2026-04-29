import psycopg2 , os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        port =os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user= os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        sslmode = os.getenv("DB_SSLMODE")
    )

    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(""" 

                create table if not exists patients 
                (
                    ssn varchar(20) PRIMARY KEY,
                    name varchar(250), 
                    birth_of_date date
                );

                create table  if not exists doctors
                (
                    staff_id serial primary key,
                    name varchar(250), 
                    medical_speciality varchar(100)
                );

                create table  if not exists appointments(
                    appointment_id serial PRIMARY KEY,
                    status varchar(50),
                    appointment_date TIMESTAMP,
                    ssn varchar(20) references patients(ssn),
                    staff_id int references doctors(staff_id)
                );


                create table if not exists wards 
                (
                    ward_id serial primary key,
                    ward_name varchar(100) unique
                );


                create table if not exists bed 
                (
                    bed_id serial primary key,
                    ward_id int references wards(ward_id)
                );


                create table if not exists stays 
                (
                    stay_id serial primary key,
                    admission_date date,
                    discharge_date date,
                    ssn varchar(20) references patients(ssn),
                    bed_id int references bed(bed_id)
                );

        """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Database Ready!✅")