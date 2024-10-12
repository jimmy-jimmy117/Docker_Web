from flask import Flask, request, render_template, jsonify
from mysql_model import Person
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import logging
import traceback

import os

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler(os.getenv("LOG_FILE"))
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s"
)
log_handler.setFormatter(formatter)
log_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_handler)
log = app.logger
engine = create_engine(os.getenv("DATABASE_URI"))
app.config["PORT"] = os.getenv("DEFAULT_PORT")


@app.route("/")
def inex():
    return "Response Data"


@app.route("/another")
def inex2():
    return "Another Response"


@app.route("/test_request")
def test_request():
    return f'test_request:{request.args.get("dummy")}'


@app.route("/exercise_request/<dummy>")
def test_request2(dummy):
    return f"exercise_request;{dummy}"


@app.route("/show_html")
def show_html():
    return render_template("test_html.html")


@app.route("/exercise_html")
def exercise_html():
    return render_template("exercise.html")


@app.route("/exercise")
def exercise_html2():
    # return f'exercise:{request.args.get("my_name")}'
    return render_template("answer.html", name=request.args.get("my_name"))


@app.route("/try_rest", methods=["POST"])
def try_rest():
    # リクエストデータをJSONとして受け取る
    request_json = request.get_json()
    print(request_json)
    print(type(request_json))
    name = request_json["name"]
    print(name)
    response_json = {"response_json": request_json}
    return jsonify(response_json)


@app.route("/person_search")
def person_search():
    return render_template("./person_search.html")


@app.route("/person_result")
def person_result():
    try:
        search_size = request.args.get("search_size")
        search_size = int(search_size)
        with Session(engine) as session:
            persons = session.query(Person).filter(Person.size > search_size)
    except Exception:
        log.error(traceback.format_exec())
    return render_template(
        "./person_result.html", persons=persons, search_size=search_size
    )


@app.route("/try_html")
def try_html():
    return render_template("try_html.html")


@app.route("/show_data", methods=["GET", "POST"])
def show_data():
    name = request.form.get("text")
    print(name)
    return render_template("try_html.html")
