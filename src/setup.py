import os
from secret_key import gen_key

def main():
    if os.environ.get("FLASK_SECRET_KEY") is None:
        print(f"Please generate and export your secret key.\n\
            This can be done with the following command:\n\
            export FLASK_SECRET_KEY={gen_key()}")
        exit(1)

    if os.environ.get("FLASK_DEVFOLDER") is None:
        print("Please export a folder path with:\n\
            export FLASK_DEVFOLDER=\"/path/to/folder\"")
        exit(1)