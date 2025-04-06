import datetime
from flask import Flask, render_template, redirect, abort, request, jsonify, make_response
from flask_restful import Api

from data import db_session, jobs_api, users_api, users_resources
from data.jobs import Jobs
from data.users import User
from forms.worker import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.works import JobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

app = Flask(__name__)
api = Api(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/mars.db")
    '''app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)'''

    @app.route("/")
    def index():
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(Jobs.is_finished != True)
        return render_template("index.html", news=news)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                address=form.address.data,
                speciality=form.speciality.data,
                position=form.position.data,
                age=form.age.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/jobs', methods=['GET', 'POST'])
    @login_required
    def add_jobs():
        form = JobForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            jobs = Jobs()
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = False
            jobs.team_leader = current_user.id
            db_sess.merge(jobs)
            db_sess.commit()
            return redirect('/')
        return render_template('jobs.html', title='Добавление новости',
                               form=form)

    @app.route('/jobs/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_jobs(id):
        form = JobForm()
        if request.method == "GET":
            db_sess = db_session.create_session()
            jobs = db_sess.query(Jobs).filter((Jobs.id == id,
                                               Jobs.team_leader == current_user.id) | (current_user.id == 1)
                                              ).first()
            if jobs:
                form.job.data = jobs.job
                form.work_size.data = jobs.work_size
                form.collaborators.data = jobs.collaborators
            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            jobs = db_sess.query(Jobs).filter((Jobs.id == id,
                                               Jobs.team_leader == current_user.id) | (current_user.id == 1)
                                              ).first()
            if jobs:
                jobs.job = form.job.data
                jobs.work_size = form.work_size.data
                jobs.collaborators = form.collaborators.data
                jobs.is_finished = False
                jobs.team_leader = current_user.id
                db_sess.commit()
                return redirect('/')
            else:
                abort(501)
        return render_template('jobs.html',
                               title='Редактирование миссии',
                               form=form
                               )

    @app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def jobs_delete(id):
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter((Jobs.id == id,
                                           Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
        if jobs:
            db_sess.delete(jobs)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.errorhandler(400)
    def bad_request(_):
        return make_response(jsonify({'error': 'Bad Request'}), 400)

    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')

    app.run()


if __name__ == '__main__':
    main()
