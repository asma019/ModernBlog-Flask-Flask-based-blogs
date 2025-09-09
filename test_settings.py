#!/usr/bin/env python3

# Quick test script to check if settings are being saved/retrieved correctly
from app import app, db, Setting

with app.app_context():
    # Test setting and getting tracking code
    print("Testing Settings...")
    
    # Set a test tracking code
    Setting.set('tracking_code', '<!-- Test Google Analytics -->')
    
    # Retrieve it
    tracking_code = Setting.get('tracking_code')
    print(f"Retrieved tracking_code: '{tracking_code}'")
    
    # Check all settings
    all_settings = Setting.query.all()
    print("\nAll settings in database:")
    for setting in all_settings:
        print(f"  {setting.key}: {setting.value}")
    
    print("\nDone!")