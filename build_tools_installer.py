import os
import subprocess

def install_android_components():
    sdk_root = r"C:\Android\sdk"
    jdk_path = r"C:\Program Files\Java\jdk17.0.15_6"
    tools_path = os.path.join(sdk_root, "cmdline-tools", "latest", "bin")
    sdkmanager = os.path.join(tools_path, "sdkmanager.bat")

    if not os.path.exists(sdkmanager):
        print("❌ sdkmanager.bat not found. Please install Android SDK command line tools first.")
        return

    # Refresh environment variables for this process
    os.environ["JAVA_HOME"] = jdk_path
    os.environ["PATH"] = os.path.join(jdk_path, "bin") + os.pathsep + os.environ["PATH"]
    os.environ["ANDROID_SDK_ROOT"] = sdk_root
    os.environ["ANDROID_HOME"] = sdk_root

    env = os.environ.copy()

    components = [
        "build-tools;34.0.0",
        "platforms;android-34"
    ]

    # Accept all licenses
    print("🔄 Accepting SDK licenses...")
    accept = subprocess.run(
        [sdkmanager, "--licenses"],
        env=env,
        input=b'y\n' * 100,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if accept.returncode != 0:
        print("⚠️ Error while accepting licenses:")
        print("STDOUT:", accept.stdout.decode())
        print("STDERR:", accept.stderr.decode())
        return

    # Install components
    for component in components:
        print(f"⬇️ Installing {component} ...")
        result = subprocess.run(
            [sdkmanager, component],
            env=env,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Error installing {component}:")
            print(result.stderr)
        else:
            print(f"✅ {component} installed successfully.")

    print("🎉 All requested SDK components installed.")
