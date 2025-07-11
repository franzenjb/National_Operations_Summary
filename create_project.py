#!/usr/bin/env python3
"""
ArcGIS Experience Builder Menu Project Generator
Creates new reusable menu projects with all necessary files
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from config import create_menu_item

class ProjectGenerator:
    """Generate new ArcGIS Experience Builder menu projects"""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent
        
    def create_project(self, project_name: str, project_path: str, 
                      experience_id: str, menu_title: str = None,
                      pythonanywhere_subdomain: str = None):
        """
        Create a new ArcGIS Experience Builder menu project
        
        Args:
            project_name: Name of the project (used for file names)
            project_path: Directory where project will be created
            experience_id: ArcGIS Experience Builder ID
            menu_title: Display title for the menu (defaults to project_name)
            pythonanywhere_subdomain: Custom subdomain for PythonAnywhere
        """
        project_path = Path(project_path) / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        menu_title = menu_title or project_name.replace('_', ' ').title()
        subdomain = pythonanywhere_subdomain or f"{project_name.lower()}-jfranzen"
        
        print(f"🚀 Creating ArcGIS Experience Builder Menu Project: {project_name}")
        print(f"📁 Location: {project_path}")
        print(f"🌐 Experience ID: {experience_id}")
        print("=" * 60)
        
        # Copy core files
        self._copy_core_files(project_path)
        
        # Create custom HTML file
        self._create_html_file(project_path, menu_title, project_name)
        
        # Create sample menu configuration
        self._create_sample_menu(project_path, experience_id)
        
        # Create project-specific configuration
        self._create_project_config(project_path, experience_id, subdomain)
        
        # Create deployment scripts
        self._create_deployment_scripts(project_path, project_name)
        
        # Create README
        self._create_readme(project_path, project_name, menu_title, experience_id)
        
        print("✅ Project created successfully!")
        print(f"📋 Next steps:")
        print(f"   1. cd {project_path}")
        print(f"   2. Edit project_config.py to customize your menu")
        print(f"   3. Run: python generate_menu.py")
        print(f"   4. Run: python deploy.py")
        
    def _copy_core_files(self, project_path: Path):
        """Copy core utility files"""
        core_files = ['config.py']
        
        for file_name in core_files:
            src = self.template_dir / file_name
            dst = project_path / file_name
            if src.exists():
                shutil.copy2(src, dst)
                print(f"📄 Copied: {file_name}")
    
    def _create_html_file(self, project_path: Path, menu_title: str, project_name: str):
        """Create customized HTML file"""
        
        # Read the template HTML
        template_html = self.template_dir / 'index.html'
        with open(template_html, 'r') as f:
            html_content = f.read()
        
        # Customize the HTML
        html_content = html_content.replace(
            'National Operations Summary (NOS)',
            f'{menu_title}'
        )
        html_content = html_content.replace(
            'National Operations Summary',
            menu_title
        )
        html_content = html_content.replace(
            'National Operating Summary',
            menu_title
        )
        
        # Write customized HTML
        with open(project_path / 'index.html', 'w') as f:
            f.write(html_content)
        
        print(f"📄 Created: index.html (customized for {menu_title})")
    
    def _create_sample_menu(self, project_path: Path, experience_id: str):
        """Create a sample menu configuration"""
        sample_menu = [
            {
                "category": "Sample Category 1",
                "color": "btn-blue",
                "links": [
                    create_menu_item("Sample Page 1", "Page-1", "sample search terms", experience_id),
                    create_menu_item("Sample Page 2", "Page-2", "more search terms", experience_id)
                ]
            },
            {
                "category": "Sample Category 2", 
                "color": "btn-green",
                "links": [
                    create_menu_item("Another Page", "Another-Page", "different terms", experience_id),
                    create_menu_item("Final Page", "Final-Page", "final terms", experience_id)
                ]
            }
        ]
        
        with open(project_path / 'menu.json', 'w') as f:
            json.dump(sample_menu, f, indent=2)
        
        print("📄 Created: menu.json (sample configuration)")
    
    def _create_project_config(self, project_path: Path, experience_id: str, subdomain: str):
        """Create project-specific configuration"""
        config_content = f'''#!/usr/bin/env python3
"""
Project-specific configuration for ArcGIS Experience Builder menu
Customize this file for your specific Experience Builder
"""
from config import create_menu_item
from menu_generator import MenuGenerator

# Project Configuration
PROJECT_NAME = "{project_path.name}"
EXPERIENCE_ID = "{experience_id}"
PYTHONANYWHERE_SUBDOMAIN = "{subdomain}"

class CustomMenuGenerator(MenuGenerator):
    """Custom menu generator for this project"""
    
    def __init__(self):
        super().__init__(experience_id=EXPERIENCE_ID)
    
    def generate_custom_menu(self):
        """
        Define your custom menu structure here
        
        Returns:
            List of category dictionaries
        """
        categories = []
        
        # Example category - customize as needed
        categories.append(self.create_category(
            "Main Dashboard", "btn-blue", [
                {{"label": "Overview", "page_id": "Overview"}},
                {{"label": "Analytics", "page_id": "Analytics"}},
                {{"label": "Reports", "page_id": "Reports"}}
            ]
        ))
        
        # Add more categories as needed
        categories.append(self.create_category(
            "Operations", "btn-green", [
                {{"label": "Current Status", "page_id": "Current-Status"}},
                {{"label": "Historical Data", "page_id": "Historical-Data"}},
                {{"label": "Planning Tools", "page_id": "Planning-Tools"}}
            ]
        ))
        
        return categories

def generate_menu():
    """Generate and save the menu for this project"""
    generator = CustomMenuGenerator()
    menu_data = generator.generate_custom_menu()
    generator.save_menu(menu_data)
    return menu_data

if __name__ == "__main__":
    generate_menu()
'''
        
        with open(project_path / 'project_config.py', 'w') as f:
            f.write(config_content)
        
        print("📄 Created: project_config.py (customizable menu configuration)")
    
    def _create_deployment_scripts(self, project_path: Path, project_name: str):
        """Create deployment scripts"""
        
        # Simple menu generator script
        generate_script = '''#!/usr/bin/env python3
"""Generate menu.json for this project"""
from project_config import generate_menu

if __name__ == "__main__":
    print("🔧 Generating menu for this project...")
    menu_data = generate_menu()
    print(f"✅ Generated {len(menu_data)} categories")
'''
        
        with open(project_path / 'generate_menu.py', 'w') as f:
            f.write(generate_script)
        
        # Copy deployment script
        deploy_src = self.template_dir / 'deploy.py'
        deploy_dst = project_path / 'deploy.py'
        if deploy_src.exists():
            shutil.copy2(deploy_src, deploy_dst)
        
        print("📄 Created: generate_menu.py (menu generation script)")
        print("📄 Created: deploy.py (deployment script)")
    
    def _create_readme(self, project_path: Path, project_name: str, 
                      menu_title: str, experience_id: str):
        """Create project README"""
        readme_content = f'''# {menu_title}

ArcGIS Experience Builder Menu Project

## Overview
This project provides a reusable menu interface for ArcGIS Experience Builder applications.

## Configuration
- **Experience ID**: `{experience_id}`
- **Project Name**: `{project_name}`
- **Menu Title**: `{menu_title}`

## Files
- `index.html` - Main menu interface
- `menu.json` - Menu configuration data
- `project_config.py` - Customizable menu structure
- `config.py` - Global configuration loader
- `deploy.py` - Deployment utilities
- `generate_menu.py` - Menu generation script

## Quick Start

1. **Customize the menu**:
   ```bash
   # Edit project_config.py to define your menu structure
   vim project_config.py
   ```

2. **Generate menu.json**:
   ```bash
   python generate_menu.py
   ```

3. **Test locally**:
   Open `index.html` in a browser to test your menu

4. **Deploy**:
   ```bash
   python deploy.py "Your commit message"
   ```

## Menu Structure
Edit `project_config.py` to customize:
- Categories and their colors
- Menu items and page IDs
- Search terms for filtering

## Global Configuration
Uses shared configuration from `~/.config/arcgis/.env`:
- ArcGIS OAuth credentials
- PythonAnywhere deployment settings
- API keys and tokens

## Deployment
- **GitHub**: Automatic git commit and push
- **PythonAnywhere**: API deployment for live menu
- **Validation**: Menu structure validation before deployment

## Troubleshooting
- Ensure global config exists: `~/.config/arcgis/.env`
- Check ArcGIS Experience Builder page IDs
- Verify PythonAnywhere API credentials

## Support
Generated by ArcGIS Experience Builder Menu Generator
'''
        
        with open(project_path / 'README.md', 'w') as f:
            f.write(readme_content)
        
        print("📄 Created: README.md (project documentation)")

def main():
    """Interactive project creation"""
    print("🚀 ArcGIS Experience Builder Menu Project Generator")
    print("=" * 60)
    
    # Get project details
    project_name = input("📝 Project name (e.g., 'Regional_Operations'): ").strip()
    if not project_name:
        print("❌ Project name is required")
        return
    
    project_path = input(f"📁 Project directory (default: current directory): ").strip()
    if not project_path:
        project_path = "."
    
    experience_id = input("🌐 ArcGIS Experience Builder ID: ").strip()
    if not experience_id:
        print("❌ Experience Builder ID is required")
        return
    
    menu_title = input(f"📋 Menu title (default: '{project_name.replace('_', ' ').title()}'): ").strip()
    
    subdomain = input(f"🌐 PythonAnywhere subdomain (default: '{project_name.lower()}-jfranzen'): ").strip()
    
    # Create project
    generator = ProjectGenerator()
    generator.create_project(
        project_name=project_name,
        project_path=project_path,
        experience_id=experience_id,
        menu_title=menu_title or None,
        pythonanywhere_subdomain=subdomain or None
    )

if __name__ == "__main__":
    main()
'''