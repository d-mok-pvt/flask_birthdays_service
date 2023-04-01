# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Regexp, Optional


class AddBirthdayForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    date = StringField('date (YYYY-MM-DD)', validators=[DataRequired(),
                                                        Regexp(r'^\d{4}-\d{2}-\d{2}$', message="Invalid date format")])
    csrf_enabled = False


class UpdateBirthdayForm(FlaskForm):
    name = StringField('name', validators=[Optional()])
    date = StringField('date (YYYY-MM-DD)', validators=[Optional(),
                                                        Regexp(r'^\d{4}-\d{2}-\d{2}$', message="Invalid date format")])
    csrf_enabled = False

    def validate(self):
        if not super(UpdateBirthdayForm, self).validate():
            return False

        if not self.name.data and not self.date.data:
            return False

        return True
    
    def _update_data_with_error(self, error_msg):
        if 'data' not in g:
            g.data = {}
        if 'errors' not in g.data:
            g.data['errors'] = []
        g.data['errors'].append(error_msg)
