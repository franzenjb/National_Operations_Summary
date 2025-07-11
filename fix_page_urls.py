#!/usr/bin/env python3
"""
Fix menu URLs to use actual ArcGIS Experience Builder page IDs
"""
import json

# Mapping from your current menu labels to actual page IDs
PAGE_MAPPING = {
    'National': 'page_84',
    'Heat Risk': 'page_95', 
    'FY 25 Incidents': 'page_96',
    'DCS 5 Year Plan': 'page_97',
    'DCS Narrative': 'page_98',
    'Global Trends': 'page_99',
    'DOCC Portal': 'page_100',
    'Current OPS Report': 'page_101',
    'Power Outages': 'page_102',
    'Storm Prediction Center': 'page_104',
    'Precipitation': 'page_106',
    'Flood Prediction': 'page_107',
    'Natl Hurricane Center': 'page_108',
    'Air Reconnaissance': 'page_161',  # Note: was "Air Reconnaisance" in API
    '7 DAY Fire Risk': 'page_109',
    'California EMS': 'page_111',
    'Natl Interagency FIRE': 'page_112',
    'Weather - General': 'page_173',
    'Tropical Hazards': 'page_174',
    'Fire Weather': 'page_175',
    'National Sheltering': 'page_114',
    'Current Open Shelters': 'page_122',
    'Shelter Intake': 'page_123',
    'SCIA Operational Dashboard': 'page_176',
    'Restricted SCIA Access Request': 'page_177',
    'Staffing': 'page_116',
    'Staff Capacity Building': 'page_168',
    'EBV - Event Volunteers': 'page_124',
    'DST - Disaster Tech': 'page_125',
    'IKD - InKind Donations': 'page_126',
    'Trailers & Assets': 'page_127',
    'ERV - Emergency vehicles': 'page_128',
    'Resourcing': 'page_150',
    'Speed to Scale': 'page_169',
    '1 800 Red Cross': 'page_117',
    'DOCC Current OPS': 'page_119',
    'NIC Teams DRO Leadership': 'page_132',
    'Active DROs': 'page_133',
    'Natl Activation Levels': 'page_134',
    'DRO Call Agenda': 'page_135',
    'Dist Partner Hub': 'page_136',
    'Hurricane Advance Planning': 'page_170',
    'DR 503-25 South Texas': 'page_139',
    'DR 535-25 Missouri/Ark': 'page_140',
    'DR 539-25 Kentucky': 'page_141',
    'DR 540-25 Tennessee': 'page_155',
    'DR 548-25 Indiana': 'page_156',
    'DR 550-25 Illinois': 'page_157',
    'DR 515-25 Harney, Oregon': 'page_158',
    'DR 497-25 Oklahoma': 'page_159',
    'DR Comp BETA': 'page_172',
    'Client Assistance': 'page_118',
    'IDC Financial': 'page_142',
    'Bridge': 'page_162',
    'DAT': 'page_171',
    'Level 1-2 Casework FA': 'page_163',
    'Request Access': 'page_164',
    'Disaster Current OPs Dashboard': 'page_165',
    "Nat'l Operations - Client Assistance": 'page_166',
    'Bridge Dashboard Historical Info': 'page_167',
    'Regional Risk Tool': 'page_120',
    'CAP Website': 'page_121',
    'Housing Resources': 'page_149'
}

BASE_URL = 'https://experience.arcgis.com/experience/ce0b7dc7574c49a8a82f36443fee494f/page/'

def fix_menu_urls():
    """Fix all URLs in menu.json to use correct page IDs"""
    
    # Read current menu
    with open('menu.json', 'r') as f:
        menu_data = json.load(f)
    
    print("🔧 Fixing menu URLs...")
    
    fixed_count = 0
    missing_count = 0
    
    # Update each category
    for category in menu_data:
        print(f"\n📂 Category: {category['category']}")
        
        for link in category['links']:
            label = link['label']
            old_href = link['href']
            
            if label in PAGE_MAPPING:
                page_id = PAGE_MAPPING[label]
                new_href = BASE_URL + page_id
                link['href'] = new_href
                print(f"  ✅ {label}: {page_id}")
                fixed_count += 1
            else:
                print(f"  ❌ MISSING: {label}")
                missing_count += 1
    
    # Save updated menu
    with open('menu_fixed.json', 'w') as f:
        json.dump(menu_data, f, indent=2)
    
    print(f"\n📊 Summary:")
    print(f"  ✅ Fixed: {fixed_count} URLs")
    print(f"  ❌ Missing: {missing_count} URLs")
    print(f"  💾 Saved to: menu_fixed.json")
    
    if missing_count == 0:
        print("\n🎉 All URLs fixed! Replace menu.json with menu_fixed.json")
    else:
        print("\n⚠️  Some URLs need manual mapping")

if __name__ == "__main__":
    fix_menu_urls()