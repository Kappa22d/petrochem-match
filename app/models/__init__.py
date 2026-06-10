"""SQLAlchemy models for PetroChem Match."""
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, DateTime, Integer, String, Text, Boolean, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

def init_db(app):
    """Initialize database with app."""
    db.init_app(app)
    return db


class Profile(db.Model):
    """User profile extended from Supabase auth."""
    __tablename__ = 'profiles'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(String(255), unique=True, nullable=False)
    full_name = db.Column(String(255))
    role = db.Column(String(50), nullable=False)
    company = db.Column(String(255))
    bio = db.Column(Text)
    location = db.Column(String(255))
    expertise_tags = db.Column(JSON, default=list)
    years_experience = db.Column(Integer)
    avatar_url = db.Column(String(512))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    rfqs = relationship('RFQ', back_populates='author', foreign_keys='RFQ.user_id')
    listings = relationship('Listing', back_populates='author')
    matches_as_a = relationship('Match', foreign_keys='Match.user_a_id', back_populates='user_a')
    matches_as_b = relationship('Match', foreign_keys='Match.user_b_id', back_populates='user_b')
    
    def __repr__(self):
        return f'<Profile {self.full_name} ({self.role})>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'company': self.company,
            'location': self.location,
            'expertise_tags': self.expertise_tags,
        }


class RFQ(db.Model):
    """Request for Quote."""
    __tablename__ = 'rfqs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False)
    title = db.Column(String(255), nullable=False)
    description = db.Column(Text)
    specifications = db.Column(JSON, default=dict)
    status = db.Column(String(50), default='open')
    budget_range = db.Column(String(100))
    anonymous = db.Column(Boolean, default=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = relationship('Profile', foreign_keys=[user_id], back_populates='rfqs')
    responses = relationship('RFQResponse', back_populates='rfq', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<RFQ {self.title}>'


class RFQResponse(db.Model):
    """Response to an RFQ."""
    __tablename__ = 'rfq_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    rfq_id = db.Column(db.Integer, ForeignKey('rfqs.id'), nullable=False)
    respondent_id = db.Column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False)
    message = db.Column(Text)
    quote_value = db.Column(String(100))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    rfq = relationship('RFQ', back_populates='responses')
    respondent = relationship('Profile')


class Listing(db.Model):
    """Product/service listing from suppliers."""
    __tablename__ = 'listings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False)
    title = db.Column(String(255), nullable=False)
    description = db.Column(Text)
    category = db.Column(String(100))
    specifications = db.Column(JSON, default=dict)
    price_range = db.Column(String(100))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = relationship('Profile', back_populates='listings')
    
    def __repr__(self):
        return f'<Listing {self.title}>'


class Match(db.Model):
    """Compatibility match between two users."""
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_a_id = db.Column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False)
    user_b_id = db.Column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False)
    score = db.Column(Numeric(3, 2))
    reason = db.Column(Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    user_a = relationship('Profile', foreign_keys=[user_a_id], back_populates='matches_as_a')
    user_b = relationship('Profile', foreign_keys=[user_b_id], back_populates='matches_as_b')


class Chemical(db.Model):
    """Chemical database for lookup tool."""
    __tablename__ = 'chemicals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(255), nullable=False, unique=True)
    cas_number = db.Column(String(20), unique=True)
    formula = db.Column(String(100))
    molecular_weight = db.Column(Numeric(10, 4))
    properties = db.Column(JSON, default=dict)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cas_number': self.cas_number,
            'formula': self.formula,
            'properties': self.properties,
        }
