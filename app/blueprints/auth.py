"""Authentication blueprint."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Profile, db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup."""
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        company = request.form.get('company')
        
        if not all([email, full_name, role]):
            flash('All fields are required', 'danger')
            return redirect(url_for('auth.signup'))
        
        if Profile.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.signup'))
        
        profile = Profile(
            email=email,
            full_name=full_name,
            role=role,
            company=company,
            expertise_tags=[]
        )
        db.session.add(profile)
        db.session.commit()
        
        session['user_id'] = str(profile.id)
        session['email'] = profile.email
        
        flash(f'Welcome, {full_name}!', 'success')
        return redirect(url_for('profile.complete_profile'))
    
    roles = ['operator', 'engineer', 'supplier', 'consultant']
    return render_template('auth/signup.html', roles=roles)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        email = request.form.get('email')
        profile = Profile.query.filter_by(email=email).first()
        if not profile:
            flash('Email not found', 'danger')
            return redirect(url_for('auth.login'))
        
        session['user_id'] = str(profile.id)
        session['email'] = profile.email
        flash(f'Welcome back, {profile.full_name}!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
