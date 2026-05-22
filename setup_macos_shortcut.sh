#!/bin/bash

# Gnom-Hub macOS App Builder & Dock Shortcut Creator
# This script compiles the custom high-quality PNG icon into a macOS icon (.icns)
# and builds a Gnom-Hub.app bundle on the Desktop.

set -e

WORKSPACE_DIR="/Users/landjunge/Documents/AG-Flega"
ICON_PNG="/Users/landjunge/.gemini/antigravity/brain/6cdd39c7-b271-4c3b-bfdf-57808f675ba5/gnom_hub_ultra_simple_1779420109688.png"
DESKTOP_DIR="/Users/landjunge/Desktop"
APP_NAME="Gnom-Hub"
APP_DIR="${DESKTOP_DIR}/${APP_NAME}.app"

echo "=== Building Gnom-Hub macOS Application Bundle ==="

# 1. Create App Bundle Directory Structure
echo "Creating directory structure..."
mkdir -p "${APP_DIR}/Contents/MacOS"
mkdir -p "${APP_DIR}/Contents/Resources"

# 2. Compile PNG Icon into macOS .icns file
if [ -f "$ICON_PNG" ]; then
    echo "Compiling high-resolution icon set..."
    ICONSET_DIR="/tmp/GnomIcon.iconset"
    mkdir -p "$ICONSET_DIR"
    
    # Generate all sizes for the Apple ICNS spec
    sips -s format png -z 16 16     "$ICON_PNG" --out "${ICONSET_DIR}/icon_16x16.png" > /dev/null 2>&1
    sips -s format png -z 32 32     "$ICON_PNG" --out "${ICONSET_DIR}/icon_16x16@2x.png" > /dev/null 2>&1
    sips -s format png -z 32 32     "$ICON_PNG" --out "${ICONSET_DIR}/icon_32x32.png" > /dev/null 2>&1
    sips -s format png -z 64 64     "$ICON_PNG" --out "${ICONSET_DIR}/icon_32x32@2x.png" > /dev/null 2>&1
    sips -s format png -z 128 128   "$ICON_PNG" --out "${ICONSET_DIR}/icon_128x128.png" > /dev/null 2>&1
    sips -s format png -z 256 256   "$ICON_PNG" --out "${ICONSET_DIR}/icon_128x128@2x.png" > /dev/null 2>&1
    sips -s format png -z 256 256   "$ICON_PNG" --out "${ICONSET_DIR}/icon_256x256.png" > /dev/null 2>&1
    sips -s format png -z 512 512   "$ICON_PNG" --out "${ICONSET_DIR}/icon_256x256@2x.png" > /dev/null 2>&1
    sips -s format png -z 512 512   "$ICON_PNG" --out "${ICONSET_DIR}/icon_512x512.png" > /dev/null 2>&1
    sips -s format png -z 1024 1024 "$ICON_PNG" --out "${ICONSET_DIR}/icon_512x512@2x.png" > /dev/null 2>&1

    iconutil -c icns "$ICONSET_DIR" -o "${APP_DIR}/Contents/Resources/GnomIcon.icns"
    rm -rf "$ICONSET_DIR"
    echo "Icon compiled successfully!"
else
    echo "Warning: Custom PNG icon not found. App bundle will use default fallback icon."
fi

# 3. Create Info.plist config
echo "Generating Info.plist..."
cat << 'EOF' > "${APP_DIR}/Contents/Info.plist"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Gnom-Hub</string>
    <key>CFBundleIconFile</key>
    <string>GnomIcon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.gnomhub.launcher</string>
    <key>CFBundleName</key>
    <string>Gnom-Hub</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.10.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOF

# 4. Create macOS Executable Runner script
echo "Generating launcher script..."
cat << EOF > "${APP_DIR}/Contents/MacOS/Gnom-Hub"
#!/bin/bash
WORKSPACE="${WORKSPACE_DIR}"
cd "\$WORKSPACE"

# Check if Gnom-Hub server is already running on port 3002
if ! lsof -Pi :3002 -sTCP:LISTEN -t >/dev/null ; then
    # Start Gnom-Hub server in a new Terminal window
    osascript -e "tell application \"Terminal\" to do script \"cd '\$WORKSPACE' && .venv/bin/python3 -m gnom_hub\""
    sleep 1.5
fi

# Open Gnom-Hub dashboard in the default browser
open "http://127.0.0.1:3002"
EOF

chmod +x "${APP_DIR}/Contents/MacOS/Gnom-Hub"

# 5. Refresh Finder to load app bundle icon correctly
touch "${APP_DIR}"

echo "=== Gnom-Hub app successfully built on your Desktop! ==="
echo "You can drag 'Gnom-Hub.app' from your Desktop straight into your macOS Dock."
