import os, shutil

def removeDir(directory):
    d = os.path.abspath(directory)
    print(f"path to delete: {d}")
    if os.path.exists(d) and os.path.isdir(d):
        print(f"deleting {d}...")
        shutil.rmtree(d, True)
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


if __name__ == "__main__":
    removeDir("public")
    copyDir("static", "public")

