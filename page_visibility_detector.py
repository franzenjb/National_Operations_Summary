#!/usr/bin/env python3
"""
ArcGIS Experience Builder Page Visibility Detector
Automatically detects which pages should be hidden from menus
"""
import requests
import json
from config import get_arcgis_credentials

def get_arcgis_token():
    """Get ArcGIS OAuth token"""
    creds = get_arcgis_credentials()
    
    token_url = 'https://www.arcgis.com/sharing/rest/oauth2/token'
    token_data = {
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'grant_type': 'client_credentials',
        'f': 'json'
    }
    
    response = requests.post(token_url, data=token_data)
    result = response.json()
    return result.get('access_token')

def should_hide_page(page_id, page_data):
    """
    Determine if a page should be hidden from menu based on various criteria
    
    Args:
        page_id: Page ID (e.g., 'page_123')
        page_data: Page configuration data from ArcGIS API
    
    Returns:
        bool: True if page should be hidden from menu
    """
    page_label = page_data.get('label', '').lower()
    
    # Rule 1: Pages explicitly marked as not visible
    if not page_data.get('visible', True):
        return True
    
    # Rule 2: Pages not shown in navigation
    if not page_data.get('showInNav', True):
        return True
    
    # Rule 3: Test/development pages
    test_keywords = ['test', 'beta', 'old', 'temp', 'draft', 'dev', 'debug']
    if any(keyword in page_label for keyword in test_keywords):
        return True
    
    # Rule 4: Under construction indicators
    construction_keywords = ['construction', 'wip', 'todo', 'pending', 'coming soon']
    if any(keyword in page_label for keyword in construction_keywords):
        return True
    
    # Rule 5: Admin/internal pages
    admin_keywords = ['admin', 'internal', 'private', 'restricted access']
    if any(keyword in page_label for keyword in admin_keywords):
        return True
    
    # Rule 6: Specific pages that should be hidden (manual overrides)
    hidden_page_ids = [
        'page_154',  # OLD
        'page_181',  # Trucks_Trailers Test
        'page_129',  # DAT Dispatch (per user request)
        'page_130'   # DRO Call Center (per user request)
    ]
    if page_id in hidden_page_ids:
        return True
    
    # Rule 7: Check if page has minimal content (might be placeholder)
    # This would require deeper inspection of page layout
    
    return False

def get_visible_pages(experience_id):
    """
    Get all pages from Experience Builder and filter out hidden ones
    
    Args:
        experience_id: ArcGIS Experience Builder ID
        
    Returns:
        dict: {page_id: page_data} for visible pages only
    """
    token = get_arcgis_token()
    
    exp_url = f'https://www.arcgis.com/sharing/rest/content/items/{experience_id}/data'
    response = requests.get(exp_url, params={'token': token, 'f': 'json'})
    exp_data = response.json()
    
    if 'pages' not in exp_data:
        return {}
    
    visible_pages = {}
    hidden_pages = {}
    
    for page_id, page_data in exp_data['pages'].items():
        if should_hide_page(page_id, page_data):
            hidden_pages[page_id] = page_data
        else:
            visible_pages[page_id] = page_data
    
    # Print summary
    print(f"📊 Page Visibility Analysis:")
    print(f"   ✅ Visible: {len(visible_pages)} pages")
    print(f"   ❌ Hidden: {len(hidden_pages)} pages")
    print()
    
    if hidden_pages:
        print("🔒 Hidden Pages:")
        for page_id, page_data in hidden_pages.items():
            reason = get_hide_reason(page_id, page_data)
            print(f"   {page_id}: {page_data.get('label', 'Unknown')} - {reason}")
        print()
    
    return visible_pages

def get_hide_reason(page_id, page_data):
    """Get the reason why a page is hidden"""
    page_label = page_data.get('label', '').lower()
    
    if not page_data.get('visible', True):
        return "Not visible"
    if not page_data.get('showInNav', True):
        return "Hidden from navigation"
    if any(kw in page_label for kw in ['test', 'beta', 'old']):
        return "Test/development page"
    if page_id in ['page_154', 'page_181', 'page_129', 'page_130']:
        return "Manual override"
    
    return "Unknown reason"

def validate_menu_against_visibility(menu_data, experience_id):
    """
    Check current menu against page visibility and report issues
    
    Args:
        menu_data: Current menu configuration
        experience_id: ArcGIS Experience Builder ID
    """
    visible_pages = get_visible_pages(experience_id)
    visible_page_ids = set(visible_pages.keys())
    
    issues = []
    
    for category in menu_data:
        for link in category['links']:
            # Extract page ID from href
            if '/page/' in link['href']:
                page_id = link['href'].split('/page/')[-1]
                
                if page_id not in visible_page_ids:
                    issues.append({
                        'category': category['category'],
                        'label': link['label'],
                        'page_id': page_id,
                        'issue': 'Links to hidden page'
                    })
    
    if issues:
        print("⚠️  Menu Issues Found:")
        for issue in issues:
            print(f"   {issue['category']} > {issue['label']} ({issue['page_id']}) - {issue['issue']}")
    else:
        print("✅ Menu is clean - no links to hidden pages")
    
    return issues

if __name__ == "__main__":
    experience_id = 'ce0b7dc7574c49a8a82f36443fee494f'
    
    print("🔍 Analyzing page visibility...")
    visible_pages = get_visible_pages(experience_id)
    
    # Check current menu
    try:
        with open('menu.json', 'r') as f:
            menu_data = json.load(f)
        
        print("🔍 Validating current menu...")
        validate_menu_against_visibility(menu_data, experience_id)
        
    except FileNotFoundError:
        print("❌ menu.json not found")