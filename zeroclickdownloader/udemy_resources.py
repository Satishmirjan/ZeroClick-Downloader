import os
import re
import sys
import requests
from urllib.parse import urlparse, parse_qs, unquote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36"
}

DOWNLOAD_FOLDER = "zeroclickdownloader"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Match Udemy CDN and S3 file URLs
CDN_URL_RE = re.compile(
    r"https://[^\s'\"<>]*(?:udemycdn\.com|att-c\.udemycdn\.com|amazonaws\.com)[^\s'\"<>]*",
    flags=re.IGNORECASE,
)

# File types we allow
FILE_EXT_RE = re.compile(
    r".*\.(zip|pdf|txt|csv|xml|json|vtt|srt)$",
    flags=re.IGNORECASE
)


def extract_filename(url):
    """Extract filename from response-content-disposition."""
    try:
        qs = parse_qs(urlparse(url).query)
        if "response-content-disposition" in qs:
            disp = unquote(qs["response-content-disposition"][0])
            if "filename=" in disp:
                return disp.split("filename=")[-1].strip('" ')
        return os.path.basename(urlparse(url).path)
    except:
        return "file"


def save_file(url):
    filename = extract_filename(url)
    filename = filename.replace("/", "_")
    path = os.path.join(DOWNLOAD_FOLDER, filename)

    print(f"\nDownloading -> {filename}")

    try:
        r = requests.get(url, headers=HEADERS, stream=True)
        if r.status_code not in (200, 206):
            print(f"❌ Failed ({r.status_code}) — {url}")
            return

        with open(path, "wb") as f:
            for chunk in r.iter_content(1024 * 64):
                if chunk:
                    f.write(chunk)

        print(f"✔ Saved: {path}")

    except Exception as e:
        print("❌ Error downloading:", e)


def main():
    user_in = input("Enter Udemy course URL, direct file URL, or path to urls.txt: ").strip()

    if not user_in:
        print("No input provided.")
        sys.exit()

    # If it's a file list
    if os.path.exists(user_in):
        print(f"Reading from file: {user_in}")
        with open(user_in, "r") as f:
            urls = [x.strip() for x in f.readlines() if x.strip()]
        print(f"Found {len(urls)} URLs in file.")
        for u in urls:
            save_file(u)
        return

    # Normalize URL
    if not user_in.startswith("http"):
        user_in = "https://" + user_in

    # If the input is a direct file URL
    if any(ext in user_in.lower() for ext in [".zip", ".pdf", ".txt", ".vtt", ".srt", ".csv"]) or \
       "udemycdn.com" in user_in or "amazonaws.com" in user_in:

        save_file(user_in)
        return

    # Otherwise treat as course page
    print("\nFetching course page...")
    html = requests.get(user_in, headers=HEADERS).text

    found = re.findall(CDN_URL_RE, html)
    found = [u for u in found if FILE_EXT_RE.match(u)]
    found = list(dict.fromkeys(found))

    print(f"Found {len(found)} downloadable resources.")

    for url in found:
        save_file(url)


if __name__ == "__main__":
    main()
