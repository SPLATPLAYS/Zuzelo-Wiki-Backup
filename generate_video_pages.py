import os
import re
from urllib.parse import unquote

def extract_video_info(html_content):
    # Find all video links and titles using regex
    pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html_content)
    return [(unquote(link), title) for link, title in matches]

def create_video_page(title, date, base_dir):
    # Create sanitized filename
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"{safe_title}.html"
    
    # Create directory structure if needed
    full_path = os.path.join(base_dir, "Videos", "AllVideos", filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Generate HTML content
    html_content = f'''<!--
title: {title}
description: Video details and information
published: true
date: {date}
tags: video
editor: code
-->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <p>Published: {date}</p>
    <!-- Add more content here -->
</body>
</html>'''

    # Write file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return full_path

def main():
    # Read input HTML file
    with open('Videos.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract video information
    videos = extract_video_info(content)
    
    # Create base directory
    base_dir = "wiki_pages"
    
    # Process each video
    for video_url, video_title in videos:
        # Extract date from title if available
        date_match = re.search(r'\(Published: ([^)]+)\)', video_title)
        date = date_match.group(1) if date_match else "Unknown Date"
        
        # Clean up title
        clean_title = video_title.split('(Published:')[0].strip()
        
        # Create page
        filepath = create_video_page(clean_title, date, base_dir)
        print(f"Created: {filepath}")

if __name__ == "__main__":
    main()
