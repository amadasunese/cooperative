from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, FileField, BooleanField, SubmitField, DateField
from wtforms import DateTimeField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange, Length
from wtforms.fields import DateTimeLocalField


class MemberForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    other_names = StringField('Other Names', validators=[DataRequired()])
    home_address = StringField('Home Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    telephone_number = StringField('Telephone Number', validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired()])
    next_of_kin_name = StringField('Next of Kin Name', validators=[DataRequired()])
    next_of_kin_phone_number = StringField('Next of Kin Phone Number', validators=[DataRequired()])
    relationship_with_next_of_kin = StringField('Relationship with Next of Kin', validators=[DataRequired()])
    address_of_next_of_kin = StringField('Address of Next of Kin', validators=[DataRequired()])
    monthly_savings = FloatField('Monthly Savings', validators=[DataRequired()])
    share_capital = FloatField('Share Capital')
    passport_photograph = FileField('Passport Photograph')
    # agreement = BooleanField('Agreement', validators=[DataRequired()])
    agreement = BooleanField('I hereby formally apply to be admitted as a member of the above society and promise to abide by the Rules and Regulations, Bye-Laws and any further amendments thereto.', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    date = DateTimeLocalField('Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Length(max=2000)])  # Optional limit on description length
    submit = SubmitField('Add Meeting')

class RSVPForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    date = DateTimeLocalField('Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Length(max=2000)])
    status = SelectField('Status', choices=[('attending', 'Attending'), ('not attending', 'Not Attending')], validators=[DataRequired()])
    submit = SubmitField('RSVP')

class DocumentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    filename = FileField('Document', validators=[DataRequired()])
    submit = SubmitField('Upload')


class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    thumbnail = FileField('Thumbnail')
    submit = SubmitField('Submit')