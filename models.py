# pip install flask-sqlalhemy

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # __tablename__ = user
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25))
    quizes = db.relationship('Quiz', backref='user', 
                             cascade = "all, delete, delete-orphan")

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name



quiz_question = db.Table('quiz_question',
            db.Column('quiz_ud', db.Integer, db.ForeignKey('quiz.id'), primary_key=True),
            db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
            )

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # question = db.relationship(
    #             'Question', 
    #             secondary=quiz_question, backref = 'quiz')

    def __init__(self, name: str, user:User) -> None:
        super().__init__()
        self.name = name
        self.user = user

    def __repr__(self) -> str:
        return f'id - {self.id}, name - {self.name}'





class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    wrong1 = db.Column(db.String(100), nullable=False)
    wrong2 = db.Column(db.String(100), nullable=False)
    wrong3 = db.Column(db.String(100), nullable=False)
    quiz = db.relationship(
                'Quiz', 
                secondary=quiz_question, backref = 'question')

    def __init__(self, quesion: str, answer, wrong1, wrong2, wrong3) -> None:
        super().__init__()
        self.question = quesion
        self.answer = answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

    def __repr__(self):
        return f'{self.id}-{self.question}'


def db_add_new_data():
    db.drop_all()
    db.create_all()

    user1 = User('user1')
    user2 = User('user2')


    quizes = [
        Quiz('QUIZ 1', user1),
        Quiz('QUIZ 2', user1),
        Quiz('QUIZ 3', user2),
        Quiz('QUIZ 4', user2)
    ]


    questions = [
        Question('Сколько будут 2+2*2', '6', '8', '2', '0'),
        Question('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        Question('Каким станет зелёный утёс, если упадет в Красное море?', 'Мокрым?', 'Красным', 'Не изменится', 'Фиолетовым'),
        Question('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        Question('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        Question('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        Question('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако'),
        Question('Что такое у меня в кармашке?', 'Кольцо', 'Кулак', 'Дырка', 'Бублик')
    ]

    quizes[0].question.append(questions[0])
    quizes[0].question.append(questions[1])
    quizes[0].question.append(questions[2])
    
    
    quizes[1].question.append(questions[3])
    quizes[1].question.append(questions[4])
    quizes[1].question.append(questions[5])
    quizes[1].question.append(questions[6])
    quizes[1].question.append(questions[0])
    
    quizes[2].question.append(questions[7])
    quizes[2].question.append(questions[6])
    quizes[2].question.append(questions[5])
    quizes[2].question.append(questions[4])
    
    quizes[3].question.append(questions[6])
    quizes[3].question.append(questions[0])
    quizes[3].question.append(questions[1])
    quizes[3].question.append(questions[3])





    db.session.add_all(quizes)
    db.session.commit()
