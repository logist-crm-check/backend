from flask import Flask, render_template, request
from webapp.model import db
from datetime import datetime, UTC
from webapp.model import db, Ticket, User
from webapp.forms import LoginForm
from flask_login import LoginManager
from flask_login import LoginManager, login_user
from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required,login_user, logout_user


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    

    @app.route('/')
    @login_required
    def index():
        title = "logist crm"
        tickets = Ticket.query.all()


        return render_template('index.html', page_title=title, tickets=tickets)
    
    
    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
        

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
           return 'Привет админ'
        else:
           return 'Ты не админ!'
        
    @app.post("/api/v1/tickets/")
    def add_ticket():
        data = request.get_json()
        ticket = Ticket(ticket_type=data["ticket_type"], plate=data["plate"], text=data["text"], created_at=datetime.now(tz=UTC))
        db.session.add(ticket)
        db.session.commit()
        return {}, 204


    return app