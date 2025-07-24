import eel
import time
import os

eel.init('web')  # folder where your HTML is

@eel.expose
def start_basic_scan(drive_path):
    print("Scan started for", drive_path)
    result = {
        "files": [],
        "progress": 0,
        "log": []
    }

    try:
        files = os.listdir(drive_path)
        total = len(files)

        for idx, file in enumerate(files):
            time.sleep(0.1)

            # Make full path
            full_path = os.path.join(drive_path, file)

            # Get size in KB
            try:
                size_kb = os.path.getsize(full_path) // 1024
            except:
                size_kb = 0

            # Flag condition (example: suspicious if .exe or size > 1024 KB)
            flagged = file.lower().endswith(".exe") or size_kb > 1024

            result["files"].append({
                "name": file,
                "size": size_kb,
                "flagged": flagged
            })

            result["progress"] = (idx + 1) / total * 100
            result["log"].append(f"Scanned: {file} ({size_kb} KB) {'[FLAGGED]' if flagged else ''}")

    except Exception as e:
        result["log"].append(f"Error: {str(e)}")

    return result


eel.start("index.html", size=(800, 600))
