# scratch/run_live_diagnose_web.py
import os
import time
from playwright.sync_api import sync_playwright
from PIL import Image

def resize_image(path, max_width=1000):
    img = Image.open(path)
    w_percent = (max_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
    img.save(path, "PNG", optimize=True)
    print(f"📷 Shrunk screenshot: {path} (new size: {max_width}x{h_size})")

def main():
    url = "http://127.0.0.1:3003"
    artifact_dir = "/Users/landjunge/.gemini/antigravity/brain/a1c21428-3ad4-4111-bea2-acd72f1cb3ba"
    os.makedirs(artifact_dir, exist_ok=True)
    
    print("🚀 Starting Playwright to trigger live self-diagnosis test in Gnom-Hub browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        
        try:
            print(f"🔗 Navigating to {url}...")
            page.goto(url)
            time.sleep(2)  # Wait for UI to load
            
            # Make sure we are in the War Room / Chat panel
            print("👉 Entering '@@diagnose' command in chat input...")
            page.fill("#chat-input", "@@diagnose")
            time.sleep(0.5)
            
            print("👉 Clicking Send button...")
            page.click("button:has-text('Send')")
            
            print("⏳ Waiting 15 seconds for agents to run self-diagnosis, output thoughts, and render Showbox warning cards...")
            # We'll poll or just wait a bit. Let's do 15 seconds.
            time.sleep(15)
            
            # Take screenshot of the screen showing agents' thoughts and Showbox warning cards
            screenshot_path = os.path.join(artifact_dir, "live_diagnose_result.png")
            page.screenshot(path=screenshot_path)
            resize_image(screenshot_path)
            
            print(f"✅ Screenshot saved successfully to {screenshot_path}")
            
        except Exception as e:
            print(f"❌ Error during automation: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
