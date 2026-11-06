# MiniMax H3 Prompt Syntax（Seedance 之外的第二目标模型）

> 来源：MiniMax H3 官方 Video Prompt Writing Guide（T2VA/I2VA/FL2VA/L2VA）与 Full-Reference Mode Rewrite Output Format Guide，经 AIKSK H3 规范（aiksk-minimax-h3-local-prompt v1.8.1）生产层整理。
> **优先级**：官方语法 > 素材真实情况 > 用户硬约束 > 本项目生产经验。任何本文档中的经验写法都不许说成"官方要求"。

## 0. 先选模式（Mode Routing）

| 素材情况 | H3 模式 | 首行要求 |
|----------|---------|----------|
| 纯文本 | `T2VA` | 无对齐指令，直接三个核心字段 |
| 首帧图 + 文本 | `I2VA` | 固定首行 `For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.` |
| 首帧 + 尾帧 + 文本 | `FL2VA` | 固定首行 `How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.` |
| 仅尾帧 + 文本 | `L2VA` | 固定首行 `How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.` |
| 多张身份/场景/道具参考图（≤9 图、≤3 视频、≤3 音频） | `Ref2VA` | 六段式结构，见第 2 节 |

S.SS 用两位小数表示**实际生效时长**；若工作流把时长吸附到合法帧率网格，用生效时长而不是用户口头值。

## 1. Base 家族：三段式

```text
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: ...
```

字段名不可改。`[Shot 1]` 不带时间戳；`[Shot 2+]` 用 `[Shot 2] At 00:03.500, the camera cuts to ...`，时间严格递增且落在成片时长内。

- **风格开场**：在 `[Shot 1]` 开头一句话交代整体风格与初始构图（`Live-action, cinematic, ...` / `2D-animated` / `3D CG` 等）
- **镜头词表**：`Static Shot` `Push In / Pull Out` `Zoom In / Zoom Out` `Pan Left/Right` `Truck Left/Right` `Tilt Up/Down` `Pedestal Up/Down` `Arc Shot` `Tracking Shot` `Shake Slightly/Strongly` `POV` `Roll Clockwise/Counterclockwise`；幅度 `with small/large amplitude`、速度 `at slow/fast speed` 只在有意义时加
- **I2VA**：首帧锚点 → 动作起始 → 连续发展 → 结果或反应
- **FL2VA**：首帧状态 → 中间可观察变化 → 差异收窄 → 尾帧落点；通常单镜不切
- **L2VA**：可信前置状态 → 动作与过渡路径 → 末镜逐步收敛 → 落尾帧

## 2. Ref2VA：六段式（顺序不可变）

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

### 2.1 subject_definitions
- `<Subject N>`：可复用的可见内容（人/动物/商品/场景/服装/风格）。多个素材指向同一对象时合并：
  `<Subject 1> is the same woman whose identity is established by <Picture 1>, <Picture 2>, and <Picture 3>.`
- `<Picture N>`：只有当图片本身是首帧/尾帧/关键帧/构图或分镜锚点时才单独列条；仅提供身份/服装/道具信息的图，写进对应 Subject 定义里
- `<Video N>`：剪辑源 / 续写起点 / 整片时间结构
- `<Audio N>`：音频信号复用或参考；绑定具体说话人时复用其全局 `(Sx)`：`<Audio 1> is the voice-timbre reference for <Subject 1> (S1).`
- **`subject_definitions` 之后不许再引入新标签**

### 2.2 summary
以方括号任务类型开头，多类型用 ` + ` 连接且不重复：
`keyframe completion` / `reference generation` / `video editing` / `video continuation` / `audio reuse` / `audio reference`。
真正的视频剪辑，任务前缀后接：`The target video is an edited version of <Video 1>.`

### 2.3 retention_analysis
每个被追踪标签一行，标记为固定英文值：
- 可见内容：`fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference`
- 音频：`fully_copy` / `partially_copy` / `reference` / `weak_reference`

格式：`<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...`

### 2.4 detailed_description
- 英文正文；对白/歌词/画面内文字保留原语言
- **`[Shot 1]` 之前**先用 1–2 句英文确立整体风格
- 生成类任务通常 **350–500 英文词**；对白密集时优先保证完整口播时间线
- 镜头内自然引用标签：`the shot begins from <Picture 1>`、`the shot ends on <Picture 3>`

### 2.5-2.6 两个声音字段
- `overall_soundscape`：全片环境声 + 物理动作声 + 非语言人声，1–4 句，**不复述对白**；完全静音才写 `N/A`
- `non_diegetic_music`：只有观众听得到的配乐，写器乐/速度/节奏/动态，不用抽象情绪词；没有则 `N/A`

## 3. 对白与画面文字

```text
The woman (S1) says: <d>[Chinese] 原台词。</d>
```
- `<d>` 内只放语言标签 + 实际口播内容，逐字保留原话和标点
- 旁白用固定短语 `says in an off-screen voiceover`，并紧跟一句说明对应角色嘴唇保持闭合
- 跨镜头台词：两端都用 `<scenetrans>` 并说明音频连续；被结尾截断用 `<cutoff>`
- 画面内可见文字用英文双引号原样包裹：`A red neon sign reading "营业中" glows above the doorway.`

## 4. H3 运行时事实（2026-08-29 校验）

- 输出时长 4–15 秒；24 FPS；立体声 32 kHz
- 基础生成短边默认 768 px；2K 属于 H3-Regenerate-2K
- Ref2VA：图片 ≤ 9、视频 ≤ 3（单段 2–15s、总时长 ≤15s）、音频 ≤ 3（单段 2–15s、总≤15s）、混合文件 ≤ 12
- 不存在"统一 10 秒上限"这种说法

## 5. 本项目 @Image 语法 → H3 标签映射

| 本项目（Seedance） | H3 写法 | 转换规则 |
|-------------------|---------|----------|
| `@Image1 as the first frame` | `I2VA` 首行 + `<Picture 1>` | 首帧图走 I2VA/FL2VA，不建成 Subject |
| `@Image1's product as the subject` | `<Subject 1>` 商品身份，内部引 `<Picture 1>` | 只提供身份/外观的图，写入 Subject 定义 |
| 人物三视图（正/侧/背） | 一个 `<Subject N>`，定义中引三张图 | 同一角色绝不拆成多个 Subject |
| `@Image4 product details reference` | `<Subject 1>` 中的外观特征描述，或独立 `<Picture 4>`（当它是关键帧） | 看它是"证据图"还是"帧锚点" |
| 旧刷对比图（反派道具） | `<Subject 2>` 道具身份 | 与主商品分开编号 |
| `@Video1's camera movement` | `<Video 1>` 整片结构/运镜参考 | 仅参考运镜时 summary 用 `reference generation`，不是 `video editing` |
| `@Audio1` BGM | `<Audio 1>` + `audio reference` | 只借风格/音色，不搬原声 |

## 6. 分镜 → H3 时间轴改写要点

- 分镜表里的"0–3s / 3–6s / 9–12s"→ `[Shot 1]` 无时间戳，后续 `At 00:03.000,` `At 00:06.000,` `At 00:09.000,`
- 每个切点必须带来新信息（主体/空间/状态/视角/时间）；只变景别就改用推拉运镜
- 多镜叙事要有因果桥：身体动作 / 视线 / 道具接触 / 动势方向 / 声音提示 / 镜头方向 / 可见状态变化
- 一镜只给一个主导运镜，禁止堆叠装饰性运镜
- 中文分镜文案里的音效提示（"咔哒""唰唰唰"）落在 `overall_soundscape` 的动作声里；BGM 落在 `non_diegetic_music`

## 7. 交付前 QA（H3 专用）

1. Base 还是 Ref2VA 家族选对
2. 官方字段名/段落名一字不差、顺序正确
3. 素材编号与实际上传一致
4. Subject 与 Picture 语义不混用；同一角色只有一个 Subject ID
5. `subject_definitions` 之后没有新标签
6. summary 任务类型与素材角色相符
7. retention 标记是官方值且与角色匹配
8. `[Shot 1]` 无时间戳；后续时间严格递增且在时长内
9. 多镜有因果桥；运镜不过载
10. 对白用稳定 `(Sx)` + `<d>[Language]`；soundscape 不复述对白
11. 生成类 detailed_description 约 350–500 词
12. 没有把本项目经验写成"官方要求"

## 8. 常见故障修复

| 现象 | 修复 |
|------|------|
| 人物换脸/漂移 | 同一角色合并到一个 `<Subject N>`，把全部身份图写进定义，重要出场重复标签不重定义 |
| 三张图幻灯片感 | 建可复用 Subject + 给每张图明确叙事角色 + 补跨切点因果桥 |
| 动作软 | 把抽象意图换成物理动作与落点（方向/接触/反作用/终点） |
| 运镜乱 | 一镜一主导运镜，删装饰性堆叠 |
| 对白赶/被切 | 说话段降视觉复杂度，切点放自然停顿，非授权不改台词 |
| 商品变形 | 几何/材质/logo/文字升级为硬连续性约束，减少涉及商品的变换 |
