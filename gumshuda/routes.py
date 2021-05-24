from gumshuda import app, db, bcrypt
from gumshuda.forms import RegistrationForm, LoginForm, addMissingPerson
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from gumshuda.models import User, AddMissingPerson
import os
import secrets
from PIL import Image

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/home')
def home():
    persons = AddMissingPerson.query.order_by(AddMissingPerson.created_at.desc())
    return render_template('home.html', title="Home", persons = persons)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    #grabimg the file ectension
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/lost_images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/add-missing-person', methods=['GET', 'POST'])
@login_required
def add_missing_person():
    form = addMissingPerson()
    if form.validate_on_submit():
        form_image = save_picture(form.image.data)
        missing_person = AddMissingPerson(name=form.name.data, age=form.age.data, 
            height=form.height.data, colour=form.colour.data, 
            lostAt=form.lostAt.data, reward=form.reward.data, gender=form.gender.data, 
            contactNo=form.contactNo.data, image = form_image, created_by = current_user.id, 
            state=form.state.data, country=form.country.data, attire=form.attire.data  )
        db.session.add(missing_person)
        db.session.commit()
        flash('You have successfully added a lost person', 'success')
        return redirect(url_for('home'))
    return render_template('addMissingPerson.html', form=form)

@app.route("/person/<int:person_id>")
def person(person_id):
    person =  AddMissingPerson.query.get_or_404(person_id)
    return render_template('personDetails.html', person = person, title= 'Details')


@app.route('/find', methods=['POST'])
def find():
    state = request.form.get('state')
    results = AddMissingPerson.query.filter_by(state = state).all()
    return render_template('homeFilter.html', results = results)
    

@app.route("/person/<int:person_id>/delete", methods=['POST'])
@login_required
def delete_person(person_id):
    person = AddMissingPerson.query.get_or_404(person_id)
    if person.created_by != current_user.id:
        abort(403)
    db.session.delete(person)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

