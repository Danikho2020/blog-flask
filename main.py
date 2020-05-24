from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import CsrfProtect
import forms
import math
from models import db, User, Comment
from flask import jsonify
from config import config
from decouple import config as config_decouple


def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    csrf = CsrfProtect()

    with app.app_context():
        csrf.init_app(app)
        db.init_app(app)
        db.create_all()

    return app

enviroment = config['development']
if config_decouple('PRODUCTION', default=False):
    enviroment = config['production']

app = create_app(enviroment)




@app.before_request
def before_request():
	if 'id' not in session and request.endpoint in ['home']:
		return redirect(url_for('login'))

	elif 'id' in session and request.endpoint in ['login', 'signup']:
		return redirect(url_for('home'))	

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/signup/', methods = ['GET', 'POST'])
def signup():
    form = forms.RegistroForm(request.form)
    if request.method == 'POST' and form.validate():

        print(form.data) #trae todos los datos en un diccionario
        print(form.username.data) #trae solo un dato

        #instanciamos el modelo deseado con los datos que traemos del formulario
        new_user = User(
            form.username.data,
            form.email.data,
            form.password.data
        )

        #guardamos la instancia en la base de datos
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))




    return render_template('signup.html', form = form)

@app.route('/logout/')
def deslogueo():
    #session['id_usuario'] = None
    session.clear()    #esto borra todas las variables que pudieramos haber guardado en session
    return redirect(url_for('login'))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = forms.LoginForm(request.form)
    mensaje = 'Ingrese sus datos:'
    if request.method == 'POST' and form.validate():
        print(form.username.data)
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            session['id'] = user.id
            return redirect(url_for('home'))
        else:
            mensaje = 'Usuario o contraseña incorrectos.'
            return render_template('login.html', form = form, mensaje = mensaje)
    return render_template('login.html', form = form, mensaje = mensaje)
    
@app.route('/home/', methods = ['GET', 'POST'])
#agregamos una ruta q pasa el numero de paginacion en el q estamos
@app.route('/home/<int:page>', methods = ['GET', 'POST'])
#en la funcion recibimos el numero de paginacion, pero le ponemos por defecto 1, para q si no dan num de paginacio, lleve a la pag 1
def home(page=1):
    user = User.query.filter_by(id = session['id']).first()
    form = forms.CommentForm(request.form)
    per_page = 3
    if len(list(Comment.query.filter_by())) <= per_page:
        total_pages = 1
    else:
        total_comments = len(list(Comment.query.filter_by()))
        total_pages = math.ceil(total_comments / per_page)

    
    comments = Comment.query.join(User).add_columns(User.username, Comment.text, Comment.created_date).order_by(Comment.created_date.desc()).paginate(page, per_page, False)

    if request.method == 'POST' and form.validate():
        comment = Comment(
            user_id = user.id,
            text = form.comment.data
        )
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('home.html', user = user, form = form, comments= comments, page = page, total_pages = total_pages)

if __name__ == '__main__':
    app.run(debug=True)
