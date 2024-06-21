import os


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        # Skip .git directory
        dirs[:] = [d for d in dirs if d != '.git']

        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


if __name__ == "__main__":
    # Get the directory where main.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    list_files(current_dir)
