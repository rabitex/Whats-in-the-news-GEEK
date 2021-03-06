from urllib.request import urlopen
from urllib.error import HTTPError
import json
from logo import printlogo
from colorama import Fore, Style, Back

cmds = {"international": ["BBC News", "CNN", "Daily Mail", "The Guardian UK", "The New York Times", "The Telegraph"],
        "national": ["The Times of India", "The Hindu"],
        "technology": ["Engadget", "Hacker News", "Techcrunch", "TechRadar", "The Next Web"],
        "sports": ["BBC Sport", "ESPN", "ESPN Cric info", "Fox Sports", "TalkSport"],
        "finance": ["Bloomberg", "Business Insider", "Financial Times", "The Wall Street Journal", "Time", "Fortune"],
        "entertainment": ["BuzzFeed", "Entertainment Weekly", "MTV News", "MTV News UK"],
        "science": ["New Scientist"],
        "blog": ["Reddit r all"],
        "adventure": ["National Geographic"],
        "help": ["help", "exit","list-news"],
        "list-news": ["international", "national", "technology", "sports", "finance", "entertainment", "science", "blog", "adventure"]
        }

# global api key to be given by the user.
api_key = None

def news(source):
    #for URL
    url = "https://newsapi.org/v2/top-headlines?sources=" + source + "&apiKey=" + api_key

    # using with .. as to allow closing the url connection by python.
    try:
        with urlopen(url) as httpob:
            decob = httpob.read().decode("utf-8")
            jsonob = json.loads(decob)
            news = jsonob["articles"]

    # if api key is Invalid an HTTPError will be thrown.
    except HTTPError as e:
        print("Invalid API")
        create_api_file(file_name)
        return console()

    # draws a border to seperate posts.
    draw_border()
    for n in news:
        print(Fore.RESET)
        try:
            key = n["source"]
            print(Back.YELLOW + key["name"] + Back.RESET)
            print(Back.RED + (Style.BRIGHT + n["title"] + Style.RESET_ALL)) 
            print(Fore.BLUE + n["description"] + Fore.RESET)
        except:
            print(Fore.RED + "SOME ERROR OCCURED!!!\n" + Fore.RESET)

        print(Fore.YELLOW + "want to read more:" + Back.RESET)
        print(Fore.GREEN + (Style.DIM + n["url"]))
        print(Style.NORMAL)
        print(Fore.MAGENTA + "powered NewsAPI.org")
        print(Style.NORMAL)
        # print(Fore.RESET)

        draw_border()

def draw_border():
    width = 80
    print(Style.BRIGHT+"-" * width +Style.RESET_ALL+"\n")


def src(n):
    k = n.replace(" ", "-")
    return k


def create_api_file(file_name):
    """
    This method creates a new file, with the name
    'file_name'.

    This file will store the api key for the user.
    """
    global api_key
    api_key = input("Enter a valid API key: ")

    with open(file_name, "w") as f:
        f.write(api_key + '\n')
    f.close()
    print("The API key is: " + api_key)


def get_api():
    global api_key 

    # the api once entered will be stored in this file.
    global file_name 
    file_name = "user-api.txt"

    try:
        f = open(file_name, "r") 
        api_key = f.readline()
        f.close()
        print("The API key is: " + api_key)
        print("Do you want to change the API key? [Y/N]\n")
        flag = input()
        if flag == 'Y':
            create_api_file(file_name)


    # if the file was not found then create the file and store the api.
    except FileNotFoundError:
        create_api_file(file_name)

    # if the api_key in the file was not present (i.e, empty file)
    # get the api from the user.
    if api_key == None or len(api_key) == 0:
        create_api_file(file_name)

def console():
    while True:
        cmd = input(">>> ")

        # command is invalid
        if (cmd not in cmds["list-news"] and cmd not in cmds["help"]):
            print(Fore.RED + "WRONG COMMAND!!!")
            print(Fore.GREEN + "Try these COMMANDS" + Fore.RESET)
            for c in cmds["help"]:
                print("    " + c)

        # help command
        elif cmd == "help":
            print(Fore.GREEN + "Try these COMMANDS" + Fore.RESET)
            for c in cmds["help"]:
                print("    " + c)

        # list command
        elif cmd == "list-news":
            print(Fore.GREEN + "Find news about any of these topics" + Fore.RESET)
            for l in cmds["list-news"]:
                print("    " + l)

        # exit command
        elif cmd == "exit":
            print(Style.RESET_ALL)
            exit()

        # show news
        else:
            for n in cmds[cmd]:
                s = src(n)
                news(s)

if __name__ == "__main__":
    printlogo()
    print(Style.DIM + "powered by NewsAPI.org\n" + Style.NORMAL)

    # get the user api first.
    get_api()

    # display the console.
    console()
