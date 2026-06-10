"""Profile management blueprint."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Profile, RFQ, Match, db
import uuid

profile_bp = Blueprint('profile', __name__)


def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return Profile.query.filter_by(id=uuid.UUID(user_id)).first()
    return None


@profile_bp.route('/complete', methods=['GET', 'POST'])
def complete_profile():
    user = get_current_user()
    if not user:
        flash('Please log in first', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        user.bio = request.form.get('bio')
        user.location = request.form.get('location')
        user.years_experience = request.form.get('years_experience', type=int)
        tags = request.form.get('expertise_tags', '').split(',')
        user.expertise_tags = [tag.strip() for tag in tags if tag.strip()]
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('profile.view_profile', user_id=user.id))
    
    return render_template('profile/complete.html', user=user)


@profile_bp.route('/<user_id>')
def view_profile(user_id):
    try:
        profile = Profile.query.filter_by(id=uuid.UUID(user_id)).first()
    except:
        profile = None
    
    if not profile:
        flash('Profile not found', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('profile/view.html', profile=profile)


@profile_bp.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        flash('Please log in first', 'warning')
        return redirect(url_for('auth.login'))
    
    user_rfqs = RFQ.query.filter_by(user_id=user.id).all()
    user_matches = Match.query.filter(
        (Match.user_a_id == user.id) | (Match.user_b_id == user.id)
    ).all()
    
    return render_template('profile/dashboard.html', user=user, rfqs=user_rfqs, matches=user_matches)
