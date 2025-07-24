import os

# Function to check if a file is suspicious
def is_suspicious(file_path):
    suspicious_ext = [".exe", ".bat", ".scr", ".dll"]
    filename = os.path.basename(file_path).lower()
    return (
        any(filename.endswith(ext) for ext in suspicious_ext) or
        os.path.getsize(file_path) > 5 * 1024 * 1024  # >5MB
    )

# Generator to yield file analysis results
def analyze_disk_image(path):
    all_files = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    total = len(all_files)

    for idx, file_path in enumerate(all_files):
        try:
            size_kb = os.path.getsize(file_path) // 1024
            name = os.path.basename(file_path)
            flagged = is_suspicious(file_path)
            percent = round(((idx + 1) / total) * 100, 2)

            yield {
                'name': name,
                'size': size_kb,
                'flagged': flagged,
                'percent': percent
            }

        except Exception:
            yield {
                'name': "[Error reading file]",
                'size': 0,
                'flagged': True,
                'percent': round(((idx + 1) / total) * 100, 2)
            }
