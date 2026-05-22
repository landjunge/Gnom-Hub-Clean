#!/usr/bin/env python3
import ftplib, os
FTP_HOST, FTP_USER, FTP_PASS = "185.243.11.43", "sysuser_a", "5Rdv4uH6~Owlqn~k"
FTP_DIR = "netzwerkpunkt.de/httpdocs"
SCRATCH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../gnom_workspace/default"))
FILES = ["index.html", "gnom_landing.html", "gnom_hub.html", "gnom_hub_v2.html", "gnom_hub_landing.html", "charaktere.md", "README.md", "style.css"]

def main():
    print("=== 🛠️ Restoring netzwerkpunkt.de files ===")
    try:
        print(f"🔌 Connecting to {FTP_HOST}...")
        with ftplib.FTP(FTP_HOST, timeout=30) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            ftp.cwd(FTP_DIR)
            for fn in FILES:
                local_path = os.path.join(SCRATCH_DIR, fn)
                if not os.path.isfile(local_path):
                    print(f"❌ Missing file: {local_path}")
                    continue
                with open(local_path, "rb") as f:
                    ftp.storbinary(f"STOR {fn}", f)
                print(f"  ✅ {fn} restored")
        print("\n🎉 **RESTORATION COMPLETE!**")
    except Exception as e:
        print(f"\n❌ Error during restoration: {e}")

if __name__ == "__main__":
    main()
