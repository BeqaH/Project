from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, length, equal_to
from flask_wtf.file import FileField, FileRequired

class AddBlogForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description",validators=[DataRequired()])
    image = FileField("Image", validators=[FileRequired()])


    submit = SubmitField("Add Your Post")

class EditBlogForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description",validators=[DataRequired()])
    image = FileField("Image")


    submit = SubmitField("Edit Your Post")


class RegisterForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[
        DataRequired(),
        length(min=8, max=20)
    ])
    repeat_password = PasswordField("Repeat Password", validators=[
        DataRequired(),
        equal_to("password", message= "Passwords Doesn't Match")
    ])

    register = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    login = SubmitField("Login")


class ContactUsForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    yourmessage = TextAreaField("Your Message", validators=[DataRequired()])

    submit = SubmitField("Send")

# class AddCommentForm(FlaskForm):
#     comment = StringField("Write your comment here...", validators=[DataRequired])
#
#     submit = SubmitField("Post Comment")