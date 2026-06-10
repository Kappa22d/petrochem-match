"""RFQ (Request for Quote) management blueprint."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import RFQ, RFQResponse, Profile, db
import uuid
from datetime import datetime

rfq_bp = Blueprint('rfq', __name__)


def get_current_user():
    """Get current logged-in user."""
    user_id = session.get('user_id')
    if user_id:
        return Profile.query.filter_by(id=uuid.UUID(user_id)).first()
    return None


@rfq_bp.route('/')
def list_rfqs():
    """List all open RFQs."""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'open')
    per_page = 10
    
    query = RFQ.query
    if status:
        query = query.filter_by(status=status)
    
    rfqs = query.order_by(RFQ.created_at.desc()).paginate(page=page, per_page=per_page)
    return render_template('rfq/list.html', rfqs=rfqs)


@rfq_bp.route('/create', methods=['GET', 'POST'])
def create_rfq():
    """Create a new RFQ."""
    user = get_current_user()
    if not user:
        flash('Please log in first', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        budget_range = request.form.get('budget_range')
        anonymous = request.form.get('anonymous') == 'on'
        
        if not title:
            flash('Title is required', 'danger')
            return redirect(url_for('rfq.create_rfq'))
        
        rfq = RFQ(
            user_id=user.id,
            title=title,
            description=description,
            budget_range=budget_range,
            anonymous=anonymous,
            status='open'
        )
        db.session.add(rfq)
        db.session.commit()
        
        flash(f'RFQ created: {title}', 'success')
        return redirect(url_for('rfq.view_rfq', rfq_id=rfq.id))
    
    return render_template('rfq/create.html')


@rfq_bp.route('/<int:rfq_id>')
def view_rfq(rfq_id):
    """View a specific RFQ."""
    rfq = RFQ.query.filter_by(id=rfq_id).first()
    if not rfq:
        flash('RFQ not found', 'danger')
        return redirect(url_for('rfq.list_rfqs'))
    
    return render_template('rfq/view.html', rfq=rfq)


@rfq_bp.route('/<int:rfq_id>/respond', methods=['POST'])
def respond_to_rfq(rfq_id):
    """Respond to an RFQ."""
    user = get_current_user()
    if not user:
        flash('Please log in first', 'warning')
        return redirect(url_for('auth.login'))
    
    rfq = RFQ.query.filter_by(id=rfq_id).first()
    if not rfq:
        flash('RFQ not found', 'danger')
        return redirect(url_for('rfq.list_rfqs'))
    
    message = request.form.get('message')
    quote_value = request.form.get('quote_value')
    
    response = RFQResponse(
        rfq_id=rfq_id,
        respondent_id=user.id,
        message=message,
        quote_value=quote_value
    )
    db.session.add(response)
    db.session.commit()
    
    flash('Your response has been submitted!', 'success')
    return redirect(url_for('rfq.view_rfq', rfq_id=rfq_id))
