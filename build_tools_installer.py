import os
import subprocess

def install_android_components():
    sdk_root = "C:\\Android\\sdk"
    tools_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin")
    sdkmanager = os.path.join(tools_path, "sdkmanager.bat")

    if not os.path.exists(sdkmanager):
        print("sdkmanager.bat not found. Install SDK first.")
        return

    env = os.environ.copy()
    env["ANDROID_SDK_ROOT"] = sdk_root

    components = [
        "platform-tools",
        "platforms;android-33",
        "build-tools;34.0.0"
    ]

    for component in components:
        print(f"Installing {component}...")
        subprocess.run([sdkmanager, component], env=env)

    print("All requested SDK components installed.")

# install_android_components()
