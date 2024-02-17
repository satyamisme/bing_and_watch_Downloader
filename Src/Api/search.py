# 10.02.24

# Class
from Src.Util.console import console, msg
from Src.Util.headers import get_headers
from Src.Util.util import get_site_name

# Import
import requests, sys
from bs4 import BeautifulSoup


# [ func ]
def search_on_server(title):
    """Make request to server site and get result with name | id | is_movie | url """

    # Note: Add options per andare avanti con le pageine

    console.print("[cyan]Make request to server ...")
    response = requests.get(f"https://{get_site_name()}/ajax/movie/search?keyword={title}", headers={'user-agent': get_headers()})

    if response.ok:

        soup = BeautifulSoup(response.text, "lxml")

        # Get soup of item
        result = []
        html_titles = soup.find_all("div", class_ = "item")

        # Collect all result of req
        for html_title in html_titles:
            title_url = html_title.find("a").get("href")

            if html_title.find("h3") != None:

                result.append({
                    'name': html_title.find("h3").text, 
                    'id': html_title.find("a").get("href").split("-")[-1], 
                    'is_movie': ( html_title.find("div", class_ = "info-split").find("span") == None ),
                    'url': title_url
                })

        return result
    
    else:
        console.log(f"[red]Cant connect to server, error: {response.status_code}")
        sys.exit(0)

def select_title():
    """Print list of result and select a valid index"""

    title = msg.ask("[green]Insert name of a title ")
    print("")
    
    title_result = search_on_server(title)

    for i in range(len(title_result)):
        name = title_result[i].get('name')
        category = "film" if title_result[i].get('is_movie') else "tv  "
        console.print(f"[cyan]Index: [yellow]{i} [white]=> [purple][ [red]{category} | {name} [purple]]")

    print("")
    index = int(msg.ask("[green]Select index "))

    if 0 <= index <= len(title_result):
        return title_result[index]
    
    else:
        console.log("[red]Invalid index for server search")
        sys.exit(0)