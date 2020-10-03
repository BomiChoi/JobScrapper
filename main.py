from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file
from datetime import date

app = Flask("SuperScrapper")

db = {} #임시 데이터베이스


@app.route("/")
def home():
    return render_template("index.html", words=sorted(list(db.keys())))


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower() #소문자로 변환
        existingJobs = db.get(word) 
        if existingJobs: #데이터베이스에 이미 있을 때
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        today = date.today()
        date_str = today.strftime("%y%m%d")
        return send_file("jobs.csv", as_attachment=True, attachment_filename=f"{word} jobs {date_str}.csv")
    except Exception as ex:
        print(ex)
        return redirect("/")


@app.route("/delete")
def delete():
    word = request.args.get('word')
    if word:
        word = word.lower() #소문자로 변환
        existingJobs = db.get(word) 
        if existingJobs: #데이터베이스에 이미 있을 때
            del db[word]
    else:
        return redirect("/")
    return render_template("index.html", words=list(db.keys()))


app.run(host="0.0.0.0", debug=True)
