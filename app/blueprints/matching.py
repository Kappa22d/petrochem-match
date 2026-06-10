"""Smart matching engine blueprint."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import Profile, Match, db
from app.utils import calculate_compatibility_score
import uuid

matching_bp = Blueprint('matching', __name__)


def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return Profile.query.filter_by(id=uuid.UUID(user_id)).first()
    return None


@matching_bp.route('/find-matches')
def find_matches():
    user = get_current_user()
    if not user:
        flash('Please log in first', 'warning')
        return redirect(url_for('auth.login'))
    
    all_profiles = Profile.query.filter(Profile.id != user.id).all()
    
    matches = []
    for profile in all_profiles:
        score = calculate_compatibility_score(user, profile)
        if score > 0.4:
            matches.append({
                'profile': profile,
                'score': float(score),
                'reason': f"{profile.role.title()} with expertise in {', '.join(profile.expertise_tags[:2] or ['general'])}"
            })
    
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    return render_template('matching/results.html', matches=matches[:20])


@matching_bp.route('/save/<profile_id>', methods=['POST'])
def save_match(profile_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        other_profile = Profile.query.filter_by(id=uuid.UUID(profile_id)).first()
    except:
        return jsonify({'error': 'Profile not found'}), 404
    
    if not other_profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    score = calculate_compatibility_score(user, other_profile)
    
    existing = Match.query.filter(
        ((Match.user_a_id == user.id) & (Match.user_b_id == other_profile.id)) |
        ((Match.user_a_id == other_profile.id) & (Match.user_b_id == user.id))
    ).first()
    
    if not existing:
        match = Match(user_a_id=user.id, user_b_id=other_profile.id, score=score)
        db.session.add(match)
        db.session.commit()
    
    return jsonify({'success': True, 'message': 'Match saved!'})
