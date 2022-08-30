from flask import Flask, request, render_template, redirect, flash
from surveys import surveys

# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "randomkey"

# debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def show_survey_start():
    """Display survey home page - survey title, instructions"""
    title = surveys['satisfaction'].title
    instructions = surveys['satisfaction'].instructions
    return render_template("survey_start.html", title=title, instructions=instructions)

@app.route("/questions/<int:num>")
def display_question(num):
    """Display question text and response choices,
    automatically show the correct question if a user tries to manually change url,
    show thank you if user has answered all questions
    """
    if num == len(responses):
        title = surveys['satisfaction'].title
        question = surveys['satisfaction'].questions[num].question
        choices = surveys['satisfaction'].questions[num].choices
        return render_template("question.html", question=question, choices=choices, title=title, num=num)
    elif num != len(responses) and len(responses) < len(surveys['satisfaction'].questions):
        correct_num = len(responses)
        flash("Please complete the questions in order and only answer each question once.")
        return redirect(f"/questions/{correct_num}")
    else:
        return redirect("/thank_you")

@app.route("/answer", methods=["POST"])
def save_answer():
    """Save answer to response list, redirect user to next question"""
    response = request.form.to_dict()
    keys = list(response.keys())
    values = list(response.values())
    next_num = int(keys[0]) + 1
    responses.append(values[0])
    if next_num < len(surveys['satisfaction'].questions):
        return redirect(f"/questions/{next_num}")
    else:
        return redirect("/thank_you")

@app.route("/thank_you")
def thank_you():
    """Display thank you page if user has answered all questions"""
    if len(responses) == len(surveys['satisfaction'].questions):
        return render_template("thank_you.html")
    else:
        correct_num = len(responses)
        flash("Please complete the questions in order and only answer each question once.")
        return redirect(f"/questions/{correct_num}")