#pip install flask-sqlalchemy

from flask import Flask, redirect, render_template, request, session, url_for
import os
from models import db, Quiz, Question, db_add_new_data, User
from random import shuffle
import sys

BASE_DIR = os.getcwd()

DB_PATH = os.path.join(BASE_DIR, 'db', 'db_quiz.db')

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECRET_KEY'] = 'secretkeysecretkeysecretkey1212121'

db.init_app(app)

html_config = {
    'admin':True
}

# with app.app_context():
#     db_add_new_data()

#     quiz = Quiz.query.all()
    # for q in quizes:
    #     print(f"{q}")
    #     for qu in q.question:
    #         print('-'*5, qu)

    # question = Question.query.all()
    # user = User.query.get(1)
    # print(quiz[1].question)
    # print('--')
    # print(question[1].quiz)
    # print(quiz[1].user)
    # print(user.quizes)
    # sys.exit()    

@app.route('/', methods = ['GET'])
def index():
    return render_template('base.html', html_config = html_config)

@app.route('/quiz/', methods = ['POST', 'GET'])
def view_quiz():
    if request.method == 'GET':
        session['quiz_id'] = -1
        quizes = Quiz.query.all()
        return render_template('start.html', quizes=quizes, html_config = html_config)
    session['quiz_id'] = request.form.get('quiz')
    session['question_n'] = 0
    session['question_id'] = 0
    session['right_answers'] = 0
    return redirect(url_for('view_question'))


@app.route('/question/', methods = ['POST', 'GET'])
def view_question():
    
    if not session['quiz_id'] or session['quiz_id'] == -1:
        return redirect(url_for('view_quiz'))

    # если пост значит ответ на вопрос        
    if request.method == 'POST':        
        question = Question.query.filter_by(id=session['question_id']).all()[0]        
        # если ответ ы сходятся значит +1
        if question.answer == request.form.get('ans_text'):
            session['right_answers'] += 1
        # следующий вопрос
        session['question_n'] += 1


    quiz = Quiz.query.filter_by(id = session['quiz_id']).all()
    if int(session['question_n']) >= len(quiz[0].question):
        session['quiz_id'] = -1 # чтообы больше не работола страница question
        return redirect(url_for('view_result'))
    
    else:
        question = quiz[0].question[session['question_n']]
        session['question_id'] = question.id
        answers = [question.answer, question.wrong1, question.wrong2, question.wrong3 ]
        shuffle(answers)

        return render_template('question.html', 
                               answers=answers, 
                               question=question, 
                               html_config = html_config)



@app.route('/questions/')
def veiw_questions():
    questions = Question.query.all()
    print(questions)
    return render_template('questions.html', questions = questions, html_config = html_config)


@app.route('/result/')
def view_result():
    return render_template('result.html', 
                    right=session['right_answers'], 
                    total = session['question_n'],
                    html_config = html_config)

@app.route('/quizes_view/', methods = ['POST', 'GET'])
def view_quiz_edit():
    if request.method == 'POST':
        quiz = request.form.get('quiz')
        if quiz and len(quiz) > 3:
            user = User.query.all()
            print(11111111111111, user)
            quiz = Quiz(quiz, user[0])
            db.session.add(quiz)
            db.session.commit()
        else:
            question = request.form.get('question')
            answer = request.form.get('answer')
            wrong1 = request.form.get('wrong1')
            wrong2 = request.form.get('wrong2')
            wrong3 = request.form.get('wrong3')
            if all([question, answer, wrong1, wrong2, wrong3]):
                q = Question(question, answer, wrong1, wrong2, wrong3)
                db.session.add(q)
                db.session.commit()
        

        
        return redirect(url_for('view_quiz_edit', qqq='123'))
    
    quizes = Quiz.query.all()
    # quizes[0].name = 'qwqwqwq'
    # db.session.commit()
    questions = Question.query.all()
    return render_template('quizes_view.html', 
                           html_config = html_config,
                           quizes = quizes,
                           questions = questions,
                           len = len)

@app.route('/quiz_edit/<int:id>/', methods = ['GET','POST'])
def quiz_edit(id):
    if request.method == 'POST':
        quiz = Quiz.query.filter_by(id = id).one()
        if quiz and request.form.get('name') and len(request.form.get('name')) > 3:
            quiz.name = request.form.get('name')
            db.session.commit()
        return redirect('/quizes_view/')

    quiz = Quiz.query.filter_by(id=id).one()    
    return render_template('quiz_edit.html', quiz = quiz, html_config = html_config)


@app.route('/quiz_delete/<int:id>/', methods = ['GET','POST'])
def quiz_deelete(id):
    Quiz.query.filter_by(id = id).delete()
    db.session.commit()
    return redirect('/quizes_view/')

@app.route('/question_delete/<int:id>/', methods = ['GET','POST'])
def question_deelete(id):
    Question.query.filter_by(id = id).delete()
    db.session.commit()
    return redirect('/quizes_view/')


@app.route('/question_edit/<int:id>/', methods = ['GET','POST'])
def question_edit(id):
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        wrong1 = request.form.get('wrong1')
        wrong2 = request.form.get('wrong2')
        wrong3 = request.form.get('wrong3')
        q:Question = Question.query.filter_by(id = id).one()
        if all([question, answer, wrong1, wrong2, wrong3, q]):
            q.question = question
            q.answer = answer
            q.wrong1 = wrong1
            q.wrong2 = wrong2
            q.wrong3 = wrong3
            db.session.commit()
        return redirect('/quizes_view/')
    
    q = Question.query.filter_by(id=id).one()    
    return render_template('question_edit.html', q = q, html_config = html_config)


@app.errorhandler(404)
def page_not_found(e):
    #snip
    return '<h1 style="color:red; text-align:center"> Упс..... </h1>'

app.run(debug=True)