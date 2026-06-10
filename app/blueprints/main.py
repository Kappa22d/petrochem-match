"""Main blueprint - Landing page and general routes."""
from flask import Blueprint, render_template, request
from app.models import Profile, RFQ, Listing

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page."""
    stats = {
        'professionals': Profile.query.count(),
        'rfqs_open': RFQ.query.filter_by(status='open').count(),
        'listings': Listing.query.count(),
    }
    
    featured_categories = [
        {'name': 'Catalysts', 'icon': '🧪', 'description': 'Reaction optimization'},
        {'name': 'Corrosion Inhibitors', 'icon': '🛡️', 'description': 'Pipeline protection'},
        {'name': 'Solvents', 'icon': '💧', 'description': 'Low-emission options'},
        {'name': 'CO₂ Capture', 'icon': '♻️', 'description': 'ESG solutions'},
        {'name': 'Pipeline Additives', 'icon': '🔧', 'description': 'Performance'},
        {'name': 'Consulting', 'icon': '📋', 'description': 'Expert guidance'},
    ]
    
    recent_rfqs = RFQ.query.filter_by(status='open').order_by(RFQ.created_at.desc()).limit(3).all()
    
    return render_template('landing.html', stats=stats, categories=featured_categories, rfqs=recent_rfqs)


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@main_bp.route('/faq')
def faq():
    """FAQ page."""
    faqs = [
        {
            'question': 'How does the matching algorithm work?',
            'answer': 'Our algorithm analyzes role compatibility, expertise tags, location, and past interactions to suggest the best matches.'
        },
        {
            'question': 'Is my data secure?',
            'answer': 'Yes. We use Supabase with enterprise-grade encryption and comply with GDPR standards.'
        },
        {
            'question': 'What industries do you serve?',
            'answer': 'Oil & gas, refining, chemical engineering, and energy sector professionals.'
        },
    ]
    return render_template('faq.html', faqs=faqs)


@main_bp.route('/disclaimer')
def disclaimer():
    """Legal disclaimer."""
    return render_template('disclaimer.html')
