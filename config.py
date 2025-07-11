#!/usr/bin/env python3
"""
Global configuration loader for ArcGIS Experience Builder projects
Loads credentials and settings from ~/.config/arcgis/.env
"""
import os
from pathlib import Path
from typing import Dict, Optional

def load_global_config() -> Dict[str, str]:
    """
    Load global ArcGIS configuration from ~/.config/arcgis/.env
    Returns a dictionary of environment variables
    """
    config_path = Path.home() / '.config' / 'arcgis' / '.env'
    
    if not config_path.exists():
        raise FileNotFoundError(f"Global config file not found at {config_path}")
    
    config = {}
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return config

def get_arcgis_credentials() -> Dict[str, str]:
    """Get ArcGIS OAuth credentials"""
    config = load_global_config()
    return {
        'client_id': config.get('ARCGIS_CLIENT_ID'),
        'client_secret': config.get('ARCGIS_CLIENT_SECRET'),
        'portal_url': config.get('ARCGIS_PORTAL_URL', 'https://experience.arcgis.com'),
        'base_experience_id': config.get('ARCGIS_BASE_EXPERIENCE_ID')
    }

def get_deployment_config() -> Dict[str, str]:
    """Get deployment configuration"""
    config = load_global_config()
    return {
        'pythonanywhere_username': config.get('PYTHONANYWHERE_USERNAME'),
        'pythonanywhere_domain': config.get('PYTHONANYWHERE_DOMAIN'),
        'menu_api_password': config.get('MENU_API_PASSWORD'),
        'menu_api_base_url': config.get('MENU_API_BASE_URL')
    }

def build_experience_url(page_id: str, experience_id: Optional[str] = None) -> str:
    """
    Build full ArcGIS Experience Builder URL
    
    Args:
        page_id: The page identifier (e.g., 'National', 'Heat-Risk')
        experience_id: Optional custom experience ID (uses default if not provided)
    
    Returns:
        Full URL to the Experience Builder page
    """
    config = get_arcgis_credentials()
    exp_id = experience_id or config['base_experience_id']
    portal_url = config['portal_url']
    
    return f"{portal_url}/experience/{exp_id}/page/{page_id}"

def create_menu_item(label: str, page_id: str, search_terms: str = "", 
                    experience_id: Optional[str] = None) -> Dict[str, str]:
    """
    Create a standardized menu item dictionary
    
    Args:
        label: Display text for the menu button
        page_id: ArcGIS Experience Builder page ID
        search_terms: Additional search terms for filtering
        experience_id: Optional custom experience ID
    
    Returns:
        Dictionary with label, href, and term keys
    """
    return {
        "label": label,
        "href": build_experience_url(page_id, experience_id),
        "term": search_terms or label
    }

if __name__ == "__main__":
    # Test the configuration loader
    try:
        config = load_global_config()
        print("✅ Global config loaded successfully")
        print(f"   ArcGIS Client ID: {config.get('ARCGIS_CLIENT_ID', 'Not found')}")
        print(f"   Portal URL: {config.get('ARCGIS_PORTAL_URL', 'Not found')}")
        
        # Test URL building
        test_url = build_experience_url("National")
        print(f"   Test URL: {test_url}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")