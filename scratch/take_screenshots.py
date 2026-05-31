# scratch/take_screenshots.py — Automatic Gnom-Hub screenshots capturer
import os
import time
from playwright.sync_api import sync_playwright
from PIL import Image

def resize_image(path, max_width=800):
    img = Image.open(path)
    w_percent = (max_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
    img.save(path, "PNG", optimize=True)
    print(f"📷 Shrunk screenshot: {path} (new size: {max_width}x{h_size})")

def main():
    url = "http://127.0.0.1:3003"
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs"))
    os.makedirs(docs_dir, exist_ok=True)
    
    print("🚀 Starting Playwright to capture Gnom-Hub screenshots...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        
        try:
            print(f"🔗 Navigating to {url}...")
            page.goto(url)
            time.sleep(2)  # Allow charts, logs, and layout to render
            
            # 1. War Room / Chat screen
            path_wr = os.path.join(docs_dir, "screenshot_warroom.png")
            page.screenshot(path=path_wr)
            resize_image(path_wr)
            
            # 2. Workspace
            print("👉 Clicking Workspace button...")
            page.click("button:has-text('Workspace')")
            time.sleep(1)
            path_ws = os.path.join(docs_dir, "screenshot_workspace.png")
            page.screenshot(path=path_ws)
            resize_image(path_ws)
            
            # 3. Dashboard
            print("👉 Clicking Dashboard button...")
            page.click("button:has-text('Dashboard')")
            time.sleep(1)
            path_db = os.path.join(docs_dir, "screenshot_dashboard.png")
            page.screenshot(path=path_db)
            resize_image(path_db)
            
            # 4. LLM Configuration (Tab 1: Global)
            print("👉 Clicking LLM button...")
            page.click("button:has-text('LLM')")
            time.sleep(1)
            path_llm_glob = os.path.join(docs_dir, "screenshot_llm_global.png")
            page.screenshot(path=path_llm_glob)
            resize_image(path_llm_glob)
            
            # 5. LLM Configuration (Tab 2: Behavior)
            print("👉 Clicking Agenten-Verhalten tab...")
            page.click("button:has-text('Agenten-Verhalten')")
            time.sleep(1)
            path_llm_beh = os.path.join(docs_dir, "screenshot_llm_behavior.png")
            page.screenshot(path=path_llm_beh)
            resize_image(path_llm_beh)
            
            # 6. Help
            print("👉 Clicking Help button...")
            page.click("button:has-text('Help')")
            time.sleep(1.5)  # Allow iframe loading
            path_help = os.path.join(docs_dir, "screenshot_help.png")
            page.screenshot(path=path_help)
            resize_image(path_help)
            
            print("✅ All screenshots taken successfully!")
            
        except Exception as e:
            print(f"❌ Error during screenshot capture: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
