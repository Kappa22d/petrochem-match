#!/usr/bin/env python
"""Entry point for the PetroChem Match application."""
import os
import sys
from app import create_app, db
from app.models import User, Profile, RFQ, Listing, Match, Chemical

# Load environment variables
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Register models for flask shell."""
    return {
        'db': db,
        'User': User,
        'Profile': Profile,
        'RFQ': RFQ,
        'Listing': Listing,
        'Match': Match,
        'Chemical': Chemical,
    }

if __name__ == '__main__':
    # Run development server
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
