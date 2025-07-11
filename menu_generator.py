#!/usr/bin/env python3
"""
Reusable ArcGIS Experience Builder Menu Generator
Creates menu.json files with automatic link generation and page visibility detection
"""
import json
from typing import List, Dict, Any
from config import create_menu_item, get_arcgis_credentials
from page_visibility_detector import get_visible_pages, should_hide_page

class MenuGenerator:
    """Generate menu configurations for ArcGIS Experience Builder projects"""
    
    def __init__(self, experience_id: str = None):
        """
        Initialize menu generator
        
        Args:
            experience_id: Optional custom experience ID (uses global default if not provided)
        """
        self.experience_id = experience_id
        self.config = get_arcgis_credentials()
    
    def create_category(self, category_name: str, color: str, items: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Create a menu category with multiple items
        
        Args:
            category_name: Display name for the category
            color: CSS color class (e.g., 'btn-purple', 'btn-blue')
            items: List of menu items with 'label', 'page_id', and optional 'search_terms'
        
        Returns:
            Complete category dictionary
        """
        links = []
        for item in items:
            menu_item = create_menu_item(
                label=item['label'],
                page_id=item['page_id'],
                search_terms=item.get('search_terms', ''),
                experience_id=self.experience_id
            )
            links.append(menu_item)
        
        return {
            "category": category_name,
            "color": color,
            "links": links
        }
    
    def generate_national_operations_menu(self) -> List[Dict[str, Any]]:
        """Generate the complete National Operations Summary menu"""
        
        categories = []
        
        # 1 Situation Summary
        categories.append(self.create_category(
            "1 Situation Summary", "btn-purple", [
                {"label": "National", "page_id": "National"},
                {"label": "Heat Risk", "page_id": "Heat-Risk"},
                {"label": "FY 25 Incidents", "page_id": "FY-25-Incidents", "search_terms": "FY25 Incidents and DROs"},
                {"label": "DCS 5 Year Plan", "page_id": "DCS-5-Year-Plan", "search_terms": "DCS 5YR Plan"},
                {"label": "DCS Narrative", "page_id": "DCS-Narrative"},
                {"label": "Global Trends", "page_id": "Global-Trends"},
                {"label": "DOCC Portal", "page_id": "DOCC-Portal"},
                {"label": "Current OPS Report", "page_id": "Current-OPS-Report", "search_terms": "Current OPS Rep"},
                {"label": "Power Outages", "page_id": "Power-Outages"}
            ]
        ))
        
        # 2 Weather
        categories.append(self.create_category(
            "2 Weather", "btn-blue", [
                {"label": "Storm Prediction Center", "page_id": "Storm-Prediction-Center"},
                {"label": "Precipitation", "page_id": "Precipitation"},
                {"label": "Flood Prediction", "page_id": "Flood-Prediction"},
                {"label": "Natl Hurricane Center", "page_id": "Natl-Hurricane-Center"},
                {"label": "Air Reconnaissance", "page_id": "Air-Reconnaissance"},
                {"label": "7 DAY Fire Risk", "page_id": "7-DAY-Fire-Risk", "search_terms": "7 Day Fire Risk"},
                {"label": "California EMS", "page_id": "California-EMS"},
                {"label": "Natl Interagency FIRE", "page_id": "Natl-Interagency-FIRE", "search_terms": "Natl Interagency Fire"},
                {"label": "Weather - General", "page_id": "Weather-General", "search_terms": "Weather General"},
                {"label": "Tropical Hazards", "page_id": "Tropical-Hazards"},
                {"label": "Fire Weather", "page_id": "Fire-Weather"},
                {"label": "National Sheltering", "page_id": "National-Sheltering"},
                {"label": "Current Open Shelters", "page_id": "Current-Open-Shelters"},
                {"label": "Shelter Intake", "page_id": "Shelter-Intake"},
                {"label": "SCIA Operational Dashboard", "page_id": "SCIA-Operational-Dashboard"},
                {"label": "Restricted SCIA Access Request", "page_id": "Restricted-SCIA-Access-Request"}
            ]
        ))
        
        # 4 Logistics
        categories.append(self.create_category(
            "4 Logistics", "btn-green", [
                {"label": "Staffing", "page_id": "Staffing"},
                {"label": "Staff Capacity Building", "page_id": "Staff-Capacity-Building"},
                {"label": "EBV - Event Volunteers", "page_id": "EBV-Event-Volunteers", "search_terms": "EBV Event Volunteers"},
                {"label": "DST - Disaster Tech", "page_id": "DST-Disaster-Tech", "search_terms": "DST Disaster Tech"},
                {"label": "IKD - InKind Donations", "page_id": "IKD-InKind-Donations", "search_terms": "IKD InKind Donations"},
                {"label": "Trailers & Assets", "page_id": "Trailers-Assets", "search_terms": "Trailers Assets"},
                {"label": "ERV - Emergency vehicles", "page_id": "ERV-Emergency-vehicles", "search_terms": "ERV Emergency vehicles"},
                {"label": "Resourcing", "page_id": "Resourcing"},
                {"label": "Speed to Scale", "page_id": "Speed-to-Scale"},
                {"label": "1 800 Red Cross", "page_id": "1-800-Red-Cross"}
            ]
        ))
        
        # 6 SADS & DRO
        categories.append(self.create_category(
            "6 SADS & DRO", "btn-orange", [
                {"label": "DOCC Current OPS", "page_id": "DOCC-Current-OPS"},
                {"label": "NIC Teams DRO Leadership", "page_id": "NIC-Teams-DRO-Leadership"},
                {"label": "Active DROs", "page_id": "Active-DROs"},
                {"label": "Natl Activation Levels", "page_id": "Natl-Activation-Levels"},
                {"label": "DRO Call Agenda", "page_id": "DRO-Call-Agenda"},
                {"label": "Dist Partner Hub", "page_id": "Dist-Partner-Hub"},
                {"label": "Hurricane Advance Planning", "page_id": "Hurricane-Advance-Planning"},
                {"label": "DR 503-25 South Texas", "page_id": "DR-503-25-South-Texas"},
                {"label": "DR 535-25 Missouri/Ark", "page_id": "DR-535-25-Missouri-Ark"},
                {"label": "DR 539-25 Kentucky", "page_id": "DR-539-25-Kentucky"},
                {"label": "DR 540-25 Tennessee", "page_id": "DR-540-25-Tennessee"},
                {"label": "DR 548-25 Indiana", "page_id": "DR-548-25-Indiana"},
                {"label": "DR 550-25 Illinois", "page_id": "DR-550-25-Illinois"},
                {"label": "DR 515-25 Harney, Oregon", "page_id": "DR-515-25-Harney-Oregon"},
                {"label": "DR 497-25 Oklahoma", "page_id": "DR-497-25-Oklahoma"},
                {"label": "DR Comp BETA", "page_id": "DR-Comp-BETA", "search_terms": "DR Comp BETA Tool"}
            ]
        ))
        
        # 7 Financial Asst DAT
        categories.append(self.create_category(
            "7 Financial Asst DAT", "btn-red", [
                {"label": "Client Assistance", "page_id": "Client-Assistance"},
                {"label": "IDC Financial", "page_id": "IDC-Financial"},
                {"label": "Bridge", "page_id": "Bridge"},
                {"label": "DAT", "page_id": "DAT"},
                {"label": "Level 1-2 Casework FA", "page_id": "Level-1-2-Casework-FA"},
                {"label": "Request Access", "page_id": "Request-Access"},
                {"label": "Disaster Current OPs Dashboard", "page_id": "Disaster-Current-OPs-Dashboard"},
                {"label": "Nat'l Operations - Client Assistance", "page_id": "Natl-Operations-Client-Assistance", "search_terms": "Natl Operations Client Assistance"},
                {"label": "Bridge Dashboard Historical Info", "page_id": "Bridge-Dashboard-Historical-Info"}
            ]
        ))
        
        # 8 Regional Risk Tool
        categories.append(self.create_category(
            "8 Regional Risk Tool", "btn-black", [
                {"label": "Regional Risk Tool", "page_id": "Regional-Risk-Tool"}
            ]
        ))
        
        # 9 Community Adaptation CAP
        categories.append(self.create_category(
            "9 Community Adaptation CAP", "btn-black", [
                {"label": "CAP Website", "page_id": "CAP-Website"},
                {"label": "Housing Resources", "page_id": "Housing-Resources"}
            ]
        ))
        
        return categories
    
    def validate_menu_visibility(self, menu_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate menu against page visibility and remove hidden pages
        
        Args:
            menu_data: Menu data to validate
            
        Returns:
            Cleaned menu data with hidden pages removed
        """
        if not self.experience_id:
            print("⚠️  No experience ID set, skipping visibility validation")
            return menu_data
        
        try:
            visible_pages = get_visible_pages(self.experience_id)
            visible_page_ids = set(visible_pages.keys())
            
            cleaned_menu = []
            removed_items = []
            
            for category in menu_data:
                cleaned_links = []
                
                for link in category['links']:
                    # Extract page ID from href
                    if '/page/' in link['href']:
                        page_id = link['href'].split('/page/')[-1]
                        
                        if page_id in visible_page_ids:
                            cleaned_links.append(link)
                        else:
                            removed_items.append({
                                'category': category['category'],
                                'label': link['label'],
                                'page_id': page_id
                            })
                    else:
                        # Keep non-page links (external URLs, etc.)
                        cleaned_links.append(link)
                
                # Only include category if it has visible links
                if cleaned_links:
                    category_copy = category.copy()
                    category_copy['links'] = cleaned_links
                    cleaned_menu.append(category_copy)
            
            if removed_items:
                print(f"🔒 Removed {len(removed_items)} hidden pages from menu:")
                for item in removed_items:
                    print(f"   {item['category']} > {item['label']} ({item['page_id']})")
            else:
                print("✅ All menu items are visible")
            
            return cleaned_menu
            
        except Exception as e:
            print(f"⚠️  Visibility validation failed: {e}")
            print("   Using original menu without validation")
            return menu_data

    def save_menu(self, menu_data: List[Dict[str, Any]], filename: str = "menu.json", validate_visibility: bool = True):
        """
        Save menu data to JSON file with optional visibility validation
        
        Args:
            menu_data: Menu data to save
            filename: Output filename
            validate_visibility: Whether to validate against page visibility
        """
        if validate_visibility:
            menu_data = self.validate_menu_visibility(menu_data)
        
        with open(filename, 'w') as f:
            json.dump(menu_data, f, indent=2)
        print(f"✅ Menu saved to {filename}")
    
    def create_custom_menu_template(self) -> Dict[str, Any]:
        """Create a template for custom menu configurations"""
        return {
            "menu_title": "Your Custom Menu",
            "categories": [
                {
                    "category_name": "Example Category",
                    "color": "btn-blue",
                    "items": [
                        {
                            "label": "Example Button",
                            "page_id": "Your-Page-ID",
                            "search_terms": "optional search terms"
                        }
                    ]
                }
            ]
        }

def main():
    """Generate menu for National Operations Summary"""
    print("🔧 Generating National Operations Summary Menu...")
    
    # Create menu generator
    generator = MenuGenerator()
    
    # Generate menu data
    menu_data = generator.generate_national_operations_menu()
    
    # Save to file
    generator.save_menu(menu_data)
    
    print(f"📊 Generated {len(menu_data)} categories")
    for category in menu_data:
        print(f"   - {category['category']}: {len(category['links'])} items")

if __name__ == "__main__":
    main()