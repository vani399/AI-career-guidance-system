from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import csv
import os
import csv
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from flask import render_template, session, redirect, send_from_directory
import os
import math
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
print("Flask using database:", os.path.abspath("database.db"))

print("USING DATABASE AT:", os.path.abspath("database.db"))
app = Flask(__name__)
app.secret_key = "career_advisor_secret_key"
DATABASE = "database.db"

# ------------------- DATABASE CONNECTION -------------------
def get_db():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row  # <-- makes rows behave like dicts
    return con


# ================= EMAIL CONFIG =================
EMAIL_ADDRESS = "careerhelp577@gmail.com"
EMAIL_PASSWORD = "okuajzvrxbyddmsr"

# ================= DATABASE INITIALIZATION =================
def insert_career_questions():

    con = get_db()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM career_questions")
    count = cur.fetchone()[0]

    # if questions already exist, don't insert again
    if count > 0:
        con.close()
        return

    questions = [

("I enjoy explaining complex topics to classmates and helping them understand difficult subjects clearly.",5,0,0,0,0,0,0,1,0,0,2,0,0),
("Helping others learn new things gives me satisfaction.",5,0,0,0,0,0,0,0,0,0,2,0,0),
("I like solving logical puzzles and challenging mathematical problems.",0,0,0,0,0,0,3,3,5,0,0,2,0),
("Scientific discoveries and experiments make me curious.",0,0,0,0,2,0,2,5,2,0,0,0,0),
("I enjoy designing machines or technological systems.",0,0,0,0,0,0,5,3,2,0,0,2,0),
("Working with computers and developing software interests me.",0,0,0,0,0,0,3,2,2,0,0,5,0),
("I enjoy analyzing numbers and identifying patterns in data.",0,0,0,0,0,0,2,3,5,1,0,2,0),
("Learning about how businesses operate fascinates me.",0,5,0,0,0,0,0,0,0,4,0,0,0),
("I like managing budgets or financial records.",0,4,0,0,0,0,0,0,0,5,0,0,0),
("I enjoy convincing people and presenting ideas.",0,5,0,0,0,0,0,0,0,3,0,0,0),
("Cooking and experimenting with recipes excites me.",0,0,5,0,0,0,0,0,0,0,0,0,0),
("Planning meals and organizing food preparation interests me.",0,1,5,0,0,0,0,0,0,0,0,0,0),
("Understanding laws and justice interests me.",0,0,0,5,0,0,0,0,0,0,2,0,2),
("I enjoy debates and defending arguments.",0,0,0,5,0,0,0,0,0,0,3,0,1),
("I want a profession where I help treat sick people.",0,0,0,0,5,4,0,2,0,0,0,0,0),
("Learning about the human body and medicine interests me.",0,0,0,0,5,4,0,3,0,0,0,0,0),
("Caring for people and helping them recover gives me happiness.",0,0,0,0,4,5,0,0,0,0,1,0,0),
("Working in laboratories and research interests me.",0,0,0,0,3,2,1,5,0,0,0,0,0),
("Writing essays, poems, or stories interests me.",2,0,0,0,0,0,0,0,0,0,5,0,0),
("Reading literature or history excites me.",2,0,0,0,0,0,0,0,0,0,5,0,0),
("Expressing ideas through art or creativity excites me.",2,0,0,0,0,0,0,0,0,0,5,0,0),
("Understanding government policies interests me.",0,0,0,2,0,0,0,0,0,0,1,0,5),
("Serving the country through government jobs interests me.",0,0,0,2,0,0,0,0,0,0,1,0,5),
("Discussing social issues interests me.",1,0,0,2,0,0,0,0,0,0,3,0,5),
("Using technology to solve problems excites me.",0,0,0,0,0,0,4,3,2,0,0,5,0),
("Learning new computer tools excites me.",0,0,0,0,0,0,3,2,2,0,0,5,0),
("Teaching younger students interests me.",5,0,0,0,0,0,0,0,0,0,2,0,0),
("Working in teams to complete projects excites me.",2,3,0,0,0,0,3,2,1,1,1,1,1),
("Planning and organizing activities is my strength.",2,4,0,0,0,0,1,0,0,3,1,0,1),
("I prefer careers where I continuously learn new knowledge.",2,2,0,0,1,1,2,4,3,0,2,1,0)

]

    cur.executemany("""
    INSERT INTO career_questions 
    (question, teaching,business,chef,law,doctor,nurse,engineering,science,maths,commerce,arts,it,government)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, questions)

    con.commit()
    con.close()


def init_db():
    con = get_db()
    cur = con.cursor()

    # ================= CREATE TABLES =================

    # Career Questions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS career_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            teaching INTEGER,
            business INTEGER,
            chef INTEGER,
            law INTEGER,
            doctor INTEGER,
            nurse INTEGER,
            engineering INTEGER,
            science INTEGER,
            maths INTEGER,
            commerce INTEGER,
            arts INTEGER,
            it INTEGER,
            government INTEGER
        )
    """)

    # Users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            district TEXT,
            qualification TEXT
        )
    """)

    # ================= ADD ADMIN USER =================
    cur.execute("SELECT COUNT(*) FROM users WHERE email='admin@example.com'")
    if cur.fetchone()[0] == 0:
        admin_password = generate_password_hash("admin123")
        cur.execute("""
            INSERT INTO users (name, email, password, district, qualification)
            VALUES (?, ?, ?, ?, ?)
        """, ("Admin", "admin@example.com", admin_password, "N/A", "Admin"))

    # Quiz Questions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            science_score INTEGER,
            commerce_score INTEGER,
            arts_score INTEGER
        )
    """)

    # Courses
    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            duration TEXT,
            eligibility TEXT,
            stream TEXT,
            level TEXT
        )
    """)

    # Skills
    cur.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            skill_name TEXT
        )
    """)

    # Colleges
    cur.execute("""
        CREATE TABLE IF NOT EXISTS colleges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            district TEXT
        )
    """)

    # College-Course Mapping
    cur.execute("""
        CREATE TABLE IF NOT EXISTS college_courses (
            college_id INTEGER,
            course_id INTEGER
        )
    """)

    # ================= ADMIN ANALYTICS TABLES =================

    # Login History
    cur.execute("""
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Quiz Attempts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            science_score INTEGER,
            commerce_score INTEGER,
            arts_score INTEGER,
            attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Course Views
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_id INTEGER,
            view_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Skill Views
    cur.execute("""
        CREATE TABLE IF NOT EXISTS skill_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_id INTEGER,
            view_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Download Logs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS download_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT,
            download_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Page Visits
    cur.execute("""
        CREATE TABLE IF NOT EXISTS page_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            page_name TEXT,
            visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ================= KNN TRAINING DATA =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_training (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teaching INTEGER,
        business INTEGER,
        chef INTEGER,
        law INTEGER,
        doctor INTEGER,
        nurse INTEGER,
        engineering INTEGER,
        science INTEGER,
        maths INTEGER,
        commerce INTEGER,
        arts INTEGER,
        it INTEGER,
        government INTEGER,
        preferred_course TEXT,
        college_type TEXT
    )
    """)

    # Delete old training data
    cur.execute("DELETE FROM student_training")

    training_data = [
# ------------------- ENGINEERING (40 rows) -------------------
(1,0,0,0,0,0,5,4,5,0,0,3,0,'B.Tech Computer Science','Private'),
(1,0,0,0,0,0,5,4,4,0,0,2,0,'B.Tech Mechanical','Private'),
(0,0,0,0,0,0,4,5,5,0,0,1,0,'B.Tech Civil','Government'),
(0,0,0,0,0,0,5,5,4,0,0,3,0,'B.Tech IT','Private'),
(0,0,0,0,0,0,4,4,5,0,0,2,0,'B.Tech Electrical','Government'),
(0,0,0,0,0,0,5,4,5,0,0,4,0,'B.Tech Electronics','Private'),
(0,0,0,0,0,0,4,5,4,0,0,2,0,'B.Tech Mechanical','Private'),
(0,0,0,0,0,0,5,4,5,0,0,3,0,'B.Tech Civil','Private'),
(0,0,0,0,0,0,4,4,4,0,0,3,0,'B.Tech IT','Government'),
(0,0,0,0,0,0,5,5,5,0,0,4,0,'B.Tech Computer Science','Private'),
(1,0,0,0,0,0,4,5,5,0,0,3,0,'B.Tech Mechanical','Private'),
(1,0,0,0,0,0,5,4,5,0,0,3,0,'B.Tech Civil','Government'),
(0,0,0,0,0,0,4,5,4,0,0,2,0,'B.Tech Electrical','Private'),
(0,0,0,0,0,0,5,4,5,0,0,3,0,'B.Tech IT','Private'),
(0,0,0,0,0,0,4,4,4,0,0,2,0,'B.Tech Computer Science','Private'),
(1,0,0,0,0,0,5,5,4,0,0,3,0,'B.Tech Mechanical','Private'),
(1,0,0,0,0,0,5,4,4,0,0,2,0,'B.Tech Civil','Government'),
(0,0,0,0,0,0,4,5,5,0,0,1,0,'B.Tech Electrical','Private'),
(0,0,0,0,0,0,5,5,4,0,0,3,0,'B.Tech IT','Private'),
(0,0,0,0,0,0,4,4,5,0,0,2,0,'B.Tech Computer Science','Private'),
(0,0,0,0,0,0,5,4,5,0,0,4,0,'B.Tech Mechanical','Private'),
(0,0,0,0,0,0,4,5,4,0,0,2,0,'B.Tech Civil','Government'),
(0,0,0,0,0,0,5,4,5,0,0,3,0,'B.Tech Electrical','Private'),
(0,0,0,0,0,0,4,4,4,0,0,3,0,'B.Tech IT','Private'),
(0,0,0,0,0,0,5,5,5,0,0,4,0,'B.Tech Computer Science','Private'),
(0,0,0,0,0,0,4,5,5,0,0,3,0,'B.Tech Mechanical','Private'),
(0,0,0,0,0,0,5,4,5,0,0,3,0,'B.Tech Civil','Government'),
(0,0,0,0,0,0,4,5,4,0,0,2,0,'B.Tech Electrical','Private'),
(0,0,0,0,0,0,5,4,5,0,0,3,0,'B.Tech IT','Private'),
(1,0,0,0,0,0,4,4,4,0,0,2,0,'B.Tech Computer Science','Private'),
(1,0,0,0,0,0,5,5,4,0,0,3,0,'B.Tech Mechanical','Private'),
(1,0,0,0,0,0,5,4,4,0,0,2,0,'B.Tech Civil','Government'),
(0,0,0,0,0,0,4,5,5,0,0,1,0,'B.Tech Electrical','Private'),
(0,0,0,0,0,0,5,5,4,0,0,3,0,'B.Tech IT','Private'),
(0,0,0,0,0,0,4,4,5,0,0,2,0,'B.Tech Computer Science','Private'),
(0,0,0,0,0,0,5,4,5,0,0,4,0,'B.Tech Mechanical','Private'),
(0,0,0,0,0,0,4,5,4,0,0,2,0,'B.Tech Civil','Government'),
(0,0,0,0,0,0,5,4,5,0,0,3,0,'B.Tech Electrical','Private'),
(0,0,0,0,0,0,4,4,4,0,0,3,0,'B.Tech IT','Private'),

# ------------------- MEDICAL (30 rows) -------------------
(0,0,0,0,5,4,1,4,2,0,0,0,0,'MBBS','Government'),
(0,0,0,0,4,5,0,3,1,0,0,0,0,'B.Sc Nursing','Government'),
(0,0,0,0,4,3,0,3,1,0,0,0,0,'B.Pharm','Private'),
(0,0,0,0,5,3,0,3,2,0,0,0,0,'BDS','Government'),
(0,0,0,0,4,4,0,3,1,0,0,0,0,'Physiotherapy','Private'),
(0,0,0,0,5,4,1,4,2,0,0,0,0,'MBBS','Government'),
(0,0,0,0,4,5,0,3,1,0,0,0,0,'B.Sc Nursing','Private'),
(0,0,0,0,4,3,0,3,1,0,0,0,0,'B.Pharm','Private'),
(0,0,0,0,5,3,0,3,2,0,0,0,0,'BDS','Government'),
(0,0,0,0,4,4,0,3,1,0,0,0,0,'Physiotherapy','Private'),
(0,0,0,0,5,4,1,4,2,0,0,0,0,'MBBS','Government'),
(0,0,0,0,4,5,0,3,1,0,0,0,0,'B.Sc Nursing','Government'),
(0,0,0,0,4,3,0,3,1,0,0,0,0,'B.Pharm','Private'),
(0,0,0,0,5,3,0,3,2,0,0,0,0,'BDS','Government'),
(0,0,0,0,4,4,0,3,1,0,0,0,0,'Physiotherapy','Private'),
(0,0,0,0,5,4,1,4,2,0,0,0,0,'MBBS','Government'),
(0,0,0,0,4,5,0,3,1,0,0,0,0,'B.Sc Nursing','Private'),
(0,0,0,0,4,3,0,3,1,0,0,0,0,'B.Pharm','Private'),
(0,0,0,0,5,3,0,3,2,0,0,0,0,'BDS','Government'),
(0,0,0,0,4,4,0,3,1,0,0,0,0,'Physiotherapy','Private'),
(0,0,0,0,5,4,1,4,2,0,0,0,0,'MBBS','Government'),
(0,0,0,0,4,5,0,3,1,0,0,0,0,'B.Sc Nursing','Government'),
(0,0,0,0,4,3,0,3,1,0,0,0,0,'B.Pharm','Private'),
(0,0,0,0,5,3,0,3,2,0,0,0,0,'BDS','Government'),
(0,0,0,0,4,4,0,3,1,0,0,0,0,'Physiotherapy','Private'),
(0,0,0,0,5,4,1,4,2,0,0,0,0,'MBBS','Government'),
(0,0,0,0,4,5,0,3,1,0,0,0,0,'B.Sc Nursing','Private'),
(0,0,0,0,4,3,0,3,1,0,0,0,0,'B.Pharm','Private'),
(0,0,0,0,5,3,0,3,2,0,0,0,0,'BDS','Government'),
(0,0,0,0,4,4,0,3,1,0,0,0,0,'Physiotherapy','Private'),
# ------------------- COMMERCE (30 rows) -------------------
(0,5,0,0,0,0,0,0,0,5,0,0,0,'BBA','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'BBA Finance','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'BBA Marketing','Private'),
(0,5,0,0,0,0,0,0,0,5,0,0,0,'B.Com','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'B.Com Accounting','Private'),
(0,4,0,0,0,0,0,0,0,4,0,0,0,'B.Com Banking','Private'),
(0,5,0,0,0,0,0,0,0,5,0,0,0,'BBA','Private'),
(0,4,0,0,0,0,0,0,0,4,0,0,0,'BBA Finance','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'BBA Marketing','Private'),
(0,5,0,0,0,0,0,0,0,5,0,0,0,'B.Com','Private'),
(0,4,0,0,0,0,0,0,0,4,0,0,0,'B.Com Accounting','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'B.Com Banking','Private'),
(0,5,0,0,0,0,0,0,0,5,0,0,0,'BBA','Private'),
(0,4,0,0,0,0,0,0,0,4,0,0,0,'BBA Finance','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'BBA Marketing','Private'),
(0,5,0,0,0,0,0,0,0,5,0,0,0,'B.Com','Private'),
(0,4,0,0,0,0,0,0,0,4,0,0,0,'B.Com Accounting','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'B.Com Banking','Private'),
(0,5,0,0,0,0,0,0,0,5,0,0,0,'BBA','Private'),
(0,4,0,0,0,0,0,0,0,4,0,0,0,'BBA Finance','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'BBA Marketing','Private'),
(0,5,0,0,0,0,0,0,0,5,0,0,0,'B.Com','Private'),
(0,4,0,0,0,0,0,0,0,4,0,0,0,'B.Com Accounting','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'B.Com Banking','Private'),
(0,5,0,0,0,0,0,0,0,5,0,0,0,'BBA','Private'),
(0,4,0,0,0,0,0,0,0,4,0,0,0,'BBA Finance','Private'),
(0,4,0,0,0,0,0,0,0,5,0,0,0,'BBA Marketing','Private'),
(0,5,0,0,0,0,0,0,0,5,0,0,0,'B.Com','Private'),
(0,4,0,0,0,0,0,0,0,4,0,0,0,'B.Com Accounting','Private'),

# ------------------- IT (20 rows) -------------------
(0,0,0,0,0,0,3,4,4,0,0,5,0,'BCA','Private'),
(0,0,0,0,0,0,2,4,4,0,0,5,0,'B.Sc Computer Science','Private'),
(0,0,0,0,0,0,2,4,3,0,0,5,0,'B.Sc Data Science','Private'),
(0,0,0,0,0,0,3,4,4,0,0,5,0,'Software Engineering','Private'),
(0,0,0,0,0,0,3,4,4,0,0,5,0,'BCA','Private'),
(0,0,0,0,0,0,3,4,3,0,0,5,0,'B.Sc Computer Science','Private'),
(0,0,0,0,0,0,3,4,3,0,0,5,0,'Data Science','Private'),
(0,0,0,0,0,0,3,4,4,0,0,5,0,'Software Engineering','Private'),
(0,0,0,0,0,0,3,4,4,0,0,5,0,'BCA','Private'),
(0,0,0,0,0,0,3,4,3,0,0,5,0,'B.Sc Computer Science','Private'),
(0,0,0,0,0,0,3,4,4,0,0,5,0,'Software Engineering','Private'),
(0,0,0,0,0,0,2,4,3,0,0,5,0,'B.Sc Data Science','Private'),
(0,0,0,0,0,0,3,4,4,0,0,5,0,'BCA','Private'),
(0,0,0,0,0,0,3,4,3,0,0,5,0,'B.Sc Computer Science','Private'),
(0,0,0,0,0,0,2,4,3,0,0,5,0,'Data Science','Private'),
(0,0,0,0,0,0,3,4,4,0,0,5,0,'Software Engineering','Private'),
(0,0,0,0,0,0,3,4,4,0,0,5,0,'BCA','Private'),
(0,0,0,0,0,0,3,4,3,0,0,5,0,'B.Sc Computer Science','Private'),
(0,0,0,0,0,0,3,4,3,0,0,5,0,'Data Science','Private'),
(0,0,0,0,0,0,3,4,4,0,0,5,0,'Software Engineering','Private'),

# ------------------- ARTS / TEACHING / LAW / GOVERNMENT / HOTEL (20 rows) -------------------
(3,0,0,0,0,0,0,1,0,1,5,0,1,'BA English','Government'),
(2,0,0,0,0,0,0,1,0,1,5,0,1,'BA History','Government'),
(2,0,0,0,0,0,0,1,0,1,5,0,1,'BA Sociology','Government'),
(1,0,0,5,0,0,0,0,0,0,2,0,5,'BA LLB','Government'),
(1,0,0,4,0,0,0,0,0,0,2,0,5,'LLB','Government'),
(5,0,0,0,0,0,1,2,2,0,3,0,0,'B.Ed','Government'),
(0,1,5,0,0,0,0,0,0,1,1,0,0,'Hotel Management','Private'),
(2,0,0,1,0,0,0,1,1,0,1,0,5,'UPSC Preparation','Government'),
(2,0,0,1,0,0,0,1,1,0,1,0,5,'TNPSC Preparation','Government'),
(2,0,0,1,0,0,0,1,1,0,1,0,5,'SSC Preparation','Government'),
(3,0,0,0,0,0,0,1,0,1,5,0,1,'BA Economics','Government'),
(3,0,0,0,0,0,0,1,0,1,5,0,1,'BA Political Science','Government'),
(1,0,0,5,0,0,0,0,0,0,2,0,5,'B.Sc Education','Government'),
(0,1,5,0,0,0,0,0,0,1,1,0,0,'Diploma in Hotel Management','Private'),
(1,0,0,4,0,0,0,0,0,0,2,0,5,'LLM','Government'),
(5,0,0,0,0,0,1,2,2,0,3,0,0,'B.Ed Special Education','Government'),
(2,0,0,1,0,0,0,1,1,0,1,0,5,'Police Exam Preparation','Government'),
(2,0,0,1,0,0,0,1,1,0,1,0,5,'Railway Exam Preparation','Government'),
(3,0,0,0,0,0,0,1,0,1,5,0,1,'BA Fine Arts','Government'),
(0,1,5,0,0,0,0,0,0,1,1,0,0,'Hospitality Management','Private')
]

    cur.executemany("""
    INSERT INTO student_training (
        teaching,business,chef,law,doctor,nurse,
        engineering,science,maths,commerce,
        arts,it,government,
        preferred_course,college_type
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, training_data)

    # INSERT COURSES IF NONE EXIST
    cur.execute("SELECT COUNT(*) FROM courses")
    if cur.fetchone()[0] == 0:
        courses = [

("Diploma in Mechanical Engineering","3 Years","Passed 10th","science","after_10th"),
("Diploma in Civil Engineering","3 Years","Passed 10th","science","after_10th"),
("Diploma in Electrical Engineering","3 Years","Passed 10th","science","after_10th"),
("Diploma in Computer Engineering","3 Years","Passed 10th","science","after_10th"),
("Diploma in Automobile Engineering","3 Years","Passed 10th","science","after_10th"),
("ITI Electrician","2 Years","Passed 10th","science","after_10th"),
("ITI Fitter","2 Years","Passed 10th","science","after_10th"),
("ITI Mechanic","2 Years","Passed 10th","science","after_10th"),
("ITI Welder","1 Year","Passed 10th","science","after_10th"),
("Diploma in Agriculture","2 Years","Passed 10th","science","after_10th"),

("Diploma in Fashion Design","2 Years","Passed 10th","arts","after_10th"),
("Diploma in Interior Design","2 Years","Passed 10th","arts","after_10th"),
("Diploma in Fine Arts","2 Years","Passed 10th","arts","after_10th"),
("Diploma in Photography","1 Year","Passed 10th","arts","after_10th"),
("Diploma in Graphic Design","2 Years","Passed 10th","arts","after_10th"),
("Diploma in Hotel Management","3 Years","Passed 10th","arts","after_10th"),
("Diploma in Culinary Arts","2 Years","Passed 10th","arts","after_10th"),

("Diploma in Business Administration","2 Years","Passed 10th","commerce","after_10th"),
("Diploma in Accounting","2 Years","Passed 10th","commerce","after_10th"),
("Diploma in Banking","2 Years","Passed 10th","commerce","after_10th"),
("Diploma in Retail Management","2 Years","Passed 10th","commerce","after_10th"),

("B.Tech Computer Science","4 Years","12th with Maths","science","after_12th"),
("B.Tech Mechanical Engineering","4 Years","12th with Maths","science","after_12th"),
("B.Tech Civil Engineering","4 Years","12th with Maths","science","after_12th"),
("B.Tech Electrical Engineering","4 Years","12th with Maths","science","after_12th"),
("B.Tech Information Technology","4 Years","12th with Maths","science","after_12th"),

("B.Sc Computer Science","3 Years","12th","science","after_12th"),
("B.Sc Physics","3 Years","12th Science","science","after_12th"),
("B.Sc Chemistry","3 Years","12th Science","science","after_12th"),
("B.Sc Mathematics","3 Years","12th Maths","science","after_12th"),
("B.Sc Biotechnology","3 Years","12th Biology","science","after_12th"),
("B.Sc Microbiology","3 Years","12th Biology","science","after_12th"),

("BCA","3 Years","12th","science","after_12th"),
("B.Sc Data Science","3 Years","12th","science","after_12th"),

("MBBS","5.5 Years","12th Biology + NEET","science","after_12th"),
("BDS","5 Years","12th Biology + NEET","science","after_12th"),
("B.Sc Nursing","4 Years","12th Biology","science","after_12th"),
("B.Pharm","4 Years","12th Biology/Maths","science","after_12th"),
("BPT (Physiotherapy)","4 Years","12th Biology","science","after_12th")

        ]

        cur.executemany("""
        INSERT INTO courses (name, duration, eligibility, stream, level)
        VALUES (?, ?, ?, ?, ?)
        """, courses)

    con.commit()
    con.close()


# ================= INSERT SKILLS (NEW – RUNS ONCE) =================

def insert_sample_skills():
    con = get_db()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM skills")
    if cur.fetchone()[0] > 0:
        con.close()
        return

    skills_map = {

        "B.Tech Computer Science": [
            "Python Programming", "Java Programming", "C++ Programming",
            "Data Structures", "Algorithms", "Web Development",
            "Database Management", "Operating Systems",
            "Computer Networks", "Problem Solving",
            "Software Development", "Debugging",
            "Cloud Computing", "Cyber Security"
        ],

        "B.Sc Computer Science": [
            "C Programming", "Java Basics", "Python Programming",
            "Algorithms", "Data Structures", "SQL",
            "Database Management", "Web Development",
            "Networking Basics", "Problem Solving"
        ],

        "Diploma in Computer Engineering": [
            "Hardware Basics", "Networking", "Embedded Systems",
            "Basic Programming", "Computer Assembly",
            "Troubleshooting", "Operating Systems",
            "Electronics Basics"
        ],

        "BBA": [
            "Business Communication", "Management Skills",
            "Marketing Basics", "Leadership",
            "Team Management", "Strategic Thinking",
            "Presentation Skills", "Entrepreneurship",
            "Decision Making"
        ],

        "B.Com": [
            "Accounting", "Financial Analysis", "Taxation",
            "Business Law", "Banking Basics",
            "Tally Software", "Auditing",
            "Financial Planning", "Economics"
        ],

        "BA English": [
            "Creative Writing", "Communication Skills",
            "Critical Thinking", "Content Writing",
            "Public Speaking", "Literature Analysis",
            "Editing", "Story Writing"
        ]
    }

    for course, skills in skills_map.items():
        cur.execute("SELECT id FROM courses WHERE name=?", (course,))
        row = cur.fetchone()

        if row:
            for skill in skills:
                cur.execute(
                    "INSERT INTO skills (course_id, skill_name) VALUES (?, ?)",
                    (row[0], skill)
                )

    con.commit()
    con.close()


init_db()
insert_sample_skills()

def knn_predict(scores, k=3):

    con = get_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM student_training")
    data = cur.fetchall()

    distances = []

    for row in data:

        distance = math.sqrt(
            (scores["teaching"] - row["teaching"])**2 +
            (scores["business"] - row["business"])**2 +
            (scores["chef"] - row["chef"])**2 +
            (scores["law"] - row["law"])**2 +
            (scores["doctor"] - row["doctor"])**2 +
            (scores["nurse"] - row["nurse"])**2 +
            (scores["engineering"] - row["engineering"])**2 +
            (scores["science"] - row["science"])**2 +
            (scores["maths"] - row["maths"])**2 +
            (scores["commerce"] - row["commerce"])**2 +
            (scores["arts"] - row["arts"])**2 +
            (scores["it"] - row["it"])**2 +
            (scores["government"] - row["government"])**2
        )

        distances.append((distance, row["preferred_course"], row["college_type"]))

    distances.sort(key=lambda x: x[0])

    top_k = distances[:k]

    course_votes = {}
    college_votes = {}

    for d in top_k:

        course = d[1]
        college = d[2]

        course_votes[course] = course_votes.get(course,0) + 1
        college_votes[college] = college_votes.get(college,0) + 1

    predicted_course = max(course_votes, key=course_votes.get)
    predicted_college = max(college_votes, key=college_votes.get)

    return predicted_course, predicted_college

# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form["password"] != request.form["confirm_password"]:
            return render_template("register.html", error="Passwords do not match")

        hashed_password = generate_password_hash(request.form["password"])

        try:
            con = get_db()
            cur = con.cursor()
            cur.execute("""
                INSERT INTO users (name, email, password, district, qualification)
                VALUES (?, ?, ?, ?, ?)
            """, (
                request.form["name"],
                request.form["email"],
                hashed_password,
                request.form["district"],
                request.form["qualification"]
            ))
            con.commit()
            con.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Email already registered")

    return render_template("register.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT id, password FROM users WHERE email=?", (request.form["email"],))
        user = cur.fetchone()
        con.close()

        if user and check_password_hash(user[1], request.form["password"]):
            session.clear()
            session["user_id"] = user[0]
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid login credentials")

    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

#=======streams=============
CAREER_TO_STREAM = {
    "science": "science",
    "engineering": "science",
    "doctor": "science",
    "nurse": "science",
    "maths": "science",
    "it": "science",

    "commerce": "commerce",
    "business": "commerce",

    "arts": "arts",
    "teaching": "arts",
    "law": "arts",
    "government": "arts",
    "chef": "arts"
}

CAREER_SKILLS = {

    "science": [
        "Analytical Thinking",
        "Problem Solving",
        "Research Skills",
        "Mathematics",
        "Critical Thinking"
    ],

    "engineering": [
        "Programming",
        "Mathematics",
        "Problem Solving",
        "Technical Design",
        "Logical Thinking"
    ],

    "doctor": [
        "Biology Knowledge",
        "Patient Care",
        "Attention to Detail",
        "Communication",
        "Decision Making"
    ],

    "it": [
        "Programming",
        "Data Structures",
        "Database Management",
        "Problem Solving",
        "Debugging"
    ],

    "business": [
        "Leadership",
        "Financial Management",
        "Communication",
        "Strategic Thinking",
        "Marketing"
    ],

    "commerce": [
        "Accounting",
        "Financial Analysis",
        "Business Communication",
        "Economics",
        "Data Interpretation"
    ],

    "arts": [
        "Creativity",
        "Communication",
        "Critical Thinking",
        "Writing Skills",
        "Public Speaking"
    ],

    "law": [
        "Legal Knowledge",
        "Argumentation",
        "Critical Thinking",
        "Research",
        "Public Speaking"
    ],

    "chef": [
        "Cooking Techniques",
        "Creativity",
        "Food Presentation",
        "Time Management",
        "Kitchen Management"
    ]
}

def save_training_data(scores, course, college):

    con = get_db()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO student_training (
            teaching,business,chef,law,doctor,nurse,
            engineering,science,maths,commerce,
            arts,it,government,
            preferred_course,college_type
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (

        scores.get("teaching",0),
        scores.get("business",0),
        scores.get("chef",0),
        scores.get("law",0),
        scores.get("doctor",0),
        scores.get("nurse",0),
        scores.get("engineering",0),
        scores.get("science",0),
        scores.get("maths",0),
        scores.get("commerce",0),
        scores.get("arts",0),
        scores.get("it",0),
        scores.get("government",0),
        course,
        college
    ))

    con.commit()
    con.close()

# ------------------ QUIZ ------------------
@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if "user_id" not in session:
        return redirect("/login")

    con = get_db()
    cur = con.cursor()

    fields = [
        "teaching","business","chef","law","doctor","nurse",
        "engineering","science","maths","commerce","arts","it","government"
    ]

    # GET ALL QUESTIONS
    cur.execute("SELECT * FROM career_questions ORDER BY RANDOM()")
    questions = cur.fetchall()

    if request.method == "POST":

        scores = {f:0 for f in fields}

        for q in questions:

            qid = q[0]
            weights = dict(zip(fields, q[2:]))

            answer = int(request.form.get(f"answer_{qid}", 0))

            for field in fields:
                scores[field] += weights[field] * answer

        session["career_scores"] = {str(k): int(v) for k, v in scores.items()}

        return redirect("/recommendation")

    return render_template(
        "quiz.html",
        questions=questions,
        total=len(questions)
    )


CAREER_RECOMMENDATIONS = {
    "science": [
        "B.Sc Physics / Chemistry",
        "Research Scientist",
        "Laboratory Technician",
        "ISRO / DRDO Exams"
    ],

    "engineering": [
        "B.Tech (Engineering)",
        "Diploma in Engineering",
        "Software Developer",
        "Public Sector (GATE → PSU)"
    ],

    "doctor": [
        "MBBS",
        "BDS",
        "Allied Health Sciences",
        "NEET Preparation"
    ],

    "nurse": [
        "B.Sc Nursing",
        "GNM Nursing",
        "Hospital Administration"
    ],

    "commerce": [
        "B.Com",
        "Chartered Accountant (CA)",
        "Cost Accountant (CMA)",
        "Bank Exams"
    ],

    "business": [
        "BBA",
        "MBA",
        "Entrepreneurship",
        "Startup / Small Business"
    ],

    "arts": [
        "BA English / History",
        "Journalism",
        "Public Administration",
        "Social Work"
    ],

    "teaching": [
        "BA / B.Sc + B.Ed",
        "Diploma in Education (D.Ed)",
        "Teacher Eligibility Test (TET)"
    ],

    "law": [
        "LLB",
        "BA LLB",
        "Judicial Services"
    ],

    "government": [
        "TNPSC",
        "SSC",
        "UPSC",
        "Railway Exams",
        "Police / Defence Services"
    ],

    "it": [
        "BCA",
        "B.Sc Computer Science",
        "Software Testing",
        "Web Development"
    ],

    "chef": [
        "Hotel Management",
        "Culinary Arts",
        "Bakery & Catering Business"
    ]
}
# ================= SAVE TRAINING DATA (OPTIMIZED) =================
def save_training_data(scores, course, college):
    """
    Save a single course's training data for KNN prediction.
    Avoid duplicate entries in student_training.
    """
    con = get_db()
    cur = con.cursor()

    # Check if the same combination already exists
    cur.execute("""
        SELECT COUNT(*) FROM student_training
        WHERE teaching=? AND business=? AND chef=? AND law=? AND doctor=? AND nurse=?
        AND engineering=? AND science=? AND maths=? AND commerce=? AND arts=? AND it=? AND government=?
        AND preferred_course=? AND college_type=?
    """, (
        scores.get("teaching",0),
        scores.get("business",0),
        scores.get("chef",0),
        scores.get("law",0),
        scores.get("doctor",0),
        scores.get("nurse",0),
        scores.get("engineering",0),
        scores.get("science",0),
        scores.get("maths",0),
        scores.get("commerce",0),
        scores.get("arts",0),
        scores.get("it",0),
        scores.get("government",0),
        course,
        college
    ))

    if cur.fetchone()[0] == 0:
        # Insert only if not exists
        cur.execute("""
            INSERT INTO student_training (
                teaching,business,chef,law,doctor,nurse,
                engineering,science,maths,commerce,
                arts,it,government,
                preferred_course,college_type
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            scores.get("teaching",0),
            scores.get("business",0),
            scores.get("chef",0),
            scores.get("law",0),
            scores.get("doctor",0),
            scores.get("nurse",0),
            scores.get("engineering",0),
            scores.get("science",0),
            scores.get("maths",0),
            scores.get("commerce",0),
            scores.get("arts",0),
            scores.get("it",0),
            scores.get("government",0),
            course,
            college
        ))

    con.commit()
    con.close()


# ================= RECOMMENDATION =================
@app.route("/recommendation")
def recommendation():
    if "user_id" not in session:
        return redirect("/login")

    scores = session.get("career_scores")
    if not scores:
        return render_template(
            "recommendation.html",
            top_fields=[],
            recommended_courses=[],
            predicted_course=None
        )

    con = get_db()
    cur = con.cursor()

    # Get user qualification
    cur.execute("SELECT qualification FROM users WHERE id=?", (session["user_id"],))
    user = cur.fetchone()
    qualification = user[0].lower() if user else ""
    level = "after_10th" if qualification.startswith("10") else "after_12th"

    # AI Prediction filtered by user's level
    predicted_course, _ = knn_predict(scores)

    # Make sure predicted course is valid for user's level
    cur.execute("SELECT name FROM courses WHERE level=?", (level,))
    valid_courses = [r[0] for r in cur.fetchall()]
    if predicted_course not in valid_courses:
        predicted_course = valid_courses[0] if valid_courses else None

    # Top career fields
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_fields = sorted_scores[:3]
    top_field = top_fields[0][0]
    stream = CAREER_TO_STREAM.get(top_field)

    # Recommended courses (stable, most relevant first)
    recommended_courses = []
    if stream:
        cur.execute("""
            SELECT id, name, duration, eligibility
            FROM courses
            WHERE LOWER(stream)=LOWER(?) AND level=?
            ORDER BY id ASC
        """, (stream, level))  # Keep a stable order, can replace id with relevance score if available
        rows = cur.fetchall()

        seen_courses = set()
        for r in rows:
            course_id, course_name, course_duration, course_eligibility = r
            if course_name not in seen_courses:
                recommended_courses.append({
                    "id": course_id,
                    "name": course_name,
                    "duration": course_duration,
                    "eligibility": course_eligibility
                })
                seen_courses.add(course_name)
            if len(recommended_courses) >= 3:  # Only top 3
                break

            # Log course view
            cur.execute(
                "INSERT INTO course_views (user_id, course_id) VALUES (?,?)",
                (session["user_id"], course_id)
            )
        con.commit()

    con.close()
    session["recommended_courses"] = recommended_courses

    # Save training data
    for course in recommended_courses:
        save_training_data(scores, course["name"], "General College")

    return render_template(
        "recommendation.html",
        top_fields=top_fields,
        recommended_courses=recommended_courses,
        predicted_course=predicted_course
    )
skill_platforms = {

    "Python Programming":{
        "Coursera":"https://www.coursera.org/search?query=python",
        "YouTube":"https://www.youtube.com/results?search_query=python+programming",
        "Udemy":"https://www.udemy.com/courses/search/?q=python"
    },

    "Java Programming":{
        "Coursera":"https://www.coursera.org/search?query=java",
        "YouTube":"https://www.youtube.com/results?search_query=java+programming",
        "Udemy":"https://www.udemy.com/courses/search/?q=java"
    },

    "C++ Programming":{
        "Coursera":"https://www.coursera.org/search?query=c%2B%2B",
        "YouTube":"https://www.youtube.com/results?search_query=c+++programming",
        "Udemy":"https://www.udemy.com/courses/search/?q=c%2B%2B"
    },

    "Data Structures":{
        "Coursera":"https://www.coursera.org/search?query=data+structures",
        "YouTube":"https://www.youtube.com/results?search_query=data+structures",
        "Udemy":"https://www.udemy.com/courses/search/?q=data+structures"
    },

    "Algorithms":{
        "Coursera":"https://www.coursera.org/search?query=algorithms",
        "YouTube":"https://www.youtube.com/results?search_query=algorithms",
        "Udemy":"https://www.udemy.com/courses/search/?q=algorithms"
    },

    "Web Development":{
        "Coursera":"https://www.coursera.org/search?query=web+development",
        "YouTube":"https://www.youtube.com/results?search_query=web+development",
        "Udemy":"https://www.udemy.com/courses/search/?q=web+development"
    },

    "Database Management":{
        "Coursera":"https://www.coursera.org/search?query=database",
        "YouTube":"https://www.youtube.com/results?search_query=database+management",
        "Udemy":"https://www.udemy.com/courses/search/?q=database"
    },

    "Problem Solving":{
        "Coursera":"https://www.coursera.org/search?query=problem+solving",
        "YouTube":"https://www.youtube.com/results?search_query=problem+solving",
        "Udemy":"https://www.udemy.com/courses/search/?q=problem+solving"
    },

    "Leadership":{
        "Coursera":"https://www.coursera.org/search?query=leadership",
        "YouTube":"https://www.youtube.com/results?search_query=leadership+skills",
        "Udemy":"https://www.udemy.com/courses/search/?q=leadership"
    },

    "Marketing Basics":{
        "Coursera":"https://www.coursera.org/search?query=marketing",
        "YouTube":"https://www.youtube.com/results?search_query=marketing+basics",
        "Udemy":"https://www.udemy.com/courses/search/?q=marketing"
    },

    "Accounting":{
        "Coursera":"https://www.coursera.org/search?query=accounting",
        "YouTube":"https://www.youtube.com/results?search_query=accounting+basics",
        "Udemy":"https://www.udemy.com/courses/search/?q=accounting"
    },

    "Creative Writing":{
        "Coursera":"https://www.coursera.org/search?query=creative+writing",
        "YouTube":"https://www.youtube.com/results?search_query=creative+writing",
        "Udemy":"https://www.udemy.com/courses/search/?q=creative+writing"
    }
}
#==========skill==============
@app.route("/skills")
def skills():
    if "user_id" not in session:
        return redirect("/login")

    courses = session.get("recommended_courses")

    if not courses:
        return render_template("skills.html", course_skills={})

    con = get_db()
    cur = con.cursor()

    course_skills = {}

    for course in courses:
        course_name = course["name"]  # get course name from dict

        cur.execute("SELECT id FROM courses WHERE name=?", (course_name,))
        row = cur.fetchone()

        skills = []

        if row:
            course_id = row[0]

            # ===== LOG SKILL PAGE VIEW FOR ADMIN =====
            cur.execute(
                "INSERT INTO skill_views (user_id, course_id) VALUES (?, ?)",
                (session["user_id"], course_id)
            )

            cur.execute("SELECT skill_name FROM skills WHERE course_id=?", (course_id,))
            skills = [s[0] for s in cur.fetchall()]

        # ===== SMART SKILL GENERATOR =====
        if not skills:

            if "Physics" in course_name:
                skills = [
                    "Analytical Thinking",
                    "Mathematical Modelling",
                    "Scientific Research",
                    "Data Analysis",
                    "Laboratory Techniques",
                    "Problem Solving"
                ]

            elif "Chemistry" in course_name:
                skills = [
                    "Laboratory Techniques",
                    "Chemical Analysis",
                    "Research Skills",
                    "Instrumentation Handling",
                    "Data Interpretation"
                ]

            elif "Mathematics" in course_name:
                skills = [
                    "Logical Reasoning",
                    "Statistical Analysis",
                    "Problem Solving",
                    "Mathematical Modelling",
                    "Programming with Python"
                ]

            elif "Engineering" in course_name or "B.Tech" in course_name:
                skills = [
                    "Problem Solving",
                    "Technical Design",
                    "Project Management",
                    "Programming Basics",
                    "Engineering Mathematics"
                ]

            elif "Nursing" in course_name:
                skills = [
                    "Patient Care",
                    "Medical Knowledge",
                    "Emergency Response",
                    "Communication Skills",
                    "Clinical Skills"
                ]

            elif "Management" in course_name or "BBA" in course_name:
                skills = [
                    "Leadership",
                    "Strategic Thinking",
                    "Business Communication",
                    "Team Management",
                    "Decision Making"
                ]

            elif "Law" in course_name or "LLB" in course_name:
                skills = [
                    "Legal Research",
                    "Critical Thinking",
                    "Public Speaking",
                    "Argumentation",
                    "Legal Writing"
                ]

            else:
                skills = [
                    "Communication Skills",
                    "Critical Thinking",
                    "Problem Solving",
                    "Time Management",
                    "Teamwork"
                ]

        course_skills[course_name] = skills

    # ===== COMMIT ALL SKILL VIEWS =====
    con.commit()
    con.close()

    return render_template(
        "skills.html",
        course_skills=course_skills
    )
# ================= HELP =================
@app.route("/help")
def help_page():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("help.html")


# -------------------------------
# CITY DIRECTORY (Tamil Nadu)
# -------------------------------
@app.route("/city_colleges")
def city_colleges():

    if "user_id" not in session:
        return redirect("/login")

    cities = []
    static_path = os.path.join(app.root_path, "static")

    for file in os.listdir(static_path):
        if file.endswith("_colleges_courses.csv"):

            city_name = file.replace("_colleges_courses.csv", "")
            city_name = city_name.replace("_", " ").title()

            cities.append({
                "name": city_name,
                "file": file
            })

    cities = sorted(cities, key=lambda x: x["name"])

    return render_template("city_colleges.html", cities=cities)


# -------------------------------
# DOWNLOAD CSV
# -------------------------------
@app.route("/download_csv/<filename>")
def download_csv(filename):
    return send_from_directory("static", filename, as_attachment=True)

#nearby colleges
@app.route("/nearby_colleges")
def nearby_colleges():

    if "user_id" not in session:
        return redirect("/login")

    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT district FROM users WHERE id=?", (session["user_id"],))
    row = cur.fetchone()
    con.close()

    if not row:
        return "User district not found"

    district_raw = row[0]

    district_clean = district_raw.strip().lower()
    district_clean = district_clean.replace(" district", "")
    district_clean = district_clean.replace(" ", "_")

    # Fix common spelling issues
    if district_clean == "namakal":
        district_clean = "namakkal"

    csv_filename = f"{district_clean}_colleges_courses.csv"
    csv_file_path = os.path.join(app.root_path, "static", csv_filename)

    colleges = []

    if os.path.exists(csv_file_path):

        with open(csv_file_path, newline="", encoding="latin-1") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]

            for row in reader:
                row_lower = {k.strip().lower(): v for k, v in row.items()}

                colleges.append({
                    "college_name": (row_lower.get("college name") or "").strip(),
                    "city": (row_lower.get("city") or "").strip(),
                    "website": (row_lower.get("website") or "").strip()
                })

    return render_template(
        "colleges.html",
        colleges=colleges,
        district=district_raw.title(),
        csv_file=csv_filename if os.path.exists(csv_file_path) else None
    )

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
