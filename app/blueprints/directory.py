"""Directory and search blueprint."""
from flask import Blueprint, render_template, request, url_for
from app.models import Profile, db
from sqlalchemy import or_, and_

directory_bp = Blueprint('directory', __name__)


@directory_bp.route('/')
def index():
    """Directory listing with search and filters."""
    query = request.args.get('q', '')
    role = request.args.get('role', '')
    location = request.args.get('location', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    q = Profile.query
    
    if query:
        q = q.filter(
            or_(
                Profile.full_name.ilike(f'%{query}%'),
                Profile.company.ilike(f'%{query}%'),
                Profile.bio.ilike(f'%{query}%')
            )
        )
    
    if role:
        q = q.filter_by(role=role)
    
    if location:
        q = q.filter(Profile.location.ilike(f'%{location}%'))
    
    profiles = q.paginate(page=page, per_page=per_page)
    roles = ['operator', 'engineer', 'supplier', 'consultant']
    
    return render_template(
        'directory/index.html',
        profiles=profiles,
        roles=roles,
        current_query=query,
        current_role=role,
        current_location=location
    )


@directory_bp.route('/search')
def search():
    """API endpoint for AJAX search."""
    query = request.args.get('q', '')
    results = Profile.query.filter(
        or_(
            Profile.full_name.ilike(f'%{query}%'),
            Profile.company.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    return {
        'results': [{'id': str(p.id), 'name': p.full_name, 'company': p.company} for p in results]
    }
