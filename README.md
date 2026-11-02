# Talvio Generator — Black Dot

10,000 Black Dot robot NFTs on BNB Chain, inspired by the HelloAgents mint flow.
First 2 free per wallet, then 0.002 BNB per mint, max 20 paid mints per wallet.

## Contents

- `index.html` — Talvio Generator mint website (Black Dot theme, logo + name top-left, realistic #0001 hero, free/paid mint tiers, Mint with an Agent prompt). Set `CONTRACT_ADDRESS` in the file after the ERC-721 contract is deployed.
- `Talvio-BlackDot-0001-metadata.json` — metadata for genesis example #0001.
- `sample-100/metadata/` — metadata for the 100 approved sample variations, with `sample-100/traits-all-100.json` combined.
- `collection-10000/metadata/` — metadata for all 10,000 tokens (#00001–#10000), with the combined traits split across `collection-10000/traits-all-10000-part1..4.json`.
- `tools/` — the trait generators used to create the sample and the full collection (Python + Pillow).

## Collection

- 10,000 unique trait combinations, 10,000 unique images (1024×1024 PNG), verified by image hash.
- Rarity: 3,210 Common · 4,002 Rare · 2,127 Epic · 661 Legendary.
- Traits: Background, Face, Ears, Eyes, Antenna, Chest Core, Mouth, Extra, Aura, Body.

## Status

Artwork and metadata are generated. The smart contract is not deployed yet, so nothing is minted on-chain.
