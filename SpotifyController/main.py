import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

def main() -> None:
    print(os.environ.get("SPOTIPY_REDIRECT_URI"))
    print(os.environ.get("SPOTIPY_CLIENT_ID"))
    print(os.environ.get("SPOTIPY_CLIENT_SECRET"))

if __name__ == '__main__':
    main()