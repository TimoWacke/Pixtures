import platform
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich import box

from app.core.settings import settings

console = Console()


def create_startup_message() -> None:

    # Create the main title
    title = Text()
    title.append("🌇 ", style="bright_yellow")
    title.append(f"{settings.PROJECT_NAME}", style="bold bright_blue")
    title.append(" is ready to roll!", style="bright_green")

    # Create main table
    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 1), width=100)
    table.add_column("Key", style="bright_yellow", width=12)
    table.add_column("Value", style="bright_white")

    # Add separator function for visual grouping
    def add_separator() -> None:
        table.add_row("-" * 15, "-" * 40)

    # Add environment information
    table.add_row("Environment", settings.ENVIRONMENT)
    table.add_row("API Version", settings.API_V1_STR)
    table.add_row("Frontend URL", settings.FRONTEND_DOMAIN)
    table.add_row("Service Runs on"), settings.SELF_DOMAIN

    add_separator()

    table.add_row("MongoDB Database", settings.MONGO_DATABASE)
    table.add_row("MongoDB Host", settings.MONGO_HOST)

    add_separator()

    table.add_row("Platform", platform.platform())
    table.add_row("Python Version", platform.python_version())
    table.add_row("Listening on", settings.APP_PORT)

    panel = Panel(
        table,
        title=title,
        subtitle="[bright_yellow]Press Ctrl+C to exit[/bright_yellow]",
        border_style="bright_yellow",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")
