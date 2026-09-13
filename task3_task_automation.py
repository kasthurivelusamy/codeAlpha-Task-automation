"""
CodeAlpha - Python Programming Internship
TASK 3: Task Automation with Python Scripts

This script offers a menu with 3 automation options:
  1. Move all .jpg files from a folder to a new folder.
  2. Extract all email addresses from a .txt file and save them to another file.
  3. Scrape the title of a fixed webpage and save it.

Key Concepts Used: os, shutil, re, requests, file handling.
"""

import os
import re
import shutil

try:
    import requests
except ImportError:
    requests = None  # Only needed for option 3


def move_jpg_files():
    """Move all .jpg files from a source folder to a destination folder."""
    src = input("Enter the SOURCE folder path (contains .jpg files): ").strip()
    dst = input("Enter the DESTINATION folder path: ").strip()

    if not os.path.isdir(src):
        print(f"⚠ Source folder '{src}' does not exist.")
        return

    os.makedirs(dst, exist_ok=True)

    moved_count = 0
    for filename in os.listdir(src):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            src_path = os.path.join(src, filename)
            dst_path = os.path.join(dst, filename)
            shutil.move(src_path, dst_path)
            print(f"  Moved: {filename}")
            moved_count += 1

    if moved_count == 0:
        print("No .jpg files found to move.")
    else:
        print(f"\n✔ Moved {moved_count} .jpg file(s) to '{dst}'.")


def extract_emails():
    """Extract all email addresses from a .txt file and save them to another file."""
    src_file = input("Enter the path of the .txt file to scan: ").strip()

    if not os.path.isfile(src_file):
        print(f"⚠ File '{src_file}' does not exist.")
        return

    with open(src_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = sorted(set(re.findall(email_pattern, content)))

    if not emails:
        print("No email addresses found in the file.")
        return

    output_file = input("Enter output filename (default: extracted_emails.txt): ").strip()
    if not output_file:
        output_file = "extracted_emails.txt"

    with open(output_file, "w") as f:
        for email in emails:
            f.write(email + "\n")

    print(f"\n✔ Found {len(emails)} unique email(s). Saved to '{output_file}'.")
    for email in emails:
        print(f"  - {email}")


def scrape_webpage_title():
    """Scrape the <title> of a webpage and save it to a text file."""
    if requests is None:
        print("⚠ The 'requests' library is not installed. Run: pip install requests")
        return

    url = input("Enter the webpage URL (e.g., https://example.com): ").strip()

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠ Failed to fetch the webpage: {e}")
        return

    match = re.search(r"<title>(.*?)</title>", response.text, re.IGNORECASE | re.DOTALL)
    if not match:
        print("⚠ Could not find a <title> tag on this page.")
        return

    title = match.group(1).strip()
    print(f"\nPage title: {title}")

    output_file = "webpage_title.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"URL: {url}\n")
        f.write(f"Title: {title}\n")

    print(f"✔ Saved to '{output_file}'.")


def main():
    while True:
        print("\n" + "=" * 45)
        print("  TASK AUTOMATION MENU")
        print("=" * 45)
        print("1. Move .jpg files to a new folder")
        print("2. Extract email addresses from a .txt file")
        print("3. Scrape a webpage's title")
        print("4. Exit")

        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            move_jpg_files()
        elif choice == "2":
            extract_emails()
        elif choice == "3":
            scrape_webpage_title()
        elif choice == "4":
            print("Goodbye 👋")
            break
        else:
            print("⚠ Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
