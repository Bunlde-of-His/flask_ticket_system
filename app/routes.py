from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt, login_manager
from app.models import User, Role, Group, Ticket
from functools import wraps


def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role.name != role_name:
                return login_manager.unauthorized()
            return func(*args, **kwargs)

        return decorated_view

    return decorator


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_name = request.form['role']
        group_name = request.form.get('group')

        if role_name == 'Admin' and User.query.join(Role).filter(Role.name == 'Admin').first():
            flash('The Admin role is already taken.', 'danger')
            return redirect(url_for('register'))

        if role_name in ['Manager', 'Analyst'] and User.query.join(Role).join(Group).filter(Role.name == role_name,
                                                                                            Group.name == group_name).first():
            flash(f'The {role_name} role for {group_name} is already taken.', 'danger')
            return redirect(url_for('register'))

        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
            db.session.commit()

        group = None
        if group_name:
            group = Group.query.filter_by(name=group_name).first()
            if not group:
                group = Group(name=group_name)
                db.session.add(group)
                db.session.commit()

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password, role=role, group=group)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    roles = Role.query.all()
    groups = Group.query.all()
    return render_template('register.html', roles=roles, groups=groups)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    tickets = Ticket.query.all()
    return render_template('index.html', tickets=tickets)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def admin():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        group_name = request.form['group']
        group = Group.query.filter_by(name=group_name).first()
        ticket = Ticket(title=title, description=description, group=group)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('admin'))

    groups = Group.query.all()
    tickets = Ticket.query.all()
    return render_template('admin.html', groups=groups, tickets=tickets)


@app.route('/manager', methods=['GET', 'POST'])
@login_required
@role_required('Manager')
def manager():
    tickets = Ticket.query.filter_by(group_id=current_user.group_id).all()
    if request.method == 'POST':
        ticket_id = request.form['ticket_id']
        status = request.form['status']
        ticket = Ticket.query.get(ticket_id)
        ticket.status = status
        db.session.commit()
        flash('Ticket status updated successfully!', 'success')
        return redirect(url_for('manager'))

    return render_template('manager.html', tickets=tickets)


@app.route('/analyst', methods=['GET', 'POST'])
@login_required
@role_required('Analyst')
def analyst():
    tickets = Ticket.query.filter_by(group_id=current_user.group_id).all()
    if request.method == 'POST':
        ticket_id = request.form['ticket_id']
        description = request.form['description']
        ticket = Ticket.query.get(ticket_id)
        ticket.description = description
        db.session.commit()
        flash('Ticket description updated successfully!', 'success')
        return redirect(url_for('analyst'))

    return render_template('analyst.html', tickets=tickets)


@app.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully!', 'success')
    return redirect(url_for('admin'))
