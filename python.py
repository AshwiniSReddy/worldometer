from worldometer.world import WorldCounters
import os
PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

wc = WorldCounters()

wc.world_population.current_population
print(wc.world_population.births_today)