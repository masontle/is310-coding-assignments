# Factorio Furnace Tradeoffs

## Question
How do Factorio's three standard furnace types compare in crafting speed, energy use, and pollution?

The [Official Factorio Wiki](https://wiki.factorio.com/Furnace) is a community-edited source with consistent equipment statistics. Comparing furnaces can help researchers examine how a factory-building game balances technological progress against energy and environmental costs.

## Collection and rules
The scraper uses `requests` and `BeautifulSoup`. It follows links from the furnace overview to the stone, steel, and electric furnace articles, then extracts normal-quality crafting speed, rated energy consumption, energy type, drain, and direct pollution into `furnace_data.csv`. Each row includes source links and a collection time.

On October 25, 2026, [robots.txt](https://wiki.factorio.com/robots.txt) had an empty `Disallow` rule for all agents, so it prohibited no paths. The [community rules](https://wiki.factorio.com/Factorio:Wiki_rules) and [copyright policy](https://wiki.factorio.com/Factorio:Copyrights) were also reviewed. Wiki text is generally CC BY-NC-SA 3.0; game assets have separate rights. Source credit: Official Factorio Wiki contributors. Reused wiki material must retain attribution, noncommercial use, and share-alike terms.

The script sends an identifying User-Agent, pauses at least three seconds between requests, checks robots rules, and stops on non-200 responses or bot challenges. `robots_snapshot.txt` and `collection_metadata.json` record the collection checks.

## Results

| Furnace | Crafting speed | Rated energy (kW) | Direct pollution/min |
| --- | ---: | ---: | ---: |
| Stone | 1 | 90 | 2 |
| Steel | 2 | 90 | 4 |
| Electric | 2 | 180 | 1 |

Steel doubles stone's crafting speed at the same rated energy use, while doubling direct pollution. Electric matches steel's speed and reduces direct pollution, but requires electricity at a higher rated power and has a separate 6 kW drain.

## Limitations
These are wiki-reported baseline statistics, not measurements of a working factory. Direct furnace pollution excludes electricity generation, and the comparison omits modules, beacons, higher quality, idle time, and construction costs. Lower direct pollution therefore does not prove that an electric furnace makes the whole factory cleaner, or that one furnace is always the best choice.

## Run
From this folder, replace the example contact with your own:

```powershell
python -m pip install -r requirements.txt
python wiki_scraping.py --contact "Mason Le; masonle2@illinois.edu"
```
