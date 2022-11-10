from flask import render_template, request
from app import app
import csv
from config import url


@app.route('/', methods=["GET", "POST"])
def index():
    p = ""
    if request.method == 'POST':
        f = request.files['file']
        t = request.form["search"].lower()
        column = request.form["column"]
        data = []
        name = f.filename
        if t and f:
            f.save(url + name)
            with open(url+name, "r", encoding="utf-8") as file:
                s = csv.DictReader(file)
                for i in s:
                    g = i[column]
                    if t in g.lower():
                        data.append(g)
                        if len(data) == 20:
                            break
            return render_template("success.html", data=data)
        elif f:
            f.save(url + name)
            with open(url+name, "r", encoding="utf-8") as file:
                p = csv.DictReader(file)
                p = "|".join(p.fieldnames)
                return render_template("index.html", p=p)
    return render_template("index.html", p=p)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    p = ""
    if request.method == 'POST':
        f = request.files['file']
        t = request.form["search"].lower()
        column = request.form["column"]
        deldata = []
        name = f.filename
        if t and f:
            f.save(url + name)
            with open(url+name, "r", encoding="utf-8") as rfile:
                s = csv.DictReader(rfile)
                with open(url+"new_"+name, "w", encoding="utf-8") as wfile:
                    writer = csv.DictWriter(wfile, dialect=csv.unix_dialect, fieldnames=s.fieldnames)
                    writer.writeheader()
                    for i in s:
                        g = i[column]
                        if t in g.lower():
                            deldata.append(i)
                        else:
                            writer.writerow(i)
            return render_template("OK del.html", deldata=deldata)
        elif f:
            f.save(url + name)
            with open(url+name, "r", encoding="utf-8") as file:
                p = csv.DictReader(file)
                p = "|".join(p.fieldnames)
                return render_template("write.html", p=p)
    return render_template("write.html", p=p)





