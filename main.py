from flask import Flask, render_template, redirect, jsonify, make_response
from data import db_session, jobs_api, users_resource
from data.users import User
from flask_login import LoginManager, current_user, logout_user, login_user, login_required
from data.jobs import Jobs
from forms.loginform import LoginForm
from forms.newjob import NewJob
from forms.registerform import RegisterForm
import datetime
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect("/main_page")
    return render_template('base.html')


@app.route('/main_page')
def main_page():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('jobs.html', jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == form.id.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/main_page")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.hashed_password = form.password.data
        user.name = form.name.data
        user.surname = form.surname.data
        user.sage = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        db_sess.merge(user)
        db_sess.commit()
        return redirect('/')
    return render_template('new_user.html', title='Добавление работы',
                           form=form)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewJob()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        if job.is_finished:
            job.end_date = datetime.datetime.now
        current_user.jobs.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('new_job.html', title='Добавление работы',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/mars_explorer.db")
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
