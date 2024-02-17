# 10.02.24

# Class
from Src.Util.console import console, msg
from Src.Util.headers import get_headers
from Src.Util.util import get_site_name
from Src.Api.film import download_film as download_episode

# Import
import requests, sys
from bs4 import BeautifulSoup

# Variable
site_name = get_site_name()


# [ func ]
def get_season_info(title_id):
    """Get list of season available from main id title"""

    console.print("[cyan]Fetch info seasons ...")
    response = requests.get(f"https://{site_name}/ajax/movie/seasons/{title_id}", headers={'user-agent': get_headers()})

    if response.ok:

        soup = BeautifulSoup(response.text, "lxml")

        # Get soup dropdown all item
        result = []
        html_seasons = soup.find_all("a", class_ = "dropdown-item")

        for html_season in html_seasons:
            result.append({'id': html_season.get("data-id")})

        return result
    
    else:
        console.log(f"[red]Cant connect to server seasons, error: {response.status_code}")
        sys.exit(0)

def get_eps_season_info(season_id):
    """Get a list of episode available for an id of a season"""

    console.print("[cyan]Fetch info episodes ...")
    response = requests.get(f"https://{site_name}/ajax/movie/season/episodes/{season_id}", headers={'user-agent': get_headers()})

    if response.ok:

        soup = BeautifulSoup(response.text, "lxml")

        # Get soup button onair item
        result = []
        html_episodes = soup.find_all("a", class_ = "btn-onair")

        for html_ep in html_episodes:
            result.append({
                'id': html_ep.get("data-id"), 
                'name': html_ep.get("title"),
                'url': html_ep.get('href')
            })

        return result
    
    else:
        console.log(f"[red]Cant connect to server episodes, error: {response.status_code}")
        sys.exit(0)

def download_episodes(season_id):
    """Select season and episode index and start download playlist m3u8"""

    print("")
    result_seasons = get_season_info(season_id)
    console.print(f"[green]Season find: [red]{len(result_seasons)}")

    print("")
    index_select_season = int(msg.ask("[green]Select season index ")) -1

    if 0 <= index_select_season <= len(result_seasons):
        select_season_id = result_seasons[index_select_season].get('id')

        result_episodes = get_eps_season_info(select_season_id)

        if len(result_episodes) == 0:
            console.log("[red]Cant find list of seasons")
            sys.exit(0)


        print("")
        for i in range(len(result_episodes)):
            name = result_episodes[i].get('name')
            console.print(f"[cyan]Index: [yellow]{i} [white]=> [purple][ {name} [purple]]")

        print("")
        index_select_episode = msg.ask("[green]Select episode index ")
        index_select_episode = int(index_select_episode)

        if 0 < index_select_episode < len(result_episodes):

            console.print("[cyan]Donwload ep ... \n")
            download_episode(result_episodes[index_select_episode])

        else:
            console.log("[red]Episode out of range")

    else:
        console.log("[red]Season out of range")
