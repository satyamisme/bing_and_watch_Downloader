# 16.02.24

# Class
from Src.Util.console import console
from Src.Util.util import async_run_executable, read_json, save_json, get_final_redirect_url, get_site_name
from Src.Lib.FFmpeg.my_m3u8 import download_m3u8, download_subtitle

# Import
import os, sys

# Variable
DONWLOAD_SUB = True
magic_exe_path = os.path.abspath(os.path.join("Src", "Lib", "Magic", "magic.exe"))
json_file_path = os.path.join("Src", "Lib", "Magic", "config.json")

# [ func ]
def download_film(film):
    """Get redirect url and download m3u8 playlist"""

    # Read json
    json_data = read_json(json_file_path)
    url = f"https://{get_site_name()}/{film.get('url')}/"
    redirect_url = get_final_redirect_url(url)

    # Change and save url with removing last "/"
    json_data['url'] = redirect_url.rstrip('/')
    save_json(json_data, json_file_path)

    # Run decryption script
    async_run_executable(path=magic_exe_path, log=False)

    # Read new json
    json_data = read_json(json_file_path)
    url_playlist = json_data.get('m3u8')
    arr_tracks = json_data.get('track')

    if url_playlist == "" or url_playlist == None:
        console.print("Cant get m3u8 url")
        sys.exit(0)

    # Download vtt only of english
    if DONWLOAD_SUB:
        if len(arr_tracks) > 0:
            for track in arr_tracks:
                english_sub_track = track.get("file")
                download_subtitle(english_sub_track, f"{film.get('id')}_{track.get('label').replace(' ', '_')}")
        else:
            console.print("[red]Cant find subtitle")


    out_path = os.path.join("videos", f"{film.get('name')}_{film.get('id')}.mp4")
    download_m3u8(m3u8_playlist=url_playlist, output_filename=out_path)
