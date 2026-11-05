# AI Video Role Pipeline Skill (Seedance 2.0 Ready)

Multi-type AI video creation skill. Final output is a **copy-paste-ready Seedance Asset Package**.

## Key Features
- **Step 0: First asks user for product images, 卖点, 痛点** (then combines with web research)
- Strict Seedance 2.0 @ reference syntax and constraints
- Explicit image role assignments + time-segmented prompts
- Forces 卖点 + 痛点 into the narrative (with source labels)
- Target market/country + target platform selection
- Research scripts for market + platform biased creative search
- Final Asset Package always states 目标市场、目标平台、来源

## Scripts
- `scripts/research_creatives.py` — generate search queries for product + type + market + platform
- `scripts/format_insight.py` — format collected pain points, selling points and ideas

## Supported Types
产品展示 · 生活种草 · 人物口播 · 搞怪离谱 · 剧情反转 · 感官氛围/ASMR · 伪纪录/采访

## License
MIT
