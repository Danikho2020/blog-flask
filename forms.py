from wtforms import Form, StringField, TextField, validators, PasswordField
from wtforms.fields.html5 import EmailField
from email_validator import validate_email
from models import User


class RegistroForm(Form):
	
	username = StringField('Nombre de ususario',
               [ 
					validators.Required(message = 'x'),
					validators.length(min=4, max=25, message='Ingrese un username entre 4 y 25 caracteres!.'),
				])

	password = PasswordField('Password', [validators.Required(message='El password es requerido')])
	
	email = EmailField('Correo electronico',
                    [ 
					validators.Required(message = 'x'),
				])
	
	def validate_username(form, field):
		username = field.data
		user = User.query.filter_by(username = username).first()
		if user != None:
			raise validators.ValidationError('El nombre de ususario ya se encuentra registrado.')

class LoginForm(Form):
	
	username = StringField('Nombre de ususario', [ validators.Required(message = 'x')])

	password = PasswordField('Password', [validators.Required(message = 'x')])


class CommentForm(Form):

	comment = TextField('Comentario:', [ validators.Required(message = 'No puedes enviar un comentario vacío!')])