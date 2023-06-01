from rich import print as rprint
from datetime import datetime
import traceback

def error(*body):
    print("\033[0;31;40m│\033[0m",end="")
    msg = ""
    flag = False
    for i in body:
        if "Error" not in str(type(i)): 
            msg += str(i) + " "
        else: flag = True
    rprint("[[bold green]" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "[/bold green]] [bold red]MuuD Server[/bold red] [[bold red]error[/bold red]] > [bold yellow]" + msg + "[/bold yellow]")
    if flag: traceback.print_exc()

def success(*body):
    print("\033[0;31;40m│\033[0m",end="")
    msg = ""
    for i in body:
        msg += str(i) + " "
    rprint("[[bold green]" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "[/bold green]] [bold red]MuuD Server[/bold red] [[bold green]success[/bold green]] > " + msg)

def info(*body):
    print("\033[0;31;40m│\033[0m",end="")
    msg = ""
    for i in body:
        msg += str(i) + " "    
    rprint("[[bold green]" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "[/bold green]] [bold red]MuuD Server[/bold red] [[bold blue]info[/bold blue]] > " + msg)

def banner(*body):
    rprint("[bold red] ███╗   ███╗██╗   ██╗██╗   ██╗██████╗  [/bold red]")
    rprint("[bold red] ████╗ ████║██║   ██║██║   ██║██╔══██╗ [/bold red]")
    rprint("[bold red] ██╔████╔██║██║   ██║██║   ██║██║  ██║ [/bold red]")
    rprint("[bold red] ██║╚██╔╝██║██║   ██║██║   ██║██║  ██║ [/bold red]")
    rprint("[bold red] ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██████╔╝ [/bold red]")
    rprint("[bold red] ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝  [/bold red]")