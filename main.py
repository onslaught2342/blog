import os
import subprocess
import re
import shutil

def copy_files(src_path: str, dest_path: str):
    command = r"""robocopy "C:\Users\abdul\Documents\vscode\github\blog\blog_files" "C:\Users\abdul\Documents\vscode\github\blog\website\content\posts" /mir"""
    subprocess.run(command, shell=True, check=True)

def process_markdown_files(posts_dir: str, attachments_dir: str, static_images_dir: str):
    """Processes markdown files, replacing image links and copying images."""
    if not os.path.exists(posts_dir):
        print(f"Error: Posts directory does not exist - {posts_dir}")
        return

    for filename in os.listdir(posts_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(posts_dir, filename)
            
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
            
            for image in images:
                markdown_image = f'![Image Description](/images/{image.replace(" ", "%20")})'
                content = content.replace(f"[[{image}]]", markdown_image)
                
                image_source = os.path.join(attachments_dir, image)
                if os.path.exists(image_source):
                    shutil.copy(image_source, static_images_dir)
                else:
                    print(f"Warning: Image not found - {image_source}")
            
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)

def commit():
    """Commits changes to the Git repository."""
    command = "git add."
    subprocess.run(command, shell=True, check=True)
    
    command = "git commit -m 'Automated blog update'"
    subprocess.run(command, shell=True, check=True)
    
    command = "git push origin master"
    subprocess.run(command, shell=True, check=True)
def main():
    posts_dir = r"C:\Users\abdul\Documents\vscode\github\blog\website\content\posts"
    attachments_dir = r"C:\Users\abdul\Documents\vscode\github\blog\attachments"
    static_images_dir = r"C:\Users\abdul\Documents\vscode\github\blog\website\static\images"
    source_path = r"C:\Users\abdul\Documents\vscode\github\blog\blog_files"
    
    copy_files(source_path, posts_dir)  # Ensure correct paths are passed
    process_markdown_files(posts_dir, attachments_dir, static_images_dir)
    print("Markdown files processed and images copied successfully.")

 #   commit()

if __name__ == "__main__":
    main()
