from flask import Flask
from flask import render_template
from flask import request
from random import randrange

from db import session, Question

app = Flask(__name__)

def gen_question():
    questions = session.query(Question).all()
    questions_n = len(questions)
    if questions_n == 0:
        return 
    rand_n = randrange(0, questions_n)
    return questions[rand_n]




@app.route('/', methods=['GET', 'POST'])
def index():
    prev_question = ""
    verdict = ""
    if request.method == 'POST':
        question = session.query(Question).filter_by(id=request.form["question_id"]).first()
        prev_question = "Previous question: " + question.text
        verdict_temp = "Your answer '{}' is {}"
        if request.form["answer"] == question.answer:
            verdict = verdict_temp.format(request.form["answer"], 'correct!')
        else: 
            verdict = verdict_temp.format(request.form["answer"], 'incorrect :(.')\
                + "Correct answer is {}".format(question.answer)
    question = gen_question()
    return render_template('index.html', question=question.text,
                            question_id=question.id,
                            prev_question=prev_question,
                            verdict=verdict)

@app.route('/add', methods=['GET', 'POST'])
def add_question():
    result = ""
    if request.method == 'POST':
        question = Question(text=request.form["text"],
                            answer=request.form["answer"],
                            type='SINGLE')
        session.add(question)
        session.commit()
        result = "Question added successfully!"
    return render_template('add.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
