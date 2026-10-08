"""Collect and save local cultural-event data from the command line."""

import json
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.text import Text


console = Console()
DATA_FILE = Path(__file__).with_name("cultural_events.json")
FIELDS = (
    ("event_name", "Event name"),
    ("event_type", "Type (music, art, food, etc.)"),
    ("venue", "Venue or location"),
    ("event_date", "Date (YYYY-MM-DD or your preferred format)"),
    ("admission", "Admission (free, price, or unknown)"),
)

EXAMPLE_EVENTS = [
    {
        "event_name": "Example: Community Mural Day",
        "event_type": "Public art",
        "venue": "Example location (fictional)",
        "event_date": "2026-10-18",
        "admission": "Free",
    },
    {
        "event_name": "Example: Student Music Showcase",
        "event_type": "Live music",
        "venue": "Example location (fictional)",
        "event_date": "2026-10-24",
        "admission": "Free",
    },
]


def show_events(events, title):
    """Display a list of event dictionaries as a Rich table."""
    table = Table(title=title, header_style="bold cyan")
    table.add_column("Event", style="magenta")
    table.add_column("Type")
    table.add_column("Venue")
    table.add_column("Date", no_wrap=True)
    table.add_column("Admission")

    for event in events:
        # Text keeps square brackets in user input from becoming Rich formatting.
        table.add_row(*(Text(str(event[field])) for field, _ in FIELDS))

    console.print(table)


def load_events():
    """Load previously saved events, or start with an empty list."""
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as data_file:
        events = json.load(data_file)
    if not isinstance(events, list) or not all(
        isinstance(event, dict)
        and all(isinstance(event.get(field), str) for field, _ in FIELDS)
        for event in events
    ):
        raise ValueError("The saved file must be a list of event records with all five fields.")
    return events


def ask_yes_no(prompt):
    """Keep asking until the user gives a yes or no answer."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        console.print("[yellow]Please enter y or n.[/yellow]")


def save_events(events):
    """Write a temporary file before replacing the previous saved data."""
    temporary_file = DATA_FILE.with_suffix(".json.tmp")
    with temporary_file.open("w", encoding="utf-8") as data_file:
        json.dump(events, data_file, indent=2, ensure_ascii=False)
        data_file.write("\n")
    temporary_file.replace(DATA_FILE)


def collect_event():
    """Ask for one event and repeat until the user confirms it."""
    while True:
        console.print("\n[bold cyan]Enter one cultural event[/bold cyan]")
        event = {}
        for field, label in FIELDS:
            value = input(f"{label}: ").strip()
            while not value:
                console.print("[yellow]Please enter a value, or unknown if you don't know.[/yellow]")
                value = input(f"{label}: ").strip()
            event[field] = value

        show_events([event], "Please review your entry")
        if ask_yes_no("Is this entry correct? (y/n): "):
            return event
        console.print("[yellow]No problem. Let's enter that event again.[/yellow]")


def main():
    console.print("[bold cyan]Local Cultural Events Data Collector[/bold cyan]")
    console.print("The examples below are fictional and are only here to demonstrate the fields.")
    show_events(EXAMPLE_EVENTS, "Example cultural-event data")

    events = load_events()
    if events:
        console.print(f"\nFound {len(events)} previously saved event(s).")

    added = 0
    while True:
        events.append(collect_event())
        save_events(events)
        added += 1
        console.print(f"\n[bold green]Saved {added} confirmed event(s) this session.[/bold green]")
        console.print("All collected data is in:")
        console.print(str(DATA_FILE.resolve()), markup=False)
        if not ask_yes_no("Add another event? (y/n): "):
            break


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        console.print("Unable to read or save the data:", style="bold red")
        console.print(str(error), markup=False)
        console.print("Check the data file and try again. Existing saved data has been kept.")
        raise SystemExit(1)
    except (EOFError, KeyboardInterrupt):
        console.print("\nSession ended. Previously confirmed entries remain saved.")
