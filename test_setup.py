#!/usr/bin/env python3
"""
Test script to verify the National Operations Summary setup
"""
import json
import os
import subprocess
import sys

def test_files_exist():
    """Check that required files exist"""
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
        return True

def test_menu_json():
    """Test that menu.json is valid JSON"""
    try:
        with open('menu.json', 'r') as f:
            data = json.load(f)
        print(f"✅ menu.json is valid JSON with {len(data)} categories")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ menu.json is invalid JSON: {e}")
        return False
    except FileNotFoundError:
        print("❌ menu.json not found")
        return False

def open_index():
    """Open index.html in the default browser"""
    try:
        index_path = os.path.abspath('index.html')
        print(f"🌐 Opening {index_path}")
        subprocess.run(['open', index_path], check=True)
        print("✅ Successfully opened index.html")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to open index.html")
        return False

def main():
    print("🔍 Testing National Operations Summary Setup")
    print("=" * 50)
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if test_files_exist():
        tests_passed += 1
    
    if test_menu_json():
        tests_passed += 1
    
    if open_index():
        tests_passed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your National Operations Summary is ready to use.")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 