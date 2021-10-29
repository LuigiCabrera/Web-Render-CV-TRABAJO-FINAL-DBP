from flask import Flask, render_template, request, session, sessions
from flask_session import Session

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
    if not session.get("personal_info") or len(session["personal_info"]) == 0: 
        vars_ = ["fname", "lname", "email", "country", "city", 
                "adress", "phone", "lk", "web", "resume", "degree"]
        session["personal_info"] = [request.form.get(v) for v in vars_]
    else: #POST JSON DATA (FORM 2)
        dataJSON = request.get_json(force=True)
        session["study"] = [li.split(",") for li in dataJSON['studies']]
        session["work"] = [li.split(",") for li in dataJSON['work']]
        session["languages"] = [li.split(",") for li in dataJSON['language']]
        session["achievements"], session["skills"] = None, None
    return render_template("form2_experience.html")


@app.route("/form3", methods=["POST"])
def form3():
    if session["achievements"] == None or session["skills"] == None:
        session["achievements"] = []
        session["skills"] = []
    else:
        dataJSON = request.get_json(force=True)
        session["skills"] = [li.split(",") for li in dataJSON['skill']]
        session["achievements"] = dataJSON['achievement']
        session["hobbies"], session["references"] = None, None
    return render_template("form3_skills.html")

@app.route("/form4", methods=["POST"])
def form4():
    if session["hobbies"] == None or session["references"] == None:
        session["hobbies"] = []
        session["references"] = []
    else:
        dataJSON = request.get_json(force=True)
        session["hobbies"] = dataJSON['hobbies']
        session["references"] = [li.split(",") for li in dataJSON['references']]
    return render_template("form4_references.html")

@app.route("/curriculum_rendered", methods=["POST"])
def render_curriculum():
    #keys = ['personal_info','study','work','languages','achievements','skills','hobbies','references']
    #for k in keys: print(session[k])
    return render_template("render_curriculum.html",personal_data=session["personal_info"],
                                                    studies=session["study"],
                                                    works=session["work"],
                                                    languages=session["languages"],
                                                    achievements=session["achievements"],
                                                    skills=session["skills"],
                                                    hobbies=session["hobbies"],
                                                    references=session["references"])


