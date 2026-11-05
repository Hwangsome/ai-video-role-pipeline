---
name: ai-video-role-pipeline
description: Multi-type AI video creation workflow with 5 non-overlapping roles that outputs ready-to-paste Seedance 2.0 image-to-video assets including exact @Image references, first-frame assignments, and full multimodal prompts. Use for product showcase, lifestyle seeding, talking-head, absurd comedy, plot twist, ASMR, mockumentary. Triggers on Seedance prompt pipeline, video role design, multi-type short video production.
---

# AI Video Role Pipeline (Seedance 2.0 Ready)

Produce complete, copy-paste-ready assets for Jimeng / Seedance 2.0 multimodal video generation. Final deliverable is a **Seedance Asset Package** that the user can upload images into and paste the prompt directly.

## Core Goal

Every run must end with assets that work immediately in Seedance 2.0:
- Clear list of required images with exact filenames / labels
- Exact role for each image (`@Image1 as first frame`, `character reference @Image2`, etc.)
- Full production prompt using correct @ syntax
- Duration, aspect, audio guidance, and parameter suggestions
- Type-specific structure (产品展示 / 生活种草 / 人物口播 / 搞怪离谱 / 剧情反转 / ASMR / 伪纪录)

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

Never leave a reference without a role. Prefer explicit Chinese or English role statements.

## Five Non-Overlapping Roles (execute in strict order)

### 1. Content Strategist
**Goal**: Lock content type + produce `concept_brief.md`.

Required fields:
- 视频类型 (one of the 7 supported)
- 核心概念 (one sentence)
- 情绪关键词 (3)
- 目标受众
- 时长目标 (seconds)
- 风格标签
- 关键信息/卖点
- 特殊要求
- 推荐参考素材类型 (what images will be needed)

**Stop**: Brief complete → hand only the brief to next role.

### 2. Narrative & Shot Director
**Goal**: Type-adapted `shot_list.md` with timed segments.

Structure must match type:
- 产品展示 → 展示 → 使用 → 结果
- 生活种草 → 日常植入流
- 人物口播 → 说话镜头 + 关键画面
- 搞怪离谱 → 铺垫 → 爆发 → 反应
- 剧情反转 → 铺垫 → 反转点 → 新现实
- ASMR → 声音驱动特写序列
- 伪纪录 → 观察 + 访谈交替

Each shot must list: duration, 画面描述, 运镜, 情绪, 音频备注, 需要的参考图类型.

**Stop**: Shot list complete and total duration feasible → hand shot_list + brief.

### 3. Visual & Persona Reference Designer
**Goal**: Produce exact image requirements and `ref_map.md`.

Output:
- Numbered list of required images (Image1 … ImageN, N≤9)
- For each: purpose, description of what the image should contain, recommended style
- Explicit assignment examples (`@Image1 as first frame`, `character consistency @Image2` …)

**Stop**: ref_map clear and consistent → hand pack description + map + upstream.

### 4. Seedance Multi-Type Prompt Engineer
**Goal**: Write production-ready prompt(s) using correct @ syntax and type template.

Must include:
- Full prompt text ready to paste
- Exact @Image / @Video / @Audio assignments with roles
- Time-segmented description if >8s
- Camera language
- Native audio / SFX / BGM direction
- Style & quality modifiers
- Recommended parameters (duration, resolution, generate_audio=true, mode)

**Stop**: Prompt self-checked against Seedance constraints → hand final package.

### 5. Generation & Type-QA Specialist
**Goal**: Package everything into final Seedance Asset Package and run type-specific QA checklist.

**Final Deliverable Format (must output this structure)**:

```markdown
# Seedance 2.0 Asset Package

## 1. Required Images (upload these in order)
| Label | Purpose | Description of image content |
|-------|---------|------------------------------|
| Image1 | first frame / character | ... |
| Image2 | product detail | ... |
| ... | ... | ... |

## 2. Ready-to-Paste Prompt
```
[full prompt with @Image1 as ..., @Image2's character as subject, ...]
```

## 3. Generation Parameters
- Duration: Xs
- Resolution: 1080p / 4K preferred
- Generate audio: true
- Mode: References / Image-to-video / Full multimodal

## 4. Type-Specific QA Checklist
- [ ] ...
```

**Stop**: Package complete and QA items listed → deliver to user.

## Type Templates (load from references/type-templates.md)

Always adapt the prompt skeleton to the locked content type. Prefer time-segmented writing for clarity.

## Hard Rules
- Roles never rewrite upstream artifacts except by explicit hand-back.
- Final output must be copy-paste ready for Seedance 2.0 (images + prompt + params).
- Prefer 4–15s. Keep total reference files ≤12.
- No realistic human faces in reference instructions.
- Every @ reference must state its exact purpose.

## Quick Start
User: “搞怪离谱 一次性马桶刷” or “产品展示 + 这个商品图”
→ Run roles 1→5 sequentially and emit the final Seedance Asset Package.
