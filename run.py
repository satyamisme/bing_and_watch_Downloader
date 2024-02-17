# 10.02.24

# Class
from Src.Util.message import get_message
from Src.Lib.FFmpeg.installer import check_ffmpeg
from Src.Util.util import clean_json
from Src.Util.os import remove_folder
from Src.Api.search import select_title
from Src.Api.series import download_episodes
from Src.Api.film import download_film
from Src.Upload.update import main_update
from Src.Util.console import console

# Import
import os, time, sys

# Variable
json_file_path = os.path.join("Src", "Lib", "Magic", "config.json")

def initialize():

    if sys.version_info < (3, 11):
        console.log("Install python version > 3.11")
        sys.exit(0)

    get_message()

    remove_folder("tmp")
    clean_json(json_file_path)
    time.sleep(1)

    try:
        main_update()
    except Exception as e:
        console.print(f"[blue]Req github [white]=> [red]Failed: {e} \n")

    check_ffmpeg()
    print("\n")

def main():

    initialize()

    title_select = select_title()

    if len(title_select) > 0:

        if title_select.get('is_movie'):
            console.print("[cyan]Donwload film ... \n")
            download_film(title_select)

        else:
            download_episodes(title_select.get('id'))

    else:
        console.print("[red]Cant find a list of title")

    console.log("[red]End")

if __name__ == "__main__":
    main()
    