---
name: ai-video-role-pipeline
description: Multi-type AI video creation workflow with 5 non-overlapping roles that outputs ready-to-paste prompts for both Seedance 2.0 (@Image references) and MiniMax H3 (official T2VA/I2VA/FL2VA/L2VA/Ref2VA grammar). First asks user for product images, selling points and pain points (then combines with web research). Supports target market/country, platform, and target model selection for culturally, platform- and model-matched output. Use for product showcase, lifestyle seeding, talking-head, absurd comedy, plot twist, ASMR, mockumentary. Triggers on Seedance prompt pipeline, MiniMax H3 prompt, video role design, multi-type short video production.
---

# AI Video Role Pipeline (Seedance 2.0 + MiniMax H3 Ready)

Produce complete, copy-paste-ready assets for multimodal video generation — **Seedance 2.0 / 即梦**（`@Image` 语法）或 **MiniMax H3**（官方 `integrated_multimodal_description` / `subject_definitions` 语法）。最终交付物是 **Asset Package**，两种模型各有对应版本。

## Core Goal

Every run must end with assets that work immediately in the target model:
- Clear list of required images with exact labels and roles
- Exact reference assignments：Seedance 用 `@Image` / `@Video` / `@Audio`；H3 用 `<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>`
- Full production prompt in the correct grammar for that model
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

5. **目标模型（决定提示词语法）**
   - Seedance 2.0 / 即梦 → `@Image` 语法
   - MiniMax H3 → 官方 Base（T2VA/I2VA/FL2VA/L2VA）或 Ref2VA 六段式
   - 不确定时说「两个都要」，同时产出两版提示词（同一分镜，两套语法）

然后：
- 用户已提供的卖点/痛点 → 优先采用
- 用户说「不确定」或只给了部分 → 用 `scripts/research_creatives.py` + web_search / x_keyword_search 补充
- 最终在 concept_brief 和 Asset Package 里标注来源：`[用户提供]` / `[网上研究]` / `[推断]`

**不要在用户还没回答产品图、卖点、痛点之前就直接输出完整分镜和提示词。**

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

## MiniMax H3 Runtime Facts（2026-08-29 校验）

| 项 | 值 |
|----|-----|
| 输出时长 | 4–15s（不存在统一 10 秒上限） |
| 帧率 / 音频 | 24 FPS / 立体声 32 kHz |
| 分辨率 | 基础短边默认 768 px；2K 属 H3-Regenerate-2K |
| Ref2VA 素材 | 图片 ≤ 9、视频 ≤ 3（单段 2–15s，总 ≤15s）、音频 ≤ 3（单段 2–15s，总 ≤15s）、混合文件 ≤ 12 |
| 模式 | Base：T2VA / I2VA / FL2VA / L2VA；全参考：Ref2VA |

### @ Reference Syntax (mandatory for Seedance 2.0)

```
@Image1 as the first frame
@Image2's character as the subject
scene references @Image3
product details reference @Image4
reference @Video1's camera movement and action
BGM references @Audio1
```

### H3 Reference Labels (mandatory for MiniMax H3)

```
<Subject N>  reusable visible content (person / product / prop / environment)
<Picture N>  concrete frame anchor (first frame / last frame / keyframe / storyboard)
<Video N>    edit source, continuation point, or whole-video temporal structure
<Audio N>    copied or referenced audio signal
```

详细语法（模式选择、六段式结构、retention 标记、对白 `<d>` 标签、运行时事实、`@Image`→H3 标签映射表、H3 专用 QA）见 [`references/h3-syntax.md`](references/h3-syntax.md)。**在写 H3 提示词前必读**，且官方语法优先级最高：任何本项目经验写法都不能说成官方要求。

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

### 4. Multi-Model Prompt Engineer
**Goal**: Production-ready prompt in the **target model's** grammar that demonstrates 卖点, contrasts 痛点, and matches target market + platform style.

**Seedance 2.0 branch**：`@Image` / `@Video` / `@Audio` 语法，写明每个引用的用途、时间段、运镜、音频、参数与市场/平台语气。

**MiniMax H3 branch**（先读 `references/h3-syntax.md`）：
1. 选模式：无图→T2VA；仅首帧→I2VA；首+尾帧→FL2VA；仅尾帧→L2VA；多张身份/场景/道具图（≤9）→Ref2VA
2. Base 家族写三段：`integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music`；首行按模式加官方对齐指令
3. Ref2VA 写六段且顺序不变：`subject_definitions` → `summary` → `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music`
4. 分镜表时间点改写成 `[Shot 1]`（无时间戳）+ `[Shot 2] At 00:03.000, ...`（严格递增、落在时长内）
5. 同一人物三视图合并为一个 `<Subject N>`；商品白底图建 `<Subject>` 并在定义里引 `<Picture>`
6. 对白用 `<d>[Language] 原文</d>` + 稳定 `(Sx)`；音效进 `overall_soundscape`，BGM 进 `non_diegetic_music`
7. 生成类 `detailed_description` 约 350–500 英文词

**Stop**: Prompt self-checked（含该模型的专用 QA）→ hand final package.

### 5. Generation & Type-QA Specialist
**Goal**: Final **Asset Package** + QA that checks product relevance, market/platform fit, and model-specific compliance.

**Final Deliverable Format (mandatory)** — 按目标模型选择其一：

```markdown
# Seedance 2.0 Asset Package

## 0. Product Insight Summary
- 目标市场：
- 目标平台：
- 目标模型：Seedance 2.0
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
```

```markdown
# H3 Asset Package

## 0. Product Insight Summary
（同上，但「目标模型」写 H3 模式，如 MiniMax H3 · Ref2VA）

## 1. Required Assets (upload these in order)
| Label | H3 标签 | Purpose | Description | 来源建议 |
|-------|---------|---------|-------------|----------|
| Image1 | <Picture 1> / <Subject 1> 内引 | ... | ... | 用户已有 / 需生成 |

## 2. Ready-to-Paste Prompt
```
[官方语法全文：Base 三段 或 Ref2VA 六段，段落名一字不差]
```

## 3. Generation Parameters
- Mode（T2VA/I2VA/FL2VA/L2VA/Ref2VA）/ Duration / Resolution / Audio

## 4. H3 QA Checklist
- [ ] 模式选对；官方段落名与顺序正确
- [ ] Subject 与 Picture 语义不混用；同一角色只一个 Subject ID
- [ ] `[Shot 1]` 无时间戳；后续时间严格递增且在时长内
- [ ] 多镜有因果桥；一镜一主导运镜
- [ ] 对白 `<d>[Language]` + 稳定 (Sx)；soundscape 不复述对白
- [ ] 卖点被动作证明、痛点被清晰感知、产品可识别
```

**Stop**: Package complete → deliver to user.

## Scripts

| Script | Purpose |
|--------|--------|
| `scripts/research_creatives.py` | Generate targeted web/X search queries for product + type + market + platform |
| `scripts/format_insight.py` | Format collected 痛点 / 卖点 / 创意方向 into clean markdown |

## Hard Rules
- **先问用户产品图、卖点、痛点（以及市场/平台、目标模型），再进入完整流水线。**
- Roles never cross boundaries.
- Final output must be copy-paste ready for the **target model**（Seedance 2.0 或 MiniMax H3）。
- H3 提示词必须严格使用官方语法：段落名、顺序、`[Shot N]` 时间戳、`<d>` 对白、retention 标记一律照官方；本项目经验写法不得冒称官方要求。
- Even 搞怪离谱 must serve product 卖点/痛点 contrast, and must be extreme enough (别人的不行 → 我们的夸张超强).
- 反差/剧情反转 must be exaggerated, not mild.
- Target market and platform must be stated; defaults applied and noted if unspecified.
- Prefer 4–15s（两个模型都支持）. Keep total reference files ≤12.
- Seedance：上传参考图不得含真实人脸（除非用户确认其通道允许授权人物图）。
- Every reference must state its exact purpose：Seedance 用 @ 标签，H3 用 `<Subject>/<Picture>` 定义。
- 卖点/痛点标注来源：`[用户提供]` / `[网上研究]` / `[推断]`。

## Quick Start
User: “一次性马桶刷 搞怪离谱”  
→ Agent 先问：有哪些产品图？卖点？痛点？目标市场和平台？目标模型（Seedance / H3）？  
→ 用户回答后（可结合网上研究）  
→ Run roles 1→5  
→ Emit complete Asset Package（Seedance 版 `@Image` 提示词 或 H3 版官方语法提示词），明确标注 目标市场 + 目标平台 + 目标模型 + 来源标注。  
→ 若用户要「两个都要」：同一分镜出两套提示词，分两个文件/两节，不混用语法。

## References

| File | When to read |
|------|--------------|
| `references/h3-syntax.md` | 写 MiniMax H3 提示词前必读（模式选择、六段式、标签映射、H3 QA） |
| `references/seedance-syntax.md` | Seedance 2.0 `@` 语法与限制细节 |
| `references/type-templates.md` | 七种内容类型的时间轴模板 |
| `references/role-contracts.md` | 五角色交付契约与接力规则 |
