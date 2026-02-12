from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

console = Console(highlight=False)

def ts():
    return f"[dim]{datetime.now().strftime('%H:%M:%S')}[/]"

def sys(text):
    line = Text.assemble(
        (ts(), "dim"),
        (" Helia ", "bold black on magenta"),
        (f" {text}", "white")
    )
    console.print(Panel(line, border_style="magenta dim"))

def msg(nick, text):
    line = Text.assemble(
        (ts(), "dim"),
        (f" {nick} ", "bold black on violet"),
        (f" {text}", "white")
    )
    console.print(Panel(line, border_style="violet"))

def pm(from_nick, text):
    line = Text.assemble(
        (ts(), "dim"),
        (" PM ", "bold black on purple"),
        (f" {from_nick} → {text}", "purple")
    )
    console.print(Panel(line, border_style="purple"))

def info(text):
    console.print(f"[bold magenta]{text}[/]")

def error(text):
    console.print(f"[bold red]✗ {text}[/]")
