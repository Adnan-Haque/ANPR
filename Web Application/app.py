from django.shortcuts import render
from matplotlib import image
import numpy as np
import lib
from flask import Flask, flash, render_template, request, send_file, url_for, redirect
import psycopg2

app = Flask(__name__, static_folder="styles/")
app.secret_key = "abc"


def get_db_connection():
    conn = psycopg2.connect(host="localhost",
                            database='carsDB',
                            user='postgres',
                            password='adnan')
    return conn


conn = get_db_connection()
cur = conn.cursor()


@app.route("/")
def home():
    cur.execute('select * from cars;')
    cars = cur.fetchall()
    print("Executing")
    print("this is cars", cars)
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        car_id = request.form['car_id']
        name = request.form['name']
        room_no = request.form['room_no']
        contact_no = request.form['contact_no']
        print(car_id, name, room_no, contact_no)
        cur.execute(
            "select car_id from cars where car_id = '{}'".format(car_id))
        exe_id = cur.fetchall()
        if(exe_id):
            flash("record already exists")
            return render_template("addCar.html", exe_id=exe_id)
        else:
            flash("record enter successfully")
            cur.execute(
                "insert into cars values ('{}','{}','{}','{}')".format(car_id, name, room_no, contact_no))
            conn.commit()
            count = cur.rowcount
            print(count, "Record inserted successfully")
            return redirect(url_for("add", count=count))
    else:
        if 'text' in request.args:
            flash(
                "The car Does not Exists in Database First insert the car in database")
            text = request.args['text']
            return render_template("addCar.html", text=text)
        else:
            return render_template("addCar.html")


@app.route('/full', methods=["POST", "GET"])
def full():
    if request.method == "POST":
        limit = int(request.form['limit'])
        cur.execute("select c.car_id, name, room_no, contact_number, curr_date, curr_time, status from cars c , logs l where c.car_id = l.car_id order by l.curr_date desc, l.curr_time desc limit {}".format(limit))
        data = cur.fetchall()
        data = [list(x) for x in data]
        return render_template("fullData.html", data=data)
    else:
        cur.execute(
            "select c.car_id, name, room_no, contact_number, curr_date, curr_time, status from cars c , logs l where c.car_id = l.car_id order by l.curr_date desc, l.curr_time desc limit 10")
        data = cur.fetchall()
        data = [list(x) for x in data]
        print(data)
        return render_template("fullData.html", data=data)


@app.route('/predict', methods=['POST', 'GET'])
def pred():
    if request.method == "POST":
        file_image = request.files['image1']
        filestr = request.files['image1'].read()
        npimg = np.frombuffer(filestr, np.uint8)
        text = lib.Predict_Plate(npimg)
        cur.execute("select * from cars where car_id='{}'".format(text))
        data = cur.fetchall()
        if(len(data) == 0):
            return redirect(url_for("add", text=text))
        else:
            data = list(data[0])
            print(data)
            return render_template("predict.html", data=data)
    else:
        return render_template("predict.html")


@app.route('/addLog', methods=['POST', 'GET'])
def addLog():
    if request.method == "POST":
        car_id = request.form['car_id']
        status = request.form['status']
        print(car_id, status)
        cur.execute("insert into logs(curr_date,curr_time,car_id,status) values(current_date,current_time::time,'{}','{}')".format(
            car_id, status))
        conn.commit()
        count = cur.rowcount
        flash("Car Entry is Done in logs")
        return redirect(url_for("pred"))


if __name__ == '__main__':
    app.run(debug=True)
