# ReVo — Credits and licenses

ReVo incorporates and adapts open-source work. Credits do not replace the license texts, copyright notices or corresponding-source obligations.

## ReVo — original work

Concept, sound direction and interaction design: **gggguto**.

ReVo's original machines are **Bioma** and **Atolls**. Their musical identities, parameter relationships, screen designs and performance workflows were developed for this project.

- **Bioma:** event-based soundscape composition; Birds phrase and timbre design; relationships among Birds, Insects, Water, Wind, Ocean Tide and Resonance; Drift/Beam and per-source interaction design.
- **Atolls:** the dual-loop performance model and its interaction design, including Fragments gestures, Flock, Landing destinations, V Format relationships, Motion, per-loop shaping and selective shared FX routing.
- **ReVo integration:** the owned-packet dual-core engine/FX pipeline, diagnostic protocol and analysis workflow, source-routing integration, native display system and instrument-specific controls.

This credits ReVo's original combinations, behaviors and project-specific implementations. The platform, reusable engines/components and adapted code remain credited separately below; their original notices and licenses are preserved.

## Firmware foundations and reused sample codec

- Felucca — Leo Kuroshita (@kurogedelic), Hügelton Instruments. GPL-3.0-only. https://github.com/hugelton/Felucca
- SLOOP — isod89 and contributors; based on Felucca. GPL-3.0-only. https://github.com/isod89/sloop-fm1
- IMA ADPCM encoder and tables: extracted from SLOOP tools/sampleio.py; native decoder tables from firmware/src/eng_sample.c. Original copyright preserved. ReVo adds indexed access and independent decode caches. FSMP storage layout and header-last persistence are adapted from eng_sample.c/editor.c, using the original HAL flash driver. The installer reuses fm1ota.js and fm1pkg.js unchanged. See sample-codec/provenance.json.

## Local development and previews

- fm1-emu — Joakim Eriksson. MIT. https://github.com/joakimeriksson/fm1-emu
- Terminus Font — Dimitar Toshkov Zhekov. SIL Open Font License 1.1. Font notices and full license supplied locally.
- JieLi toolchain and AC79 SDK are build/platform dependencies, governed by their respective supplied terms; they are not authored by ReVo.
- Emscripten, Clang/LLVM, Python, Node.js and Docker are development tools. Their use does not mean every tool is embedded in the firmware.

## References, not imported components

M-VAVE fm1_open / Workbench and the aroum resource directory were researched. No official Workbench/SDK component has been imported in this stage; no Relay component was imported. Future imports require a recorded source, version/hash and applicable license.

## Local independence

The reused codec executes locally. No third-party account, cloud API or hosted editor is required by it. Sample preparation, format conversion and USB transfer run locally. The public editor prepares up to 7.384 seconds per saved slot.

This inventory is maintained as components are integrated. Existing file-level notices and full third-party licenses remain part of the deliverable.

The website uses ReVo Field Text / Display, outlined conversions of the firmware’s Terminus bitmap glyphs. Modified font family names distinguish them from the original font. The original BDF sources and OFL notice are supplied under site/assets/.
