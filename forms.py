from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, length


class UpdateMovieForm(FlaskForm):
    rating = FloatField(label="Rating", validators=[NumberRange(min=0, max=10)])
    review = TextAreaField(label="My Review", validators=[DataRequired(), length(max=250)])
    submit = SubmitField("Update")


class AddUserForm(FlaskForm):
    user_name = StringField(label="Enter User Name", validators=[DataRequired()])
    submit = SubmitField(label="Add User")
