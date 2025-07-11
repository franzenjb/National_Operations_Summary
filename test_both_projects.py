#!/usr/bin/env python3
"""
Test script to verify both National Operations Summary and Florida Regional Operations Summary setups
"""
import json
import os
import subprocess
import sys

def test_project(project_name, project_path):
    """Test a specific project"""
    print(f"\n🔍 Testing {project_name}")
    print("=" * 50)
    
    # Change to project directory
    if not os.path.exists(project_path):
        print(f"❌ Project directory not found: {project_path}")
        return False
    
    os.chdir(project_path)
    
    # Check required files
    required_files = ['index.html', 'menu.json', 'editor.html']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files exist")
    
    # Test menu.json validity
    try:
        with open('menu.json', 'r') as f:
            data = json.load(f)
        print(f"✅ menu.json is valid JSON with {len(data)} categories")
    except json.JSONDecodeError as e:
        print(f"❌ menu.json is invalid JSON: {e}")
        return False
    
    # Test HTML files
    for html_file in ['index.html', 'editor.html']:
        try:
            with open(html_file, 'r') as f:
                content = f.read()
            if len(content) > 100:  # Basic check
                print(f"✅ {html_file} appears to be valid")
            else:
                print(f"❌ {html_file} appears to be empty or corrupted")
                return False
        except Exception as e:
            print(f"❌ Error reading {html_file}: {e}")
            return False
    
    return True

def open_project(project_name, project_path):
    """Open a project in the browser"""
    try:
        index_path = os.path.join(project_path, 'index.html')
        abs_path = os.path.abspath(index_path)
        print(f"🌐 Opening {project_name} at {abs_path}")
        subprocess.run(['open', abs_path], check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to open {project_name}")
        return False

def main():
    print("🚀 Testing Both Projects: National Operations Summary & Florida Regional Operations Summary")
    print("=" * 80)
    
    # Project paths
    base_path = "/Users/jefffranzen/Desktop/REPOSITORIES"
    national_path = os.path.join(base_path, "National_Operations_Summary")
    florida_path = os.path.join(base_path, "Florida_Regional_Operations_Summary")
    
    # Test both projects
    national_success = test_project("National Operations Summary", national_path)
    florida_success = test_project("Florida Regional Operations Summary", florida_path)
    
    print("\n" + "=" * 80)
    print("📊 FINAL RESULTS")
    print("=" * 80)
    
    if national_success:
        print("✅ National Operations Summary: WORKING")
    else:
        print("❌ National Operations Summary: FAILED")
    
    if florida_success:
        print("✅ Florida Regional Operations Summary: WORKING")
    else:
        print("❌ Florida Regional Operations Summary: FAILED")
    
    if national_success and florida_success:
        print("\n🎉 Both projects are working correctly!")
        
        # Ask user which to open
        print("\n🌐 Which project would you like to open?")
        print("1. National Operations Summary")
        print("2. Florida Regional Operations Summary")
        print("3. Both")
        print("4. Neither")
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice == "1":
                open_project("National Operations Summary", national_path)
            elif choice == "2":
                open_project("Florida Regional Operations Summary", florida_path)
            elif choice == "3":
                open_project("National Operations Summary", national_path)
                open_project("Florida Regional Operations Summary", florida_path)
            else:
                print("👍 No projects opened")
        except KeyboardInterrupt:
            print("\n👍 No projects opened")
    else:
        print("\n❌ Some projects failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 