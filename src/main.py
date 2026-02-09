import os, shutil, sys, re
from converter import markdown_to_html

def removeDir(directory):
    d = os.path.abspath(directory)
    print(f"path to delete: {d}")
    if os.path.exists(d) and os.path.isdir(d):
        print(f"deleting...")
        shutil.rmtree(d)
        print("deleted")
    else:
        print("path not found or not a directory")

def copyDir(src, dest):
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)
    if os.path.exists(src):
        if os.path.exists(dest):
            print(f"dest '{dest}' already exists")
            return
        else:
            if os.path.isdir(src):
                print(f"creating destination folder '{dest}'")
                os.mkdir(dest)
                for file in os.listdir(src):
                    copyDir(os.path.join(src, file), os.path.join(dest, file))
            else:
                print(f"copying file to '{dest}'")
                shutil.copy(src,dest)
                return
    else:
        print(f"src '{src}' does not exist - aborting")

def extract_title(markdown):
    titles = re.findall(r"(?<!#)# .+", markdown)
    if not titles:
        raise AttributeError("No title found")
    return titles[0][2:]

def generate_page(from_path, template_path, dest_path, basepath):
    from_path = os.path.abspath(from_path)
    template_path = os.path.abspath(template_path)
    dest_path = os.path.abspath(dest_path)
    if not os.path.exists(from_path):
        raise AttributeError(f"from_path {from_path} does not exist")
    if not os.path.exists(template_path):
        raise AttributeError(f"template_path {template_path} does not exist")
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template_html = f.read()

    print("\n\n--------------")
    html = markdown_to_html(markdown)
    title = extract_title(markdown)
    template_html = template_html.replace("{{ Title }}", title)
    template_html = template_html.replace("{{ Content }}", html)
    template_html = template_html.replace('href="/', f'href="{basepath}')
    template_html = template_html.replace('src="/', f'src="{basepath}')
    

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wt") as f:
        f.write(template_html)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    removeDir("doc")
    removeDir("public")
    copyDir("static", "docs")
    for p, folders, files in os.walk("content"):
        for f in files:
            if f.endswith(".md"):
                generate_page(os.path.join(p, f), "template.html",
                              os.path.join(p.replace("content", "docs"), f.replace(".md", ".html")), basepath)

