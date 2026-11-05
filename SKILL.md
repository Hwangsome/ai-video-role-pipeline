---
name: ai-video-role-pipeline
description: Multi-type AI video creation workflow with 5 non-overlapping roles that outputs ready-to-paste Seedance 2.0 image-to-video assets including exact @Image references, first-frame assignments, and full multimodal prompts. First asks user for product images, selling points and pain points (then combines with web research). Supports target market/country and platform selection for culturally and platform-matched style. Use for product showcase, lifestyle seeding, talking-head, absurd comedy, plot twist, ASMR, mockumentary. Triggers on Seedance prompt pipeline, video role design, multi-type short video production.
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

## Step 0 — First Ask the User (mandatory before full pipeline)

Before locking the concept or running the 5 roles, **always ask the user** for the following (in one clear message):

1. **产品图 / 已有素材**
   - 你现在有哪些产品相关图片？（完整包装图、刷头特写、使用场景、前后对比等）
   - 可以上传或描述，没有也可以说「没有，请帮我规划需要哪些图」

2. **卖点（可多选或补充）**
   - 你认为这个产品最想突出的 1–3 个卖点是什么？
   - 如果不确定，可以说「不确定，请结合网上信息帮我提炼」

3. **痛点（可多选或补充）**
   - 目标用户现在最烦的是什么？有哪些使用痛点？
   - 如果不确定，可以说「不确定，请结合网上信息帮我找」

4. （可选但推荐）**目标市场 + 平台**
   - 例如：中国大陆 + 抖音 / 美国 + TikTok / 中国大陆 + 小红书 等

然后：
- 用户已提供的卖点/痛点 → 优先采用
- 用户说「不确定」或只给了部分 → 用 `scripts/research_creatives.py` + web_search / x_keyword_search 补充
- 最终在 concept_brief 和 Asset Package 里标注来源：`[用户提供]` / `[网上研究]` / `[推断]`

**不要在用户还没回答产品图、卖点、痛点之前就直接输出完整分镜和 Seedance 提示词。**

## Target Market + Platform

User can specify both. If not specified after asking:
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

## Research Step (after user reply, if needed)

When用户对卖点/痛点说「不确定」或信息不足时：

```bash
python scripts/research_creatives.py "产品名" --type 搞怪离谱 --market 中国大陆 --platform 抖音
python scripts/research_creatives.py "产品名" --market 美国 --platform TikTok
```

用返回的 query 调用 `web_search` / `x_keyword_search`，再用 `scripts/format_insight.py` 整理，与用户提供的内容合并后写入 `concept_brief.md`。

Never invent pain points or selling points when real signals (user or web) are available. Mark inferred items as `[推断]`.

## Input Handling Summary

| 用户输入情况 | 行为 |
|--------------|------|
| 只给产品名 | 先问产品图、卖点、痛点、市场/平台 |
| 给了卖点/痛点 | 优先使用，可再网上补充差异化创意 |
| 说「不确定」 | 启动研究脚本 + web search，再与用户确认关键结论 |
| 给了产品图 | 从图片提取视觉/功能卖点，再问/补充痛点 |
| 明确市场+平台 | 全程按该市场+平台风格执行 |

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

## Five Non-Overlapping Roles (execute in strict order, after Step 0)

### 1. Content Strategist
**Goal**: After collecting user input + optional research, lock content type + 目标市场 + 目标平台 + 卖点 & 痛点 + produce `concept_brief.md`.

Required fields:
- 视频类型
- **目标市场 / 国家**
- **目标平台**
- 核心概念（必须体现产品如何解决痛点或展示卖点，且符合市场+平台风格）
- 用户痛点（1–3个，标注来源）
- 核心卖点（1–3个，对应痛点，标注来源）
- 情绪关键词 / 目标受众 / 时长目标 / 风格标签
- 已有产品图情况 / 需要补拍或生成的参考图
- 特殊要求
- （可选）研究来源摘要

**Stop**: Brief complete → hand only the brief.

### 2. Narrative & Shot Director
**Goal**: Type + market + platform adapted `shot_list.md` that forces 痛点 → 卖点 demonstration.

Tone, pacing, humor density, length habits, and cultural/platform references must match.
Each shot notes which 痛点 or 卖点 it serves.

**Type structure rules (必须遵守)**:
- 产品展示 → 痛点场景 → 产品出现 → 卖点演示 → 结果
- 生活种草 → 日常痛点瞬间 → 自然使用 → 轻松解决
- 人物口播 → 先说痛点 → 再展示卖点证据
- **搞怪离谱 → 必须足够离谱**：别人的产品很惨/很普通 → 我们的产品夸张到开挂级别的强 → 冷静收尾强调真实卖点。动作和逻辑要夸张到让人觉得「这也行？」
- **剧情反转 / 强反差 → 反差必须夸张**：把痛点放大到崩溃，再用我们的产品把效果夸张到「一次搞定/干净到反光」，预期被大幅打破
- ASMR → 感官细节强化产品质感卖点
- 伪纪录 → 观察痛点 → 自然露出卖点

**Stop**: Shot list complete → hand shot_list + brief.

### 3. Visual & Persona Reference Designer
**Goal**: Exact image requirements + `ref_map.md` supporting story, product proof, and market/platform aesthetic.
优先复用用户已有产品图，不足部分明确列出需要补充的图。

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
- 用户痛点：（来源标注）
- 核心卖点：（来源标注）
- 本视频如何体现：
- 已有/需要的产品图情况：
- （可选）研究来源

## 1. Required Images (upload these in order)
| Label | Purpose | Description of image content | 来源建议 |
|-------|---------|------------------------------|----------|
| Image1 | ... | ... | 用户已有 / 需生成 |

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
- **先问用户产品图、卖点、痛点（以及市场/平台），再进入完整流水线。**
- Roles never cross boundaries.
- Final output must be copy-paste ready for Seedance 2.0.
- Even 搞怪离谱 must serve product 卖点/痛点 contrast, and must be extreme enough (别人的不行 → 我们的夸张超强).
- 反差/剧情反转 must be exaggerated, not mild.
- Target market and platform must be stated; defaults applied and noted if unspecified.
- Prefer 4–15s. Keep total reference files ≤12.
- No realistic human faces in reference instructions.
- Every @ reference must state its exact purpose.
- 卖点/痛点标注来源：`[用户提供]` / `[网上研究]` / `[推断]`。

## Quick Start
User: “一次性马桶刷 搞怪离谱”  
→ Agent 先问：有哪些产品图？卖点？痛点？目标市场和平台？  
→ 用户回答后（可结合网上研究）  
→ Run roles 1→5  
→ Emit complete Seedance Asset Package that explicitly shows 目标市场 + 目标平台 + 来源标注。
