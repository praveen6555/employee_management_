from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret"

# Database connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pallavi@143",
        database="company"
    )

# -------- ADMIN REGISTER --------
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form["username"]
        pwd = request.form["password"]

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users (username,password,role) VALUES (%s,%s,%s)",
            (uname, pwd, "admin")
        )
        con.commit()
        con.close()
        return redirect("/login")

    return render_template("register.html")

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        pwd = request.form["password"]

        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                    (uname, pwd))
        user = cur.fetchone()
        con.close()

        if user:
            session["admin"] = uname
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")

# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/")
    return render_template("dashboard.html")

# -------- ADD EMPLOYEE --------
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = (
            request.form["eid"],
            request.form["ename"],
            request.form["edept"],
            request.form["esalary"],
            request.form["ephone"]
        )

        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO employee VALUES (%s,%s,%s,%s,%s)", data)
        con.commit()
        con.close()
        return redirect("/view")

    return render_template("add_employee.html")

# -------- VIEW EMPLOYEES --------
@app.route("/view")
def view():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM employee")
    data = cur.fetchall()
    con.close()
    return render_template("view_employee.html", employees=data)

# -------- EDIT EMPLOYEE --------
@app.route("/edit/<eid>")
def edit(eid):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM employee WHERE eid=%s", (eid,))
    emp = cur.fetchone()
    con.close()
    return render_template("edit_employee.html", emp=emp)

# -------- UPDATE EMPLOYEE --------
@app.route("/update", methods=["POST"])
def update():
    data = (
        request.form["ename"],
        request.form["edept"],
        request.form["esalary"],
        request.form["ephone"],
        request.form["eid"]
    )

    con = get_db()
    cur = con.cursor()
    cur.execute(
        "UPDATE employee SET ename=%s, edept=%s, esalary=%s, ephone=%s WHERE eid=%s",
        data
    )
    con.commit()
    con.close()
    return redirect("/view")

# -------- DELETE EMPLOYEE --------
@app.route("/delete/<eid>")
def delete(eid):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM employee WHERE eid=%s", (eid,))
    con.commit()
    con.close()
    return redirect("/view")

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route('/home')
def Home():
 return render_template('home.html')
@app.route('/contact')
def Contact():
    return render_template('contact.html')
@app.route('/about')
def About():
   return render_template('about.html')



if __name__ == "__main__":
    app.run(debug=True)
