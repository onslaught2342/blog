from python_modules.markdown import copy_files, process_markdown_files
from python_modules.github import commit
from python_modules.build import update_base_url, build_github, build_cloudflare, build_infinity_free


def main():
    posts_dir = "C:/Users/abdul/Documents/vscode/github/blog/website/content/posts"
    attachments_dir = "C:/Users/abdul/Documents/vscode/github/blog/attachments"
    static_images_dir = "C:/Users/abdul/Documents/vscode/github/blog/website/static/images"
    source_path = "C:/Users/abdul/Documents/vscode/github/blog/blog_files"
    file_path = r"C:\Users\abdul\Documents\vscode\github\blog\website\hugo.yaml"
    
    copy_files(source_path, posts_dir)  
    process_markdown_files(posts_dir, attachments_dir, static_images_dir)
    print("Markdown files processed and images copied successfully.")
    
    links = ["onslaught2342.github.io/blog", "onslaught2342.pages.dev", "localhost:8080"]
    
    for link in links:
        update_base_url(file_path, link)
        print(f"Base URL updated for {link}")
        
        if link == "onslaught2342.github.io/blog":
            print("Building static files for GitHub...")
            build_github()
        
        elif link == "onslaught2342.pages.dev":
            print("Building static files for Cloudflare Pages...")
            build_cloudflare()
        
        elif link == "localhost:8080":
            print("Building static files for Infinity Free...")
            build_infinity_free()
        
        print("Committing changes...")
        commit()
        print("Changes committed successfully.")
        print("----------------------------------")


if __name__ == "__main__":
    main()

