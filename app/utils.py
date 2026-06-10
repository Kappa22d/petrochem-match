"""Utility functions for PetroChem Match."""
import json
from datetime import datetime


def calculate_compatibility_score(profile_a, profile_b):
    """Calculate compatibility score between two profiles (0.0 - 1.0)."""
    score = 0.0
    
    # Same company penalty
    if profile_a.company and profile_b.company and profile_a.company == profile_b.company:
        return 0.1
    
    # Role-based matching
    role_pairs = {
        ('operator', 'supplier'): 0.8,
        ('operator', 'consultant'): 0.7,
        ('operator', 'engineer'): 0.6,
        ('engineer', 'supplier'): 0.85,
        ('engineer', 'consultant'): 0.75,
        ('supplier', 'consultant'): 0.6,
    }
    
    role_tuple = tuple(sorted([profile_a.role, profile_b.role]))
    score = role_pairs.get(role_tuple, 0.3)
    
    # Expertise overlap bonus
    tags_a = set(profile_a.expertise_tags or [])
    tags_b = set(profile_b.expertise_tags or [])
    if tags_a and tags_b:
        overlap = len(tags_a & tags_b) / max(len(tags_a), len(tags_b))
        score = score * 0.6 + overlap * 0.4
    
    return min(max(score, 0.0), 1.0)


def truncate(text, length=100):
    """Truncate text to specified length."""
    if len(text) > length:
        return text[:length - 3] + '...'
    return text


def format_date(dt):
    """Format datetime for display."""
    if not dt:
        return ''
    return dt.strftime('%B %d, %Y')
