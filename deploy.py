#!/usr/bin/env python3
"""
Enhanced deployment tool for ArcGIS Experience Builder menus
Integrates with GitHub and PythonAnywhere using global configuration
"""
import subprocess
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from config import get_deployment_config, load_global_config

class MenuDeployer:
    """Deploy ArcGIS Experience Builder menus to GitHub and PythonAnywhere"""
    
    def __init__(self):
        self.config = get_deployment_config()
        self.global_config = load_global_config()
        
    def run_command(self, cmd, description):
        """Run a command and report the result"""
        print(f"🔄 {description}...")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if result.stdout:
                print(f"✅ {description} completed")
                print(f"   Output: {result.stdout.strip()}")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed")
            print(f"   Error: {e.stderr.strip()}")
            return False, e.stderr

    def check_git_status(self):
        """Check if there are changes to commit"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def deploy_to_github(self, commit_message=None):
        """Deploy changes to GitHub"""
        print("🚀 Deploying to GitHub")
        print("=" * 40)
        
        # Check git status
        changes = self.check_git_status()
        if not changes:
            print("✅ No changes to commit")
            return True
        else:
            print(f"📝 Changes detected:\n{changes}")
        
        # Add all changes
        success, _ = self.run_command(['git', 'add', '.'], "Adding all changes")
        if not success:
            return False
        
        # Commit changes
        if not commit_message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            commit_message = f"Update ArcGIS Experience Builder menu - {timestamp}"
        
        success, _ = self.run_command(['git', 'commit', '-m', commit_message], "Committing changes")
        if not success:
            return False
        
        # Push to GitHub
        success, _ = self.run_command(['git', 'push'], "Pushing to GitHub")
        return success

    def deploy_to_pythonanywhere(self):
        """Deploy menu.json to PythonAnywhere API"""
        print("🌐 Deploying to PythonAnywhere")
        print("=" * 40)
        
        # Load menu.json
        menu_file = Path('menu.json')
        if not menu_file.exists():
            print("❌ menu.json not found")
            return False
        
        try:
            with open(menu_file, 'r') as f:
                menu_data = json.load(f)
            
            # Send to PythonAnywhere API
            api_url = f"{self.config['menu_api_base_url']}/menu"
            params = {'pw': self.config['menu_api_password']}
            
            response = requests.post(
                api_url,
                params=params,
                json=menu_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.ok:
                print("✅ Successfully deployed to PythonAnywhere")
                result = response.json()
                if 'message' in result:
                    print(f"   Response: {result['message']}")
                return True
            else:
                print(f"❌ PythonAnywhere deployment failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in menu.json: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False

    def backup_current_menu(self):
        """Create a backup of the current menu"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"menu_backup_{timestamp}.json"
            
            if Path('menu.json').exists():
                subprocess.run(['cp', 'menu.json', backup_name], check=True)
                print(f"📋 Backup created: {backup_name}")
                return backup_name
        except Exception as e:
            print(f"⚠️  Backup failed: {e}")
        return None

    def validate_menu(self):
        """Validate menu.json structure"""
        try:
            with open('menu.json', 'r') as f:
                menu_data = json.load(f)
            
            if not isinstance(menu_data, list):
                print("❌ Menu must be a list of categories")
                return False
            
            for i, category in enumerate(menu_data):
                if not isinstance(category, dict):
                    print(f"❌ Category {i} must be a dictionary")
                    return False
                
                required_fields = ['category', 'color', 'links']
                for field in required_fields:
                    if field not in category:
                        print(f"❌ Category {i} missing required field: {field}")
                        return False
                
                if not isinstance(category['links'], list):
                    print(f"❌ Category {i} links must be a list")
                    return False
                
                for j, link in enumerate(category['links']):
                    if not isinstance(link, dict):
                        print(f"❌ Category {i}, link {j} must be a dictionary")
                        return False
                    
                    link_fields = ['label', 'href', 'term']
                    for field in link_fields:
                        if field not in link:
                            print(f"❌ Category {i}, link {j} missing field: {field}")
                            return False
            
            print("✅ Menu validation passed")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return False
        except FileNotFoundError:
            print("❌ menu.json not found")
            return False

    def full_deployment(self, commit_message=None):
        """Run complete deployment workflow"""
        print("🚀 Starting Full Deployment Workflow")
        print("=" * 50)
        
        # Create backup
        self.backup_current_menu()
        
        # Validate menu
        if not self.validate_menu():
            print("❌ Deployment aborted due to validation errors")
            return False
        
        # Deploy to GitHub
        github_success = self.deploy_to_github(commit_message)
        
        # Deploy to PythonAnywhere
        pythonanywhere_success = self.deploy_to_pythonanywhere()
        
        # Summary
        print("=" * 50)
        if github_success and pythonanywhere_success:
            print("🎉 Full deployment completed successfully!")
            print(f"   GitHub: ✅")
            print(f"   PythonAnywhere: ✅")
            print(f"   Menu URL: {self.config['pythonanywhere_domain']}")
            return True
        else:
            print("⚠️  Deployment completed with issues:")
            print(f"   GitHub: {'✅' if github_success else '❌'}")
            print(f"   PythonAnywhere: {'✅' if pythonanywhere_success else '❌'}")
            return False

def main():
    """Main deployment function"""
    if len(sys.argv) > 1:
        commit_message = " ".join(sys.argv[1:])
    else:
        commit_message = None
    
    deployer = MenuDeployer()
    deployer.full_deployment(commit_message)

if __name__ == "__main__":
    main()