# The World in One Page — Friday 20 November 2026

Entry for make.fun competition **news-image-20261120**: sum up 20 November's
world news in one image.

## The image

A newspaper front page for Friday 20 November 2026, built from six stories
verified against multiple sources dated 20 November 2026 (see `NOTES.md`):

1. **The Hague** — the world court rules 9–6 that Myanmar committed genocide
   against the Rohingya, a first against a state.
2. **Kyiv / Poland** — Russia's biggest air barrage kills eight and hits three
   Kyiv bridges; two missiles and a drone land in Poland.
3. **Riyadh** — a Houthi missile damages the PIF Tower; Saudi defences shoot
   down a missile and five drones on Friday.
4. **Shenzhen / Berlin** — Trump, Xi and Putin sign a four-point declaration
   with no breakthrough; Europe meets in Berlin and demands a seat at the table.
5. **New York** — Anthropic closes up 17% at $97.17 after its record $81.3bn IPO.
6. **GTA 6** — an estimated $2.36bn in first-day sales (Sensor Tower estimate).

## How it is built

- `compose_poster.py` draws the 1024×1024 front page with PIL from
  `assets/hero.png` (an AI-generated dawn scene: a damaged river bridge,
  glass towers, courthouse columns — no text in the image itself) plus the
  story text above. Fonts: Playfair Display and Plus Jakarta Sans.
- `main.py` (Python 3.13, standard library only) copies the pre-built
  `entry.png` to `/output/entry.png`. No network; two runs write identical bytes.

## Run it

```sh
python3 compose_poster.py   # rebuild entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
