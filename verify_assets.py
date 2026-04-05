#!/usr/bin/env python3
"""
Asset Verification Script
Checks if all required assets are present and accessible
Run this if you get "logo not found" or other asset errors
"""

import os
import sys

# Get the base directory (same logic as in the application)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Define all required assets
REQUIRED_ASSETS = {
    "keymorpher-ai-logo.png": {
        "type": "Image",
        "required": True,
        "description": "Main logo for splash screen"
    },
    "keyboard-symbol.png": {
        "type": "Image",
        "required": True,
        "description": "Keyboard icon for header"
    },
    "name.png": {
        "type": "Image",
        "required": True,
        "description": "Branding text image"
    },
    "intro.wav": {
        "type": "Audio",
        "required": False,
        "description": "Startup/intro sound"
    },
    "click.wav": {
        "type": "Audio",
        "required": False,
        "description": "Key click sound effect"
    }
}

def verify_assets():
    """Check all assets and report status"""
    print("=" * 70)
    print("KEYMORPHER AI - ASSET VERIFICATION")
    print("=" * 70)
    print(f"\nAssets Directory: {ASSETS_DIR}\n")
    
    missing_critical = False
    missing_optional = []
    found_count = 0
    
    for asset_name, info in REQUIRED_ASSETS.items():
        asset_path = os.path.join(ASSETS_DIR, asset_name)
        exists = os.path.exists(asset_path)
        
        status = "[OK]" if exists else "[MISSING]"
        required_label = "[REQUIRED]" if info["required"] else "[OPTIONAL]"
        
        print(f"{status} {required_label} {asset_name}")
        print(f"      Type: {info['type']}")
        print(f"      Description: {info['description']}")
        
        if exists:
            file_size = os.path.getsize(asset_path)
            print(f"      Size: {file_size:,} bytes")
            found_count += 1
        else:
            print(f"      Location: {asset_path}")
            if info["required"]:
                missing_critical = True
            else:
                missing_optional.append(asset_name)
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Found: {found_count}/{len(REQUIRED_ASSETS)} assets")
    
    if missing_critical:
        print("\n[ERROR] CRITICAL: Missing required assets!")
        print("\nFix: Try these steps:")
        print("  1. Make sure you cloned the full repository:")
        print("     git clone https://github.com/Punerihardik11/Keymorpher-AI.git")
        print("  2. Verify the assets folder exists:")
        print(f"     ls {ASSETS_DIR}")
        print("  3. If still missing, pull the latest changes:")
        print("     git pull origin master")
        print("  4. Check file sizes (PNG should be ~100KB, logo ~1MB):")
        print(f"     ls -lh {ASSETS_DIR}")
        return False
    
    if missing_optional:
        print(f"\n[WARNING] Missing optional assets: {', '.join(missing_optional)}")
        print("The application will work but without sound effects.")
        return True
    
    print("\n[OK] All assets verified successfully!")
    print("The application should run without problems.")
    return True

if __name__ == "__main__":
    success = verify_assets()
    sys.exit(0 if success else 1)
