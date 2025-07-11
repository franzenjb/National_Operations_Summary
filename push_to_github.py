#!/usr/bin/env python3
"""
Simple script to push changes to GitHub
"""
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and report the result"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} completed")
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    print("🚀 Pushing changes to GitHub")
    print("=" * 40)
    
    # Check git status
    print("📋 Checking git status...")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if not result.stdout.strip():
            print("✅ No changes to commit")
            return
        else:
            print(f"📝 Changes detected:\n{result.stdout}")
    except subprocess.CalledProcessError:
        print("❌ Failed to check git status")
        return
    
    # Add all changes
    if not run_command(['git', 'add', '.'], "Adding all changes"):
        return
    
    # Commit changes
    commit_message = "Update National Operations Summary configuration"
    if not run_command(['git', 'commit', '-m', commit_message], "Committing changes"):
        return
    
    # Push to GitHub
    if not run_command(['git', 'push'], "Pushing to GitHub"):
        return
    
    print("=" * 40)
    print("🎉 Successfully pushed changes to GitHub!")

if __name__ == "__main__":
    main() 