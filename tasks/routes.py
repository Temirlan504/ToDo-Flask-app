from datetime import datetime, timezone
from flask import abort, flash, redirect, render_template, request, url_for
from tasks import app, bcrypt, db
from .models import Task, User
from .forms import RegisterForm, LoginForm, UpdateAccountForm, TaskForm, UpdateTaskForm
from flask_login import login_required, login_user, current_user, logout_user

@app.route('/')
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', title='My App', tasks=tasks)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', title='Account', form=form)


# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful,' 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Save user to database
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!,', 'success')
        return redirect(url_for('login'))

    return render_template(
        'register.html', title='Register', form=form
    )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# Tasks routes
@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
    form = TaskForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            task = Task(
                title=form.title.data,
                content=form.content.data,
                date_created=datetime.now(timezone.utc),
                user_id=current_user.id
            )
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

    return render_template('new_task.html', title='New Task', form=form)

@app.route('/task/<int:task_id>')
@login_required
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    return render_template('task_detail.html', title=task.title, task=task)

@app.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    
    form = UpdateTaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        db.session.commit()
        return redirect(url_for('task_detail', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.content.data = task.content

    return render_template('new_task.html', title='Update Task', form=form)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))
