# /main.py

```python
#!/usr/bin/env python3

from python_modules.images import copy
from python_modules.github import commit
from python_modules.build import update_base_url, build_github, build_cloudflare, build_netlify , build_vercel
from python_modules.path_fix import search_and_replace , replace_text_in_file
from python_modules.frontmatter import process_markdown_files

def main():
    posts_dir = "website/content/posts"
    attachments_dir = "attachments"
    static_images_dir = "website/static/images"
    source_path = "blog_files"
    file_path = "website/hugo.yaml"
    
    try:
        copy(posts_dir, attachments_dir, static_images_dir, source_path)
    except Exception as e:
        print(f"Fatal error: {e}")
    process_markdown_files(posts_dir)
    print("Markdown files processed and images copied successfully.")
    replace_dir = r"website_github_public"
    update_base_url(file_path, "https://onslaught2342.github.io/blog/")
    build_github()
    search_and_replace(replace_dir, "/images", "/blog/images")
    update_base_url(file_path, "https://blog-onslaught.pages.dev")
    build_cloudflare()
    update_base_url(file_path, "https://blog-onslaught.vercel.app")
    build_vercel()
    update_base_url(file_path, "https://blog-onslaught.netlify.app")
    build_netlify()
    
    commit()
if __name__ == "__main__":
    main()
```
# /python_modules/build.py
```python
import os
import re
import os
import shutil
def build_github():
    try:
        shutil.rmtree(r'website_github_public')
    except Exception as e:
        print("directory doesnot exist creating new one")
    os.system(" hugo -s website -d ../website_github_public -F")

def build_vercel():
    try:
        shutil.rmtree(r'website_vercel_public')
    except Exception as e:
        print("directory doesnot exist creating new one")
    os.system(" hugo -s website -d ../website_vercel_public -F")

def build_netlify():
    try:
        shutil.rmtree(r'website_netlify_public')
    except Exception as e:
        print("directory doesnot exist creating new one")
    os.system(" hugo -s website -d ../website_netlify_public -F")

def build_cloudflare():
    try:
        shutil.rmtree(r'website_cloudflare_public')
    except Exception as e:
        print("directory doesnot exist creating new one")
    
    os.system(" hugo -s website -d ../website_cloudflare_public -F")

# def build_infinity_free():
#     os.system("")

def update_base_url(file_path, new_url):
    with open(file_path, "r") as file:
        content = file.read()
    updated_content = re.sub(r'baseURL:\s*".*?"', f'baseURL: "{new_url}"', content)
    with open(file_path, "w") as file:
        file.write(updated_content)

```
# /python_modules/frontmatter.py
``` python
import os
import datetime
import random

posts_dir = "website/content/posts"
posts_dir = r"blog_files"

def generate_front_matter(file_name):
    try:
        # Extract date from filename (DD-MM-YYYY.md)
        parts = file_name.split('-')
        if len(parts) != 3:
            print(f"Skipping {file_name}: Invalid filename format.")
            return None

        day, month, year_ext = parts
        year = year_ext.split('.')[0]  # Remove ".md" extension
        
        post_date = datetime.date(int(year), int(month), int(day))
        current_date = datetime.date.today()
        
        if post_date == current_date:
            post_time = datetime.datetime.now().time()  # Use current time
        else:
            random_hour = random.randint(8, 22)  # Random hour between 8 AM and 10 PM
            random_minute = random.randint(0, 59)  # Random minute
            post_time = datetime.time(random_hour, random_minute, 0)
        
        post_datetime = datetime.datetime.combine(post_date, post_time).isoformat() + "Z"
        
        # Generate front matter
        front_matter = f"""---
title: "Blog Post {day}-{month}-{year}"
date: {post_datetime}
draft: false
tags: []
---
"""
        return front_matter
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        return None

def process_markdown_files(post_dir):
    for file_name in os.listdir(post_dir):
        if file_name.endswith(".md"):
            file_path = os.path.join(post_dir, file_name)

            with open(file_path, "r+", encoding="utf-8") as f:
                content = f.read()
                
                # Check if front matter already exists
                if content.startswith("---"):
                    print(f"Skipping {file_name}: Front matter already exists.")
                    continue
                
                front_matter = generate_front_matter(file_name)
                if front_matter:
                    # Add front matter to the file
                    f.seek(0)
                    f.write(front_matter + "\n" + content)
                    print(f"Updated {file_name} with front matter.")

# Run the script
if __name__ == "__main__":
    process_markdown_files(posts_dir)

```
# /python_modules/github.py
``` python
import subprocess

def commit():
    """Commits changes to the Git repository with error handling."""
    try:
        output = subprocess.run(["git", "add", "."], check=True)
        output = subprocess.run(["git", "commit", "-m", "Automated blog update"])
        output = subprocess.run(["git", "push" , "origin", "main"])
        output = "work done"

        print("Changes committed and pushed successfully.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}. Git command failed.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return output

if __name__ == "__main__":
    commit()
```
# /python_modules/images.py
``` python
import os
import re
import shutil
import subprocess

def copy(posts_dir, attachments_dir, static_images_dir, source_path):
    """Copies files using robocopy with error handling."""
    command = rf'robocopy "{source_path}" "{posts_dir}" /mir'
    result = subprocess.run(command, shell=True, check=False)

    if result.returncode >= 8:
        print("Warning: Robocopy encountered issues during execution.")

    # Process markdown files
    for filename in os.listdir(posts_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(posts_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()

                # Convert [[image.png]] to ![image.png](/images/image.png) properly
                images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
                for image in images:
                    markdown_image = f"![{image}](/images/{image.replace(' ', '%20')})"
                    content = content.replace(f"[[{image}]]", markdown_image)

                    image_source = os.path.join(attachments_dir, image)
                    image_dest = os.path.join(static_images_dir, image)

                    if os.path.exists(image_source):
                        shutil.copy(image_source, image_dest)
                        print(f"Copied image: {image_source} -> {image_dest}")
                    else:
                        print(f"Missing image: {image_source}")

                # Remove accidental "!image.png" cases (fix your issue)
                content = re.sub(r'!\s*(!\[[^\]]*\]\([^\)]+\))', r'\1', content)

                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(content)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    print("Markdown files processed and images copied successfully.")

    # Remove {} from markdown image references
    for root, _, files in os.walk(posts_dir):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                try:
                    with open(md_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    updated_content = re.sub(r'\{([^}]*)\}', r'\1', content)
                    if content != updated_content:
                        with open(md_path, "w", encoding="utf-8") as f:
                            f.write(updated_content)
                        print(f"Updated: {md_path}")
                except Exception as e:
                    print(f"Error updating {md_path}: {e}")

    # Rename image files and delete old ones
    for file in os.listdir(static_images_dir):
        old_path = os.path.join(static_images_dir, file)
        if os.path.isfile(old_path) and "{" in file and "}" in file:
            new_name = re.sub(r'[{}]', '', file)
            new_path = os.path.join(static_images_dir, new_name)

            try:
                if not os.path.exists(new_path):  # Check before renaming
                    os.rename(old_path, new_path)
                    print(f"Renamed: {file} -> {new_name}")
                else:
                    print(f"Skipping rename: {new_name} already exists.")

                # Delete the old file if renaming was successful
                if os.path.exists(old_path):
                    os.remove(old_path)
                    print(f"Deleted old file: {old_path}")
            except Exception as e:
                print(f"Error renaming {file}: {e}")

if __name__ == "__main__":
    try:
        copy("posts", "attachments", "static/images", "source")
    except Exception as e:
        print(f"Fatal error: {e}")

```
# /python_modules/path_fix.py
``` python
import os

def replace_text_in_file(file_path, search_text, replace_text):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Ensure we don't replace if already correctly formatted
        updated_content = content.replace(search_text, replace_text)
        updated_content = updated_content.replace("/blog/blog/images", "/blog/images")
        
        if content != updated_content:  # Only write if there are changes
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"Updated: {file_path}")
    except Exception as e:
        print(f"Skipping {file_path}: {e}")

def search_and_replace(directory, search_text, replace_text):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            replace_text_in_file(file_path, search_text, replace_text)

if __name__ == "__main__":
    directory = r"website_github_public"
    search_and_replace(directory, "/images", "/blog/images")

```