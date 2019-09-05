from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, SelectField, SubmitField,TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cancer101.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'password'
db = SQLAlchemy(app)


class Cancer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cancer_name = db.Column(db.String(20))
    cancer_types = db.Column(db.Text(1000))
    cancer_stages = db.Column(db.Text(1000))
    cancer_symptoms = db.Column(db.Text(1000))
    cancer_treatment = db.Column(db.Text(1000))

    def __repr__(self):
        return self.cancer_name


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_name = db.Column(db.String(100))
    quote_author = db.Column(db.String(25))

    def __repr__(self):
        return self.quote_name


class CancerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    types = TextAreaField('Type', validators=[DataRequired()])
    stages = TextAreaField('Stage', validators=[DataRequired()])
    symptoms = TextAreaField('Symptoms', validators=[DataRequired()])
    treatment = TextAreaField('Treatment', validators=[DataRequired()])
    submit = SubmitField('Post Cancer')

class Search(Form):
    choices = [('Type', 'Type'),
               ('Symptom', 'Symptom')]
    select = SelectField('Search for cancer:', choices=choices)
    search = StringField('')



@app.route('/')
def index():
    cancers = Cancer.query.all()
    return render_template('index.html', cancers=cancers)


@app.route('/stage')
def base():
    return render_template('stage.html')


@app.route('/Cancer/post', methods=['GET', 'POST'])
def postCancer():
    form = CancerForm()
    if form.validate_on_submit():
        # if the user adds data //POST
        name = form.name.data
        types = form.types.data
        stages = form.stages.data
        symptoms = form.symptoms.data
        treatment = form.treatment.data
        # save data to the db
        new_cancer = Cancer(cancer_name=name, cancer_types= types, cancer_stages=stages,cancer_symptoms=symptoms,cancer_treatment=treatment)
        db.session.add(new_cancer)
        db.session.commit()

        return redirect('/')
    # if the user visits the post data form//GET
    return render_template('postCancer.html', title='Sign In', form=form)


@app.route('/detail/<int:cancer_id>')
def detail(cancer_id):
    cancer = Cancer.query.filter_by(id=cancer_id).first()

    return render_template('detail.html', cancer=cancer)


@app.route('/detail/delete/<int:cancer_id>')
def delete(cancer_id):
    cancer = Cancer.query.filter_by(id=cancer_id).first()
    db.session.delete(cancer)
    db.session.commit()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title="Internal server error"), 500



if __name__ == '__main__':
    app.run(debug=True, port=2000)
