"""Compare speed, energy, and pollution for Factorio's standard furnaces."""

import argparse
import csv
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE = "https://wiki.factorio.com"
INDEX = BASE + "/Furnace"
OUT = Path(__file__).resolve().parent


def read_stats(soup):
    box = soup.select_one(".infobox")
    if box is None:
        raise RuntimeError("Infobox missing; inspect the page.")
    stats = {}
    for row in box.select("tr"):
        cells = row.find_all("td", recursive=False)
        if len(cells) == 2:
            stats[cells[0].get_text(" ", strip=True)] = cells[1]
    return stats


def number(cell, label):
    if cell is None:
        raise RuntimeError(f"Missing field: {label}")
    # Normal quality is listed first, before higher-quality variants.
    match = re.match(r"\s*(\d+(?:\.\d+)?)", cell.get_text(" ", strip=True))
    if not match:
        raise RuntimeError(f"Cannot read number for {label}")
    return float(match.group(1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contact", default="Mason", help="Your name and optional email/profile")
    args = parser.parse_args()
    if not args.contact.strip() or any(c in args.contact for c in "\r\n"):
        parser.error("Provide your name/contact on one line.")
    agent = f"is310-course-scraper/1.0 ({args.contact}; educational wiki project)"
    session = requests.Session()
    session.headers.update({"User-Agent": agent})
    delay = 3.0
    previous = None
    log = []

    def fetch(url, robots=None):
        nonlocal previous
        if robots is not None and not robots.can_fetch(agent, url):
            raise RuntimeError(f"robots.txt disallows {url}")
        if previous is not None:
            time.sleep(max(0.0, delay - (time.monotonic() - previous)))
        try:
            response = session.get(url, timeout=30, allow_redirects=False)
        finally:
            previous = time.monotonic()
        print(response.status_code, url, flush=True)
        log.append({"url": url, "status_code": response.status_code})
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}; stopping without parsing or retrying.")
        if "Just a moment..." in response.text or "Enable JavaScript and cookies" in response.text:
            raise RuntimeError("Bot challenge detected; stopping.")
        return response.text

    robots_text = fetch(BASE + "/robots.txt")
    robots = RobotFileParser()
    robots.parse(robots_text.splitlines())
    delay = max(delay, float(robots.crawl_delay(agent) or 0))
    rate = robots.request_rate(agent)
    if rate:
        delay = max(delay, rate.seconds / rate.requests)

    # First level: discover furnace article links on the overview page.
    index = BeautifulSoup(fetch(INDEX, robots), "html.parser")
    content = index.select_one("#mw-content-text .mw-parser-output")
    if content is None:
        raise RuntimeError("Overview content missing.")
    links = {}
    for anchor in content.select("a[href]"):
        url = urljoin(INDEX, anchor["href"])
        parts = urlsplit(url)
        if (parts.scheme == "https" and parts.netloc == "wiki.factorio.com"
                and parts.path.endswith("_furnace") and not parts.query and not parts.fragment):
            links[url] = parts.path.lstrip("/").replace("_", " ")
    if len(links) != 3:
        raise RuntimeError(f"Expected three standard furnace articles; found {len(links)}.")

    # Second level: read the statistics in each linked article's infobox.
    records = []
    for url, name in links.items():
        stats = read_stats(BeautifulSoup(fetch(url, robots), "html.parser"))
        energy = stats.get("Energy consumption")
        pollution = stats.get("Pollution")
        if energy is None or "kW" not in energy.get_text():
            raise RuntimeError("Energy field or kW unit missing.")
        if pollution is None or "/m" not in pollution.get_text():
            raise RuntimeError("Pollution field or per-minute unit missing.")
        records.append({
            "furnace": name,
            "crafting_speed_normal": number(stats.get("Crafting speed"), "Crafting speed"),
            "energy_consumption_kw": number(energy, "Energy consumption"),
            "energy_type": "electric" if "electric" in energy.get_text() else "burner",
            "drain_kw": number(stats["Drain"], "Drain") if "Drain" in stats else 0.0,
            "direct_pollution_per_minute": number(pollution, "Pollution"),
            "source_url": url,
            "index_url": INDEX,
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        })

    # Write results only after all pages succeed.
    with (OUT / "furnace_data.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    (OUT / "collection_metadata.json").write_text(json.dumps({
        "user_agent": agent,
        "delay_seconds": delay,
        "requests": log,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    }, indent=2) + "\n", encoding="utf-8")
    (OUT / "robots_snapshot.txt").write_text(robots_text, encoding="utf-8")
    print(f"Saved {len(records)} furnace records.")


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, RuntimeError) as error:
        raise SystemExit(f"Collection stopped: {error}")

