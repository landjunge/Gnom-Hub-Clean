#!/usr/bin/env python3
import ftplib
import os

FTP_HOST = "185.243.11.43"
FTP_USER = "sysuser_a"
FTP_PASS = "5Rdv4uH6~Owlqn~k"
FTP_DIR = "netzwerkpunkt.de/httpdocs"

SCRATCH_DIR = "/Users/landjunge/.gemini/antigravity/brain/906ef630-ac5d-4658-8863-f14655e4bdf0/scratch/gnom_workspace/default"

FILES_TO_UPLOAD = [
    "index.html",
    "gnom_landing.html",
    "gnom_hub.html",
    "gnom_hub_v2.html",
    "gnom_hub_landing.html",
    "charaktere.md",
    "README.md",
    "style.css",
]

def upload_file(ftp, local_path, remote_name):
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_name}", f)
    print(f"  ✅ {remote_name} restored")

def main():
    print("=== 🛠️ Restoring netzwerkpunkt.de files to original state ===")
    try:
        print(f"🔌 Connecting to {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST, timeout=30)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"✅ Logged in as {FTP_USER}")
        
        print(f"📂 Changing directory to {FTP_DIR}...")
        ftp.cwd(FTP_DIR)
        
        print("\n📤 Uploading original files...")
        for filename in FILES_TO_UPLOAD:
            local_path = os.path.join(SCRATCH_DIR, filename)
            if not os.path.isfile(local_path):
                print(f"❌ Missing file in scratch: {local_path}")
                continue
            upload_file(ftp, local_path, filename)
            
        ftp.quit()
        print("\n🎉 **RESTORATION COMPLETE!**")
        print("🌐 https://netzwerkpunkt.de/ is restored to its original state.")
    except Exception as e:
        print(f"\n❌ Error during restoration: {e}")

if __name__ == "__main__":
    main()
