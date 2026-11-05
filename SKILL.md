---
name: ai-video-role-pipeline
description: Multi-type AI video creation workflow using 5 non-overlapping roles for Seedance 2.0. Use when user wants product showcase, lifestyle seeding, talking-head, absurd comedy, plot twist, ASMR sensory, or mockumentary interview videos. Triggers on video role design, Seedance prompt pipeline, multi-type short video production.
---

# AI Video Role Pipeline

Design and execute short-form videos for Seedance 2.0 across seven content types using five strictly non-overlapping roles.

## Supported Content Types

- 产品展示 (product showcase)
- 生活种草 (lifestyle seeding)
- 人物口播 (talking-head / oral broadcast)
- 搞怪离谱 (absurd comedy)
- 剧情反转 (plot twist)
- 感官氛围 / ASMR (sensory / ASMR)
- 伪纪录 / 采访 (mockumentary / interview)

## Role Contracts (execute in order)

### 1. Content Strategist
- Lock the content type and produce `concept_brief.md`.
- Must include fields: 视频类型, 核心概念, 情绪关键词, 目标受众, 时长目标, 风格标签, 关键信息/卖点, 特殊要求.
- Stop when brief is complete. Hand off only the brief.

### 2. Narrative & Shot Director
- Convert brief into type-adapted `shot_list.md`.
- Structure must match type (e.g. 铺垫→爆发→反应 for 搞怪离谱; 功能演示流 for 产品展示; 声音驱动特写序列 for ASMR).
- Each shot lists duration, description, camera, emotion, audio note, reference needs.
- Stop when shot list is complete. Hand off shot list + brief.

### 3. Visual & Persona Reference Designer
- Produce `reference_pack/` (max 9 images) and `ref_map.md`.
- Prioritize consistency for people (talking-head, interview) or product states (showcase, seeding).
- For absurd comedy prepare exaggerated expression/action refs; for ASMR prepare macro texture/hand refs.
- Stop when pack and map are ready. Hand off everything upstream.

### 4. Seedance Multi-Type Prompt Engineer
- Translate shot list + refs into production-ready `seedance_prompts.md`.
- Use type-specific templates (clean commercial for product, wild exaggerated for absurd, lip-sync dialogue for talking-head, sound-first for ASMR, observational handheld for mockumentary).
- Always include correct [ImageN] tags, camera language, native-audio description, and parameter suggestions (duration, resolution, audio on, reference mode).
- Stop when prompts are complete and self-checked. Hand off prompts + all upstream files.

### 5. Generation & Type-QA Specialist
- Execute on Seedance 2.0 (or compatible platform) using the prompts and references.
- Run type-specific QA checklist (laugh landing for absurd, lip-sync for talking-head, sound layers for ASMR, etc.).
- Output final video file + `qa_report.md`.
- Stop at quality pass or max iteration limit. Deliver to user.

## Hard Rules
- Roles never cross boundaries. No role may rewrite upstream artifacts except by explicit hand-back.
- Prefer 4–15 s clips. Keep total under Seedance 2.0 practical limits.
- Always produce the named markdown files so the next role can consume them directly.
- Final deliverable is a Seedance-ready prompt package plus optional generated video.

## Quick Start
User says the content type + subject (e.g. "搞怪离谱 一次性马桶刷").  
Execute roles 1→5 in sequence and emit each contract output.
