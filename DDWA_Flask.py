from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import abort, request, escape, make_response,jsonify
import numpy as np
import sqlite3
import json

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("carsDB1.db")
        print("Connection Eshtablished Successfully")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/cars", methods=["GET", "POST"])
def cars():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("select * from Cars_selected")
        cars = [
            dict(wheelbase=row[0],carlength=row[1],carwidth=row[2],carheight=row[3],curbweight=row[4],enginsize=row[5],boreratio=row[6],stroke=row[7],compressionratio=row[8],horsepower=row[9],peakrpm=row[10],price=row[11])
        for row in cursor.fetchall()]
        if cars is not None:
            return jsonify(cars)

    if request.method == "POST":
        conn.execute("INSERT INTO Cars_selected VALUES (:wheelbase, :carlength, :carwidth, :carheight, :curbweight, :enginesize, :boreratio, :stroke, :compressionratio, :horsepower, :peakrpm, :price)",
            ({"wheelbase": float(request.json['wheelbase']),
              "carlength": float(request.json['carlength']),
              "carwidth": float(request.json['carwidth']),
              "carheight": float(request.json['carheight']),
              "curbweight": int(request.json['curbweight']),
              "enginesize": int(request.json['enginesize']),
              "boreratio": float(request.json['boreratio']),
              "stroke": float(request.json['stroke']),
              "compressionratio": float(request.json['compressionratio']),
              "horsepower": int(request.json['horsepower']),
              "peakrpm": int(request.json['peakrpm']),
              "price": int(request.json['price'])
              })
            )
        conn.commit()
        return "New record generated!"
    else:
        abort(405)


@app.route('/')
def check():
  return "<h1>Flask Is Working!</h1>"


if __name__=='__main__':
    app.run()