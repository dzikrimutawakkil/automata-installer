import urllib.request
import subprocess
import os
import shutil
import sys
import winreg

def install_nodejs():
    node_url = "https://nodejs.org/dist/v18.17.1/node-v18.17.1-x64.msi"
    installer_path = os.path.join(os.getenv("TEMP"), "node_installer.msi")
    
    print("Downloading Node.js installer...")
    urllib.request.urlretrieve(node_url, installer_path)

    print("Running Node.js installer...")
    subprocess.check_call(["msiexec", "/i", installer_path, "/quiet", "/norestart"])

    # Wait a bit for installer to finish
    import time
    time.sleep(5)

    # Check if node is now in path
    if shutil.which("node") is None:
        print("Node is installed, but not in PATH. Attempting to update environment variable...")

        node_path = r"C:\Program Files\nodejs"
        if os.path.exists(os.path.join(node_path, "node.exe")):
            # Add to current session
            os.environ["PATH"] += os.pathsep + node_path

            # Add to user PATH permanently
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Environment", 0, winreg.KEY_SET_VALUE) as key:
                current_path, _ = winreg.QueryValueEx(key, "Path")
                if node_path not in current_path:
                    new_path = current_path + os.pathsep + node_path
                    winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                    print("Node.js path added to user environment variables.")
        else:
            print("Node.js installed, but executable not found. Please check installation.")
    else:
        print("Node.js successfully installed and available in PATH.")
