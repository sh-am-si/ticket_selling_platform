from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email



class HomeForm(FlaskForm):
    play_select = SelectField(label='Select play',
                              coerce=int,
                              validators=[DataRequired()]
                              )

    first_name = StringField(label='First name',
                             default='Francis',
                             validators=[DataRequired(),
                                         Length(min=2, max=30)]
                             )

    last_name = StringField(label='Last name',
                            default='Bacon',
                            validators=[DataRequired(),
                                        Length(min=2, max=30)])

    email = StringField(label='Email',
                        default='france@is.bacon',
                        validators=[DataRequired(),
                                    Email()])

    ticket_select = SelectField(label='Select category',
                                coerce=int,
                                validators=[DataRequired()])

    submit = SubmitField(label='Reserve Ticket')


class StatsForm(FlaskForm):
    play_select = SelectField(label='Select play',
                              coerce=int,
                              validators=[DataRequired()]
                              )

    submit = SubmitField(label='Show statistics')

