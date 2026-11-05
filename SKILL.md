---
name: ai-video-role-pipeline
description: Multi-type AI video creation workflow with 5 non-overlapping roles that outputs ready-to-paste Seedance 2.0 image-to-video assets including exact @Image references, first-frame assignments, and full multimodal prompts. Requires or extracts product selling points and user pain points so the video clearly shows benefit and problem. Supports web search and short-video platform research for real creative references. Use for product showcase, lifestyle seeding, talking-head, absurd comedy, plot twist, ASMR, mockumentary. Triggers on Seedance prompt pipeline, video role design, multi-type short video production.
---

# AI Video Role Pipeline (Seedance 2.0 Ready)

Produce complete, copy-paste-ready assets for Jimeng / Seedance 2.0 multimodal video generation. Final deliverable is a **Seedance Asset Package**.

## Core Goal

Every run must end with assets that work immediately in Seedance 2.0:
- Clear list of required images with exact labels and roles
- Exact @Image / @Video / @Audio assignments
- Full production prompt using correct @ syntax
- **Product selling points (卖点) and user pain points (痛点) are explicitly woven into the narrative**
- Creative ideas are informed by real short-video references when possible

## Research Step (before or inside Content Strategist)

When 卖点 / 痛点 / 创意方向不足时，先做研究：

1. Run the helper script to get targeted search queries:
   ```bash
   python scripts/research_creatives.py "产品名" --type 搞怪离谱
   # or without --type for all types
   ```

2. Use the returned queries with `web_search` and/or `x_keyword_search` (and platform-specific operators) to collect:
   - Real user pain points and complaints
   - Common selling points / recommendation reasons
   - Existing creative approaches on Douyin / TikTok / Xiaohongshu for the same product + type
   - Visual, pacing, or twist techniques worth borrowing (without copying)

3. Summarize findings with:
   ```bash
   python scripts/format_insight.py --pain "..." --benefit "..." --ideas "..." --how "..."
   ```

4. Feed the structured insight into `concept_brief.md`.

Never invent pain points or selling points when real signals are available. Mark inferred items as `[推断]`.

## Input Handling

- Only product name → research + infer 卖点/痛点
- Product images provided → extract visual + functional selling points from images, then research
- User gives explicit 卖点/痛点 list → use directly, still optionally research for creative differentiation

Even 搞怪离谱 must serve a clear product benefit or pain-point contrast. Pure random absurdity is not allowed.

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
**Goal**: Lock content type + extract/confirm 卖点 & 痛点 (via research if needed) + produce `concept_brief.md`.

Required fields:
- 视频类型
- 核心概念（必须体现产品如何解决痛点或展示卖点）
- 用户痛点（1–3个）
- 核心卖点（1–3个，对应痛点）
- 情绪关键词 / 目标受众 / 时长目标 / 风格标签
- 特殊要求
- 推荐参考素材类型
- （可选）研究来源摘要

**Stop**: Brief complete → hand only the brief.

### 2. Narrative & Shot Director
**Goal**: Type-adapted `shot_list.md` that forces 痛点 → 卖点 demonstration into the structure.

Structure guidance:
- 产品展示 → 痛点场景 → 产品出现 → 卖点演示 → 结果
- 生活种草 → 日常痛点瞬间 → 自然使用 → 轻松解决
- 人物口播 → 先说痛点 → 再展示卖点证据
- 搞怪离谱 → 夸张放大痛点 → 用产品特性荒诞“解决” → 回归真实卖点
- 剧情反转 → 痛点铺垫 → 反转时卖点成为关键力量
- ASMR → 感官细节强化产品质感卖点
- 伪纪录 → 观察痛点 → 自然露出卖点

Each shot notes which 痛点 or 卖点 it serves.

**Stop**: Shot list complete → hand shot_list + brief.

### 3. Visual & Persona Reference Designer
**Goal**: Exact image requirements + `ref_map.md` supporting both story and product proof (detail shots that prove 卖点).

**Stop**: ref_map clear → hand upstream.

### 4. Seedance Multi-Type Prompt Engineer
**Goal**: Production-ready prompt with correct @ syntax that visibly demonstrates 卖点 and contrasts 痛点.

Must include full ready-to-paste prompt, explicit @ roles, time segments if needed, camera, audio, parameters.

**Stop**: Prompt self-checked → hand final package.

### 5. Generation & Type-QA Specialist
**Goal**: Final **Seedance Asset Package** + QA that checks product relevance.

**Final Deliverable Format (mandatory)**:

```markdown
# Seedance 2.0 Asset Package

## 0. Product Insight Summary
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
[full prompt with @Image roles]
```

## 3. Generation Parameters
- Duration / Resolution / Generate audio / Mode

## 4. Type-Specific + Product QA Checklist
- [ ] 痛点是否被清晰感知
- [ ] 卖点是否被动作或画面证明
- [ ] 产品始终可识别
- [ ] ...
```

**Stop**: Package complete → deliver to user.

## Scripts

| Script | Purpose |
|--------|--------|
| `scripts/research_creatives.py` | Generate targeted web/X search queries for a product + type across Douyin / TikTok / Xiaohongshu style sources |
| `scripts/format_insight.py` | Format collected 痛点 / 卖点 / 创意方向 into clean markdown for the brief and Asset Package |

## Hard Rules
- Roles never cross boundaries.
- Final output must be copy-paste ready for Seedance 2.0.
- Even 搞怪离谱 must serve product 卖点/痛点 contrast.
- Prefer 4–15s. Keep total reference files ≤12.
- No realistic human faces in reference instructions.
- Every @ reference must state its exact purpose.
- Research when 卖点/创意信号不足；标记推断内容。

## Quick Start
User provides product + type (and optionally images or 卖点 list)  
→ (Optional) Run research scripts + web_search / x_keyword_search  
→ Run roles 1→5  
→ Emit the complete Seedance Asset Package with insight summary.
