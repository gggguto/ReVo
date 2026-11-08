# ReVo — Generative Soundscapes

Hello, traveller. Welcome to ReVo: an experimental soundscape instrument for the **M-VAVE FM-1**, and a fertile ground for sonic exploration.

**[Explore ReVo](https://gggguto.github.io/ReVo/) · [Field guide](https://gggguto.github.io/ReVo/manual/) · [Firmware](https://gggguto.github.io/ReVo/install/) · [Samples](https://gggguto.github.io/ReVo/samples/)**

There are two islands waiting for you:

- **Bioma** — a synthesized ecosystem. Birds, Insects and Water listen and answer; Wind, Drift, Beam and Resonance shape the landscape.
- **Atolls** — two independent sample loops. Guide their windows, play Fragments, mark Landing destinations and let Flock and V Format move between them.

Concept, sound direction and interaction design by **[gggguto](https://gggguto.com)**. Built on **Felucca and SLOOP**; original platform, component and license notices are preserved in [CREDITS.md](CREDITS.md).

## Firmware 1.0

The downloadable package is **build2026110608**, with Bioma opening by default and both machines using the dual-core pipeline. The manifest includes the exact package hash and matching source archive. MIDI tests in Bioma and Atolls were confirmed on the author’s FM-1 on 8 November 2026; native sanitizer and exact-package emulator tests also passed.

Open Firmware in Chrome or Edge and follow the installer. The site checks package identity and SHA-256 before updating. The matching source and recovery instructions are available on the same page.

## MIDI

- [Bioma notes and CCs](https://gggguto.github.io/ReVo/manual/bioma-midi/): Wind, global controls, Birds, Insects, Water, Resonance, FX, Drift and Beam.
- [Atolls notes and CCs](https://gggguto.github.io/ReVo/manual/midi/): loop transport, Fragments and loop parameters.

MIDI Clock and performance control are independent selections in Settings. MIDI CONTROL starts OFF.

## Samples

The browser editor displays the four device slots, lets you crop a WAV to the supported **7.384 seconds**, optionally normalize, and audition the decoded ADPCM result before writing a selected slot. Choose Atolls before writing samples. Your source recordings stay in your browser; they are not uploaded to a server.

## Local preview and checks

Python 3 and Node.js 20+ are sufficient; the website has no runtime package dependencies.

```sh
python3 tools/check_site.py
node tools/samples-check.mjs
python3 -m http.server 8767 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:8767/. The sample-editor tests use simulated MIDI and never write to hardware.

## Repository layout

- `site/`: website, field guides, firmware installer, sample editor and credits.
- `site/install/`: firmware package, SHA-256 manifest and matching GPL source download.
- `site/assets/`: original native LCD captures, animation frames, sprites and bitmap-derived fonts.
- `tools/`: website and sample-editor checks.
- `.github/workflows/pages.yml`: validates and publishes `site/` to GitHub Pages.

The screen animations replay the firmware’s original LCD captures. Typography derives from Terminus bitmap fonts, with the renamed font files, original BDF sources and SIL OFL license included.

See [LICENSE](LICENSE), [CREDITS.md](CREDITS.md) and the matching firmware source archive for licenses and attribution. Personal recordings and diagnostic logs are not part of this repository.
