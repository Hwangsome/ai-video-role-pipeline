---
name: ai-video-role-pipeline
description: Multi-type AI video creation workflow with 5 non-overlapping roles that outputs ready-to-paste Seedance 2.0 image-to-video assets including exact @Image references, first-frame assignments, and full multimodal prompts. Requires or extracts product selling points and user pain points so the video clearly shows benefit and problem. Use for product showcase, lifestyle seeding, talking-head, absurd comedy, plot twist, ASMR, mockumentary. Triggers on Seedance prompt pipeline, video role design, multi-type short video production.
---

# AI Video Role Pipeline (Seedance 2.0 Ready)

Produce complete, copy-paste-ready assets for Jimeng / Seedance 2.0 multimodal video generation. Final deliverable is a **Seedance Asset Package** that the user can upload images into and paste the prompt directly.

## Core Goal

Every run must end with assets that work immediately in Seedance 2.0:
- Clear list of required images with exact labels and roles
- Exact @Image / @Video / @Audio assignments
- Full production prompt using correct @ syntax
- Duration, audio guidance, and parameter suggestions
- **Product selling points (卖点) and user pain points (痛点) are explicitly woven into the narrative** so the video is not just entertainment but shows why the product matters

## Input Handling (important)

When the user provides:
- **Only product name / description** → Content Strategist must ask for or reasonably infer 1–3 core 卖点 + corresponding 用户痛点
- **Product images** → Visual role + Strategist should extract visual + functional selling points from the images (appearance, material, usage, packaging cues)
- **Explicit 卖点 / 痛点 list** → Use them directly and force the narrative to demonstrate them

Never create a pure “funny for funny’s sake” video. Even 搞怪离谱 must have the absurdity serve a clear product benefit or pain-point contrast.

## Seedance 2.0 Hard Constraints (always respect)

| Input | Limit | Notes |
|-------|-------|-------|
| Images | ≤ 9 | jpeg/png/webp, <30MB each |
| Videos | ≤ 3 | mp4/mov, total 2–15s |
| Audio | ≤ 3 | mp3/wav, total ≤15s |
| Total files | ≤ 12 | prioritize highest-impact assets |
| Duration | 4–15s | match prompt complexity to length |
| Faces | No realistic human faces in uploaded refs | system blocks them |

### @ Reference Syntax (mandatory)

Always assign a clear purpose to every reference:

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
**Goal**: Lock content type + extract/confirm 卖点 & 痛点 + produce `concept_brief.md`.

Required fields:
- 视频类型
- 核心概念（一句话，必须包含产品如何解决痛点或展示卖点）
- 用户痛点（1–3个具体痛点）
- 核心卖点（1–3个，对应痛点）
- 情绪关键词
- 目标受众
- 时长目标
- 风格标签
- 特殊要求
- 推荐参考素材类型

**Rule**: If 卖点/痛点 missing, either ask the user or make a reasonable product-based inference and mark it as `[推断]`. The core concept must show the product solving a pain or highlighting a benefit.

**Stop**: Brief complete → hand only the brief.

### 2. Narrative & Shot Director
**Goal**: Type-adapted `shot_list.md` that forces the 卖点/痛点 into the structure.

- 产品展示 → 痛点场景 → 产品出现 → 卖点演示 → 结果
- 生活种草 → 日常痛点瞬间 → 自然使用 → 轻松解决
- 人物口播 → 先说痛点 → 再展示卖点证据
- 搞怪离谱 → 用夸张方式放大痛点，再用产品（或产品特性）荒诞地“解决”，最后回归真实卖点
- 剧情反转 → 前期痛点铺垫 → 反转时产品卖点成为关键解决力量
- ASMR → 通过感官细节强化产品质感卖点
- 伪纪录 → 真实观察痛点 → 采访中自然露出卖点

Each shot must note which 痛点 or 卖点 it serves.

**Stop**: Shot list complete → hand shot_list + brief.

### 3. Visual & Persona Reference Designer
**Goal**: Exact image requirements + `ref_map.md` that support both story and product proof.

Prioritize:
- Product hero + detail shots that prove the 卖点 (material, cleanliness, one-time use, packaging…)
- Before/after or pain-point visual cues when relevant
- Action references that make the benefit visible

**Stop**: ref_map clear → hand upstream.

### 4. Seedance Multi-Type Prompt Engineer
**Goal**: Production-ready prompt with correct @ syntax that visibly demonstrates 卖点 and contrasts 痛点.

Must include:
- Full ready-to-paste prompt
- Explicit @Image role assignments
- Time-segmented action if >8s
- Camera language
- Native audio direction
- Clear visual proof of the core 卖点 inside the action
- Recommended parameters

**Stop**: Prompt self-checked → hand final package.

### 5. Generation & Type-QA Specialist
**Goal**: Final **Seedance Asset Package** + type-specific QA that also checks product relevance.

**Final Deliverable Format (mandatory)**:

```markdown
# Seedance 2.0 Asset Package

## 0. Product Insight Summary
- 用户痛点：
- 核心卖点：
- 本视频如何体现：

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

## Hard Rules
- Roles never cross boundaries.
- Final output must be copy-paste ready for Seedance 2.0.
- Even 搞怪离谱 must serve product 卖点/痛点 contrast.
- Prefer 4–15s. Keep total reference files ≤12.
- No realistic human faces in reference instructions.
- Every @ reference must state its exact purpose.

## Quick Start
User provides product + type (and optionally images or 卖点 list)  
→ Run roles 1→5  
→ Emit the complete Seedance Asset Package with insight summary.
