from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'secret-key'
marshmallow = Marshmallow(app)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

local = False
if local:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@127.0.0.1/soccer_db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b36064d9893fb5:39dec7a9@us-cdbr-east-06.cleardb.net/heroku_6c4f9dd4746ddb4'


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Accounts(db.Model):
    username = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now())


class SoccerScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.String(255), nullable=False)
    away = db.Column(db.String(255), nullable=False)
    score_home_team = db.Column(db.String(255), nullable=False)
    score_away_team = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now())


# serializer for score Api


class ScoreSchema(marshmallow.Schema):
    class Meta:
        fields = ("id", "home", "away", "score_home_team",
                  "score_away_team", "date", "created_at")
        model = SoccerScore


soccer_schema = ScoreSchema(many=True)


# soccer api endpoint


class SoccerListResource(Resource):
    def get(self):
        scores = SoccerScore.query.all()
        return soccer_schema.dump(scores)


api.add_resource(SoccerListResource, '/scores_api')


@app.route('/')
def index():
    scores = db.session.query(SoccerScore).all()

    return render_template('index.html', scores=scores)


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    try:
        if 'user' in session:
            return redirect('/admin_dashboard')
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = Accounts.query.filter_by(
                username=username, password=password).first()
            if user:
                session['user'] = user.username
                return redirect('/admin_dashboard')
            else:
                flash(message='Username or password is incorrect!', category='error')
                return redirect(request.url)
        return render_template('admin_login.html')
    except Exception as error:
        print('#'*40)
        print(error)
        print('#'*40)
        return redirect('/')


@app.route('/admin_dashboard')
def admin_dashboard():
    try:
        if 'user' in session:
            scores = db.session.query(SoccerScore).all()
            return render_template('admin_dashboard.html', scores=scores)
        return redirect('/admin')
    except Exception as error:
        print('#'*40)
        print(error)
        print('#'*40)
        return redirect('admin')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect('/admin')


@app.route('/add_score', methods=['GET', 'POST'])
def add_score():
    try:
        if 'user' not in session:
            return redirect('/admin')
        page = 'add'
        if request.method == 'POST':
            home = request.form.get('home')
            away = request.form.get('away')
            score_away_team = request.form.get('score_away_team')
            score_home_team = request.form.get('score_home_team')
            date = request.form.get('date')

            score = SoccerScore(
                home=home, away=away, score_home_team=score_home_team, score_away_team=score_away_team, date=date
            )
            db.session.add(score)
            db.session.commit()
            flash(message='Successfully added score', category='success')
        elif request.method == 'GET':
            return render_template('add_edit_score.html', page=page)
    except Exception as error:
        print('#'*40)
        print(error)
        print('#'*40)
    return redirect('/admin_dashboard')


@app.route('/edit_score/<int:score_id>', methods=['GET', 'POST'])
def edit_score(score_id):
    try:
        page = 'edit'
        if 'user' not in session:
            return redirect('/admin')
        if request.method == 'GET':
            score = db.session.query(SoccerScore).filter(
                SoccerScore.id == score_id).first()
            return render_template('add_edit_score.html', page=page, score=score)
        elif request.method == 'POST':
            home = request.form.get('home')
            away = request.form.get('away')
            score_away_team = request.form.get('score_away_team')
            score_home_team = request.form.get('score_home_team')
            date = request.form.get('date')
            score = db.session.query(
                SoccerScore).filter_by(id=score_id).first()
            score.home = home
            score.away = away
            score.score_away_team = score_away_team
            score.score_home_team = score_home_team
            score.date = date
            db.session.commit()
    except Exception as error:
        print('#'*40)
        print(error)
        print('#'*40)
    return redirect('/admin_dashboard')


@app.route('/delete_score/<int:score_id>')
def delete_score(score_id):
    if 'user' not in session:
        return redirect('/admin')
    score = db.session.query(SoccerScore).filter(
        SoccerScore.id == score_id).first()
    db.session.delete(score)
    db.session.commit()
    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
