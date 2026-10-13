# Mintopia

A 3D crypto-themed clicker. Mine the big coin, buy generators, hire a crew of 24 humans and monsters to run them, climb a ladder of 40 coins, use abilities, then prestige and rebirth for tokens you spend in two shops. Collect crew skins and coin skins along the way.

It is **one static file** (`public/index.html`): no server, no network traffic, and the 3D engine, the sky, the coin emblems and the music are all made in code. **It is a game only: no real money, wallet or cryptocurrency is involved.**

## What is in it

- **Mining that is worth doing.** Tap the coin (or Space, Enter, the Mine button). Every click fills the **hype** meter: at full hype clicks pay x2.5 and your whole crew works 50% faster, but it drains when you stop. **Critical hits** (x10) come from Lucky Fingers upgrades, and Power Tap upgrades add a share of your income to each click.
- **24 generators, 24 crew**, twelve human and twelve monster, each with their own look, prop and way of working. Without a manager you tap the station to run a cycle; with one it runs forever. **The more you own and upgrade, the faster they work** (and animate): +1% per extra unit up to double, +10% per generator upgrade, and team upgrades for everyone.
- **40 coins** from Dust through Pepe, Dogecoin, Solana, Ethereum and Bitcoin to Nebula and Mintopia. Each adds +3% income, and each has its own **emblem** drawn in code (the real coins get their well-known marks, the invented ones get their own). It shows on the big 3D coin and next to the coin name.
- **157 upgrades:** five per generator (x3 income and +10% speed each), ten click boosts, tap and crit upgrades, twelve global boosts, six team-speed boosts.
- **4 abilities** (Frenzy, Overdrive, Coin Storm, Lucky Streak): unlocked by reaching coins, kept forever, trained with prestige tokens.
- **Prestige** (+2% income per token, 8-item shop) and **Rebirth** at 100 tokens (+50% per rebirth token, permanent 6-item shop).
- **Skins:** 9 coin skins and 8 skins for every crew member. Premium crew skins (Neon, Frost, Inferno, Golden, Shadow, Cosmic, Holo) get glowing outlines and floating sparkles; Holo shimmers through the rainbow.
- **A painted sky** (aurora, a ringed planet, twinkling and shooting stars) behind a floating crystal island, **calm generative music** (slow chords and soft bells, made live with Web Audio), 21 achievements, airdrops, offline earnings (25% for up to 8 hours), autosave, export and import codes.
- Works on phones (the menu becomes a bottom panel), keyboard accessible, respects reduced motion, and falls back to a plain mine button if a device cannot run WebGL.

## Develop

```
cd src && python3 build.py          # writes public/index.html
node tests/unit.js                  # 147 checks of the game rules
pip install -r tests/requirements-test.txt && playwright install chromium
cd tests && python3 test_game.py    # about 270 checks in a real browser, about 15 minutes
```

Source: `game.js` (all the rules, no drawing), `icons.js` (coin emblems), `engine.js` (WebGL), `chars.js` (the crew and their skins), `scene.js` (the stage), `bg.js` (the sky), `music.js`, `ui.js`, `head.html`, `logo.svg`.

## Hosting

- **Vercel:** import the repo. `vercel.json` serves `public/` as a static site.
- **GitHub Pages:** Settings > Pages > Source: GitHub Actions; `.github/workflows/pages.yml` deploys `public/`.

## Honest notes

- **Check the name.** "Mintopia" has not been checked for availability or trademarks.
- **Coin logos.** The real coins' emblems are simplified drawings made in code, not the official files. The names and marks belong to their projects. Check what you need before using them commercially.
- **Balance** has only been checked with a simulated player (first prestige token at about 8 to 10 minutes). Expect to tune the numbers at the top of `src/game.js`.
- **The music has been tested with a stand-in for the audio system, not listened to by the people who made the tests.** Judge it by ear and adjust `music.js`.
- The tests ran in Chromium with software 3D. Real graphics cards, real phones, Safari and Firefox have not been tried.
- Saves live in the browser's local storage (a save from the earlier Hodl Heroes name is picked up automatically). Use Export for a backup.
- Add a `LICENSE` file if you want others to reuse the code.
