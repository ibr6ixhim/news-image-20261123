# THE WORLD IN ONE DAY — 38 stories, Monday 23 November 2026: Zelenskyy confirms the Merkury sinking, Nvidia surges 30% as Huang returns, Iran flogs singer Parastoo Ahmadi

[![Make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/ibr6ixhim/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/ibr6ixhim/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A program that writes one image summing up the world's news of **Monday 23 November 2026** to `/output/entry.png`. The image is a dense newspaper front page — 38 verified stories from 7 regions — drawn with Python's PIL and copied by `main.py` (standard library only, no network, byte-identical on every run).

Built with [make.fun](https://make.fun/r/8kq0s40d) — enter the bounty yourself with my referral link: https://make.fun/r/8kq0s40d

## The three biggest stories

1. **Zelenskyy confirms Ukraine sank the Russian corvette Merkury** off Libya — seven Ukrainian sea drones sank the corvette in Benghazi harbour and hit the cargo ship Angara; confirmed in his speech to NATO's Parliamentary Assembly in Berlin. (AP, WSJ, BBC, The Times — CONFIRMED)
2. **Huang returns as Nvidia chief; Nasdaq +7%, Nvidia +30%** — its biggest one-day gain in 23 years, while Asian tech stocks fell deeper into the AI sell-off. (Reuters — CONFIRMED)
3. **Iran flogs singer Parastoo Ahmadi, 74 lashes, in Qom** — she and four band members were punished for performing without a hijab. (wires — REPORTED)

## Stories by region (38 total)

**America (7):** Nvidia/Huang; US sanctions on Iran's shadow banking; Commanders 22–20 Bengals (MNF); US Army lead-azide detonation in Iowa; FBI probes NCIC hack; masked ICE agents detain father and son at Sea-Tac; NBA: Bucks end 13-game skid.

**Europe (10):** Merkury confirmation; Kyiv toll rises to at least 15; EU proposes new Russia sanctions (60 banks, 70 ships); Belgium's airports shut for a day; Finland summons Russia's ambassador; Russia warns Estonia of open war; NATO meets over Poland missile strike; eurozone inflation 4.0%; UN autonomous-weapons talks end without a deal; Poland: Russia tried to kill rapper Kyivstoner twice.

**Asia (6):** India gives €1.4bn to Nepal; Kim Jong-un stresses sovereignty; Indonesia candy-factory fire — 24 body bags recovered; Asian tech stocks fall; Bitcoin falls to ~$55,100 then recovers near $61,000; BepiColombo enters Mercury orbit.

**Middle East (5):** Ahmadi flogging; Iran vows to fight a US Hormuz blockade; Israeli strike on Gaza truck kills 3, including an UNRWA staffer; Saudi strike on Hodeida, Yemen; Oxfam: toxic contamination in 99% of Gaza.

**Africa (3):** Kenya and DR Congo restore full diplomatic ties; WHO chief urges peace as fighting disrupts the Ebola response; drone hits a home and a UN building in Khartoum.

**Oceania (3):** Molly Meldrum dies aged 83; NZ–India Test drawn in Wellington, Australia back to No. 2; New Zealand retail sales +2.2% in Q3.

**Latin America (4):** Drone hits police base in Cúcuta, Colombia; Bolsonaro diagnosed with pneumonia in ICU, surgery cancelled; Bukele eyes a third term; Argentina's Senate approves a permanent disability law.

## Date discipline

Every story happened or was first reported on Monday 23 November 2026. The image carries a **DATE CHECK** box listing what was deliberately left out because it happened earlier: the COP31 collapse (22 Nov), the Democrats' 258 House seats (22 Nov), the arrest of Chapo Isidro (21 Nov) and the California concert shooting (21 Nov). The Merkury sinking itself happened early Sunday 22 Nov — Monday's news is Zelenskyy's confirmation.

## How it works

- `render.py` — draws the 1024×1024 PNG front page with PIL (deterministic: two runs produce byte-identical files).
- `main.py` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), prints its SHA-256.

## Verify locally

```bash
python3 render.py            # writes entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
sha256sum out1/entry.png out2/entry.png entry.png   # all three identical
```

## License

MIT — see [LICENSE](LICENSE).
