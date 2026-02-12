from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from crypto import Crypto
from server import run_server
from client import run_client

console = Console()

console.print(Panel.fit(
    "Helia – خورشیدی در دل تاریکی\nby Backdoor / Bamdad",
    border_style="magenta",
    padding=(1, 2),
))

role = Prompt.ask("Role", choices=["host", "client"], default="client").lower()

if role == "host":
    port = int(Prompt.ask("Port", default="55555"))
    pw = Prompt.ask("Room password", password=True) or "helia2026"

    crypto = Crypto()
    console.print("\n[bold magenta]Helia Key:[/] " + crypto.get_key())
    console.print("[bold violet]Password:[/] " + pw)
    console.print("[bold cyan]Port:[/] " + str(port) + "\n")

    run_server(port, pw, crypto)

else:
    key = Prompt.ask("[magenta]Helia Key[/]", password=True)
    if not key:
        console.print("[red]Key required[/]")
        exit(1)

    host = Prompt.ask("Host IP", default="127.0.0.1")
    port = int(Prompt.ask("Port", default="55555"))

    run_client(host, port, key)
