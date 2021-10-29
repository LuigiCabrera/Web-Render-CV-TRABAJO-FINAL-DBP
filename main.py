from flask import Flask, render_template, request, session, sessions
from flask_session import Session
from modules import *

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/main", methods=["POST"])
def main():
    return render_template("main.html", email=request.form.get('email'))

@app.route("/form1", methods=["POST"])
def form1():
    session["personal_info"] = []
    return render_template("form1_personal_data.html")

@app.route("/form2", methods=["POST"])
def form2():
    #Viene de form1
    if not session.get("personal_info") or len(session["personal_info"]) == 0: 
        vars_ = ["fname", "lname", "email", "country", "city", 
                "adress", "phone", "lk", "web", "resume", "degree"]
        session["personal_info"] = [request.form.get(v) for v in vars_]

        session["study"] = []
        session["work"] = []
        session["languages"] = []

        session["achievements"] = None
        session["skills"] = None
        
        return render_template("form2_experience.html")

    # Viene de form 2
        
    vars = ["y_begin_s", "y_end_s", "title", "study"]
    fill = [request.form.get(v) for v in vars]
    if verify_list(fill): session["study"].append(fill)        

    vars = ["y_begin_w", "y_end_w", "job", "work"]
    fill = [request.form.get(v) for v in vars]
    if verify_list(fill): session["work"].append(fill) 

    vars = ["language", "level"]
    fill = [request.form.get(v) for v in vars]
    if verify_list(fill): session["languages"].append(fill) 
    
    return render_template("form2_experience.html", studies=session["study"], work=session["work"], languages=session["languages"])

@app.route("/form3", methods=["POST"])
def form3():

    # Viene de form 2
    if session["achievements"] == None or session["skills"] == None:
        session["achievements"] = []
        session["skills"] = []

        session["hobbies"] = None
        session["references"] = None

        dataGet = request.get_json(force=True)
        print(dataGet)

        return render_template("form3_skills.html")

    fill = request.form.get("achievement")
    if verify_var(fill): session["achievements"].append(fill)        

    vars = ["skill", "level"]
    fill = [request.form.get(v) for v in vars]
    if verify_list(fill): session["skills"].append(fill) 
    
    return render_template("form3_skills.html", achievements=session["achievements"], skills=session["skills"])

@app.route("/form4", methods=["POST"])
def form4():

    # Viene de form 2
    if session["hobbies"] == None or session["references"] == None:
        session["hobbies"] = []
        session["references"] = []

        return render_template("form4_references.html")

    fill = request.form.get("hobbie")
    if verify_var(fill): session["hobbies"].append(fill)        

    vars = ["name", "job", "email", "phone"]
    fill = [request.form.get(v) for v in vars]
    if verify_list(fill): session["references"].append(fill) 
    
    return render_template("form4_references.html", hobbies=session["hobbies"], references=session["references"])

@app.route("/curriculum_rendered", methods=["POST"])
def render_curriculum():
    return render_template("render_curriculum.html", personal_data=session["personal_info"],
                                                    studies=session["study"],
                                                    works=session["work"],
                                                    languages=session["languages"],
                                                    achievements=session["achievements"],
                                                    skills=session["skills"],
                                                    hobbies=session["hobbies"],
                                                    references=session["references"])


