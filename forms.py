from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class SuggessionForm(FlaskForm):
    username = StringField('Имя: ', validators=[DataRequired(), Length(min=2, max=20, message='Имя должно состоять минимум из 2 символов')])
    e_mail = StringField('Email: ', validators=[Email(message='Некорректный email')])
    suggestion = TextAreaField('Пожелания: ', validators=[Length(max=200)])
    submit = SubmitField('Отправить')


class Register(FlaskForm):
    username = StringField('Имя: ', validators=[DataRequired(), Length(min=2, max=20, message='Имя должно состоять от 2 до 20 символов')])
    e_mail = StringField('Email: ', validators=[Email(message='Некорректный email')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=5, max=20)])
    psw2 = PasswordField('Повторите пароль: ', validators=[EqualTo('psw', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')

class LogIn(FlaskForm):
    e_mail = StringField('Email: ', validators=[Email(message='Некорректный email')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=5, max=20)])
    remember = BooleanField(label='запомнить', default=False)
    submit = SubmitField('Войти')
