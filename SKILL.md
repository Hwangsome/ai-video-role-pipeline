---
name: ai-video-role-pipeline
description: Multi-type AI video creation workflow with 5 non-overlapping roles that outputs ready-to-paste Seedance 2.0 image-to-video assets including exact @Image references, first-frame assignments, and full multimodal prompts. Requires or extracts product selling points and user pain points so the video clearly shows benefit and problem. Supports target market/country and platform selection for culturally and platform-matched style, web search and short-video platform research for real creative references. Use for product showcase, lifestyle seeding, talking-head, absurd comedy, plot twist, ASMR, mockumentary. Triggers on Seedance prompt pipeline, video role design, multi-type short video production.
---

# AI Video Role Pipeline (Seedance 2.0 Ready)

Produce complete, copy-paste-ready assets for Jimeng / Seedance 2.0 multimodal video generation. Final deliverable is a **Seedance Asset Package**.

## Core Goal

Every run must end with assets that work immediately in Seedance 2.0:
- Clear list of required images with exact labels and roles
- Exact @Image / @Video / @Audio assignments
- Full production prompt using correct @ syntax
- **Product selling points (卖点) and user pain points (痛点) are explicitly woven into the narrative**
- **Target market/country + target platform style is respected**
- Creative ideas are informed by real short-video references when possible

## Target Market + Platform (重要)

User can specify both. If not specified:
- Market defaults to **中国大陆**
- Platform defaults according to market (中国大陆→抖音, 美国→TikTok, etc.)

### Supported Markets (examples)
| Market | Default Platform | Typical Style Cues |
|--------|------------------|--------------------|
| 中国大陆 | 抖音 | 快节奏、强反差、夸张、卡点、直接卖点、竖屏 |
| 美国 | TikTok | 口语、irony、relatable chaos、trend audio |
| 日本 | TikTok | 精致、细腻、轻微荒诞、高审美 |
| 东南亚 | TikTok | 热情、明亮、生活化、强情绪 |
| 韩国 | TikTok | 干净、有设计感、轻微剧情 |

### Supported Platforms
抖音 · 小红书 · TikTok · YouTube Shorts · Instagram Reels · B站 · Shopee Video

When market + platform are set:
- Research queries bias to that platform and market language
- Narrative tone, humor, pacing, visual references, and length habits match the platform
- Final Asset Package **must state both 目标市场 and 目标平台**

## Research Step (before or inside Content Strategist)

When 卖点 / 痛点 / 创意方向不足时，先做研究：

```bash
python scripts/research_creatives.py "产品名" --type 搞怪离谱 --market 中国大陆 --platform 抖音
python scripts/research_creatives.py "产品名" --market 美国 --platform TikTok
```

Then use the returned queries with `web_search` / `x_keyword_search`, summarize with `scripts/format_insight.py`, and feed into `concept_brief.md`.

Never invent pain points or selling points when real signals are available. Mark inferred items as `[推断]`.

## Input Handling

- Product name only → research + infer 卖点/痛点 + default market 中国大陆 + default platform 抖音
- + target market → style and research biased to that market
- + target platform → further bias research and creative tone to that platform’s norms
- Product images → extract visual + functional selling points, then research
- Explicit 卖点/痛点 list → use directly, still optionally research for local differentiation

Even 搞怪离谱 must serve a clear product benefit or pain-point contrast.

## Seedance 2.0 Hard Constraints

| Input | Limit | Notes |
|-------|-------|-------|
| Images | ≤ 9 | jpeg/png/webp, <30MB each |
| Videos | ≤ 3 | mp4/mov, total 2–15s |
| Audio | ≤ 3 | mp3/wav, total ≤15s |
| Total files | ≤ 12 | prioritize highest-impact assets |
| Duration | 4–15s | match prompt complexity to length |
| Faces | No realistic human faces in uploaded refs | system blocks them |

### @ Reference Syntax (mandatory)

```
@Image1 as the first frame
@Image2's character as the subject
scene references @Image3
product details reference @Image4
reference @Video1's camera movement and action
BGM references @Audio1
```

## Five Non-Overlapping Roles (execute in strict order)

### 1. Content Strategist
**Goal**: Lock content type + **目标市场** + **目标平台** + extract/confirm 卖点 & 痛点 + produce `concept_brief.md`.

Required fields:
- 视频类型
- **目标市场 / 国家**（未指定则默认中国大陆并注明）
- **目标平台**（未指定则按市场默认并注明）
- 核心概念（必须体现产品如何解决痛点或展示卖点，且符合市场+平台风格）
- 用户痛点（1–3个）
- 核心卖点（1–3个，对应痛点）
- 情绪关键词 / 目标受众 / 时长目标 / 风格标签（需反映市场+平台）
- 特殊要求
- 推荐参考素材类型
- （可选）研究来源摘要

**Stop**: Brief complete → hand only the brief.

### 2. Narrative & Shot Director
**Goal**: Type + market + platform adapted `shot_list.md` that forces 痛点 → 卖点 demonstration.

Tone, pacing, humor density, length habits, and cultural/platform references must match.

Each shot notes which 痛点 or 卖点 it serves.

**Stop**: Shot list complete → hand shot_list + brief.

### 3. Visual & Persona Reference Designer
**Goal**: Exact image requirements + `ref_map.md` supporting story, product proof, and market/platform aesthetic.

**Stop**: ref_map clear → hand upstream.

### 4. Seedance Multi-Type Prompt Engineer
**Goal**: Production-ready prompt with correct @ syntax that demonstrates 卖点, contrasts 痛点, and matches target market + platform style.

Must include full ready-to-paste prompt, explicit @ roles, time segments if needed, camera, audio, parameters, and market/platform-appropriate mood/pacing descriptors.

**Stop**: Prompt self-checked → hand final package.

### 5. Generation & Type-QA Specialist
**Goal**: Final **Seedance Asset Package** + QA that checks product relevance and market/platform fit.

**Final Deliverable Format (mandatory)**:

```markdown
# Seedance 2.0 Asset Package

## 0. Product Insight Summary
- 目标市场：
- 目标平台：
- 用户痛点：
- 核心卖点：
- 本视频如何体现：
- （可选）研究来源

## 1. Required Images (upload these in order)
| Label | Purpose | Description of image content |
|-------|---------|------------------------------|
| Image1 | ... | ... |

## 2. Ready-to-Paste Prompt
```
[full prompt with @Image roles + market/platform-appropriate style language]
```

## 3. Generation Parameters
- Duration / Resolution / Generate audio / Mode

## 4. Type-Specific + Product + Market/Platform QA Checklist
- [ ] 痛点是否被清晰感知
- [ ] 卖点是否被动作或画面证明
- [ ] 产品始终可识别
- [ ] 节奏/幽默/视觉是否符合目标市场习惯
- [ ] 是否符合目标平台内容习惯（时长、竖屏、卡点等）
- [ ] ...
```

**Stop**: Package complete → deliver to user.

## Scripts

| Script | Purpose |
|--------|--------|
| `scripts/research_creatives.py` | Generate targeted web/X search queries for product + type + market + platform |
| `scripts/format_insight.py` | Format collected 痛点 / 卖点 / 创意方向 into clean markdown |

## Hard Rules
- Roles never cross boundaries.
- Final output must be copy-paste ready for Seedance 2.0.
- Even 搞怪离谱 must serve product 卖点/痛点 contrast.
- Target market and platform must be stated; defaults applied and noted if unspecified.
- Prefer 4–15s. Keep total reference files ≤12.
- No realistic human faces in reference instructions.
- Every @ reference must state its exact purpose.
- Research when 卖点/创意信号不足；标记推断内容。

## Quick Start
User: “一次性马桶刷 搞怪离谱 中国大陆 抖音”  
或 “一次性马桶刷 搞怪离谱 美国 TikTok”  
或 “一次性马桶刷 搞怪离谱”（默认 中国大陆 + 抖音）  
→ (Optional) research with market + platform bias  
→ Run roles 1→5  
→ Emit complete Seedance Asset Package that explicitly shows 目标市场 + 目标平台.
