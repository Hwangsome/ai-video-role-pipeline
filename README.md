# AI Video Role Pipeline

把一个商品变成能直接粘贴进生成平台的完整资产包：五个不重叠的编导角色、真实的痛点与卖点、明确的参考素材分工。**同时支持 Seedance 2.0（即梦）`@Image` 语法与 MiniMax H3 官方语法（T2VA/I2VA/FL2VA/L2VA/Ref2VA）**。

`ai-video-role-pipeline` 是一个面向电商 AI 视频生产的 Agent Skill。它不是"写一段提示词"，而是一条流水线：先向用户收齐产品图、卖点、痛点、目标市场与目标模型，再按五个角色的顺序把创意一路推到可直接上传生成的 **Asset Package**。

仓库同时收录配套技能 **`ecom-product-asset-gen`**：从产品演示视频生成与视频同款一致的产品资产图（三视图 / 细节图 / 场景图）、去除生成平台水印，并从画面提炼卖点痛点洞察——正好补上流水线 Step 0 "产品图不够、卖点痛点靠脑补" 和 Step 3 参考图来源这两个缺口。

[快速开始](#快速开始) · [支持的内容类型](#同一商品可以拍成什么) · [目标模型](#目标模型seedance-20-与-minimax-h3) · [工作流程](#它怎么工作) · [交付物](#你会拿到什么) · [实际案例](#实际案例) · [配套技能](#配套技能产品资产图生成) · [技能入口](ai-video-role-pipeline/SKILL.md)

## 为什么做这个技能

AI 视频生成经常卡在几件事上：提示词写了一堆，生成出来产品却走形了；故事有趣，但和卖点没关系；角色每换一个镜头就换一张脸；最关键的卖点和痛点，靠模型自己"脑补"，结果全是套话。

这个技能用几条硬规则解决这些问题：

- **先问，再写**：Step 0 强制先向用户收产品图、卖点、痛点、目标市场与平台，不许直接输出分镜。
- **来源标注**：每个卖点和痛点都要标 `[用户提供]` / `[网上研究]` / `[推断]`，不把猜测伪装成事实。
- **产品锚定**：白底图 / 主图固定为 `@Image 的 product as the subject`，产品外观跨镜头不走形。
- **角色不越界**：五个角色按顺序接力，每个角色只交付自己的文件，不重写上游。
- **离谱要服务卖点**：搞怪、反转必须回到"痛点 → 卖点"的对比上，纯随机荒诞不允许。

## 快速开始

### 方式一：复制提示词，让 Agent 安装

```text
请帮我安装这个仓库中的 AI 视频角色流水线技能：
https://github.com/Hwangsome/ai-video-role-pipeline

需要安装的技能名称：ai-video-role-pipeline
仓库内的技能路径：ai-video-role-pipeline/

请先读取仓库 README 和 SKILL.md，再按当前 Agent 实际支持的技能安装方式，
安装完整文件夹，保留 references/ 与 scripts/，不要只复制 SKILL.md。
如果已有同名技能，请先比较版本、保留本地修改，再处理更新。
安装后告诉我实际安装位置、调用方法，以及是否需要刷新技能列表或开启新会话。
```

### 方式二：手动获取

```bash
git clone https://github.com/Hwangsome/ai-video-role-pipeline.git
```

将 `ai-video-role-pipeline/` 子文件夹放到你所用工具的技能目录（例如 WorkBuddy 用户级技能目录 `~/.workbuddy/skills/`），或让能读取本地文件的 Agent 直接按 [`SKILL.md`](ai-video-role-pipeline/SKILL.md) 执行。配套技能 `ecom-product-asset-gen/` 同样整体复制到技能目录即可。

主技能本体不依赖任何第三方包；`scripts/` 下的研究脚本只使用 Python 标准库（3.10+）。配套技能的 `extract_keyframes.py` 需要 ffmpeg 在 PATH 中，`remove_ai_watermark.py` 需要 numpy + opencv-python。

### 安装后，复制这段开始使用

```text
使用 ai-video-role-pipeline，给一次性马桶刷做一条视频。
```

技能会先走 Step 0，问你五件事：

1. 你有哪些产品图？（或需要我规划 + AI 生成补齐）
2. 卖点用你提供的，还是结合网上研究？
3. 痛点用你提供的，还是结合网上研究？
4. 目标市场 + 平台？（如 中国大陆+抖音 / 马来西亚+TikTok）
5. 目标模型？（Seedance 2.0 / MiniMax H3 / 两个都要）

回答后流水线自动跑完五个角色，产出完整资产包。也可以跳过提问直接给全量输入：

```text
产品图在 D:\资产\图片\；卖点：自带清洁液、一键抛头、不脏手；
痛点：旧刷子洗不净发臭；市场马来西亚，平台 TikTok，类型搞怪离谱；模型 H3，直接出稿。
```

## 同一商品可以拍成什么

| 内容类型 | 结构骨架 | 观众为什么看 |
|---|---|---|
| 产品展示 | 痛点场景 → 产品出现 → 卖点演示 → 结果 | 看操作、细节、质感与变化 |
| 生活种草 | 日常痛点瞬间 → 自然使用 → 轻松解决 | 代入一个具体生活时刻 |
| 人物口播 | 先说痛点 → 再展示卖点证据 | 听一个有态度的人讲明白 |
| 搞怪离谱 | **必须足够离谱**：别人的产品很惨 → 我们的夸张到开挂 → 冷静收尾 | 看荒诞反差怎么升级和收尾 |
| 剧情反转 | 痛点放大到崩溃 → 产品把效果夸张到"一次搞定/干净到反光" | 预期被大幅打破 |
| 感官氛围 / ASMR | 感官细节强化产品质感卖点 | 享受声音、动作和秩序 |
| 伪纪录 / 采访 | 观察痛点 → 自然露出卖点 | 看熟悉的严肃形式讲意外的事 |

目标市场决定幽默方式、节奏和文化梗：中国大陆偏快节奏强反差卡点，马来西亚/东南亚偏明亮热情生活化，美国偏口语和 irony。目标平台决定时长习惯和字幕密度。详见 [`references/type-templates.md`](ai-video-role-pipeline/references/type-templates.md) 与 SKILL.md 中的市场/平台配置。

## 目标模型：Seedance 2.0 与 MiniMax H3

同一套分镜可以输出两种模型的提示词，素材清单不变，语法层分别编译。

| 维度 | Seedance 2.0 / 即梦 | MiniMax H3 |
|------|---------------------|------------|
| 参考素材写法 | `@Image1 as the first frame`、`@Image2's character as the subject` | `<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>` |
| 提示词结构 | 单段多模态描述 + 生成参数 | Base 三段（`integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music`）或 Ref2VA 六段式 |
| 模式 | 图生视频 / 首尾帧 / 参考生 | T2VA / I2VA / FL2VA / L2VA / Ref2VA |
| 多图身份锚定 | 多张 `@Image` 直接挂参考 | 三视图合并为一个 `<Subject N>`，在其定义里引多张 `<Picture>` |
| 时间轴写法 | 提示词内写 0–3s / 3–6s | `[Shot 1]` 无时间戳，后续 `At 00:03.000, ...` |
| 时长 | 4–15s | 4–15s（不存在"统一 10 秒上限"这种说法） |
| 对白 | 自然语言描述口播 | `<d>[Language] 原文</d>` + 稳定 `(Sx)` |

H3 语法细节（mode routing、retention 标记、镜头词表、`@Image`→H3 标签映射表、H3 专用 QA 与故障修复）见 [`references/h3-syntax.md`](ai-video-role-pipeline/references/h3-syntax.md)。**官方语法优先级最高**：本项目沉淀的生产经验不会被包装成官方要求。

## 它怎么工作

```text
Step 0：向用户收产品图 / 卖点 / 痛点 / 市场+平台 / 目标模型
        ↓（不足的部分用 scripts/ + web_search 补研究）
1. Content Strategist        锁类型、市场、平台、卖点痛点 → concept_brief.md
        ↓
2. Narrative & Shot Director 按类型结构拆分镜，每镜标注服务的卖点 → shot_list.md
        ↓
3. Visual & Reference Designer  逐张定义参考图用途与来源 → ref_map.md
        ↓
4. Prompt Engineer（Seedance / H3）  按目标模型编译提示词并自检
        ↓
5. Generation & QA Specialist  汇总成 Asset Package（Seedance 或 H3 版）+ 分类型 QA
```

五个角色不越界：上游只交付文件，下游不重写上游结论。

### 硬约束（技能内置）

| 输入 | 限制 | 说明 |
|------|------|------|
| 图片 | ≤ 9 张 | jpeg/png/webp，单张 <30MB |
| 视频 | ≤ 3 段 | mp4/mov，总时长 2–15s |
| 音频 | ≤ 3 段 | mp3/wav，总时长 ≤15s |
| 总文件 | ≤ 12 | 优先放最有说服力的素材 |
| 成片时长 | 4–15s | 提示词复杂度与时长匹配 |
| 参考图 @ 语法 | 每个引用必须写明用途 | 如 `@Image4 作为细节参考` |
| **H3** 参考标签 | `<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>` | 同一角色只建一个 Subject |
| **H3** 段落结构 | Base 三段 或 Ref2VA 六段 | 段落名与顺序不可改 |
| **H3** 时间戳 | `[Shot 1]` 无时间戳，后续 `At 00:03.000, ...` | 严格递增且落在时长内 |

## 你会拿到什么

| 你提出的任务 | 对应交付 |
|---|---|
| "给 XX 商品做条视频" | Step 0 提问 → 完整 Asset Package（Seedance 或 H3） |
| "只给我提示词" | 目标模型语法的可粘贴提示词 + 生成参数 |
| "市场换成美国 / 平台换成小红书" | 研究查询、叙事节奏、字幕语言与风格全部重定向 |
| "帮我补一张对比道具图" | 图生图方案 + 存放路径 + 更新后的 ref_map |
| "生成出来人脸/产品走形了" | QA 定位 → 锚点调整方案（换参考图 / 改 @ 分工 / 降级为纯文生） |

最终交付固定为 **Asset Package**（Seedance 或 H3 版）：Insight Summary（含来源标注与目标模型）、参考素材清单（含上传顺序与 H3 标签映射）、可粘贴提示词、生成参数、分类型与模型专用 QA 清单。默认保存 Markdown；需要网页版交付物时可产出单文件 HTML（见实际案例）。

## 实际案例

### [一次性马桶刷 · 马来西亚 TikTok · 搞怪离谱](ai-video-role-pipeline/examples/01-disposable-toilet-brush-my-tiktok/index.html)

完整走完 Step 0 → 五角色的真实产出，包括：

- 用户提供 8 张产品图 + 卖点痛点文档 `[用户提供]`，缺的传统脏刷对比图用图生图补齐 `[AI 生成]`
- 研究结论：TikTok 马来清洁内容以 malas 自嘲钩子 + 口语化马来语字幕跑量 `[网上研究]`
- 创意《Toilet Brush Horror Story》：传统刷惨剧（缠发/甩水/臭味波浪）→ 蓝泡爆发开挂三连刷 → 一按落盒摊手炫耀 → 马来语字幕冷静收尾
- 9 张参考图打满上限：产品 5 张 + AI 脏刷 1 张 + 人物三视图 3 张（正面锁脸 / 侧面锁轮廓 / 背面锁头巾）
- **已按此资产包实际生成成片**：[generated-video.mp4](ai-video-role-pipeline/examples/01-disposable-toilet-brush-my-tiktok/generated-video.mp4)（15s · 9:16），「POWER UP ⚡」蓝泡爆发等关键时序与提示词一一对应
- 同一分镜另出 **MiniMax H3 Ref2VA 版提示词**（六段式官方结构，演示双模型编译）
- 配套单文件 HTML 交付物（含一键复制提示词 + 成片播放）：[examples/01-disposable-toilet-brush-my-tiktok/index.html](ai-video-role-pipeline/examples/01-disposable-toilet-brush-my-tiktok/index.html)

配套文档：[concept_brief.md](ai-video-role-pipeline/examples/01-disposable-toilet-brush-my-tiktok/concept_brief.md) · [shot_list.md](ai-video-role-pipeline/examples/01-disposable-toilet-brush-my-tiktok/shot_list.md) · [ref_map.md](ai-video-role-pipeline/examples/01-disposable-toilet-brush-my-tiktok/ref_map.md) · [Seedance_Asset_Package.md](ai-video-role-pipeline/examples/01-disposable-toilet-brush-my-tiktok/Seedance_Asset_Package.md) · [H3_Asset_Package.md](ai-video-role-pipeline/examples/01-disposable-toilet-brush-my-tiktok/H3_Asset_Package.md)

## 配套技能：产品资产图生成（ecom-product-asset-gen）

流水线经常卡在"产品图不够 / 角度不对 / 卖点痛点靠脑补 / 带着字幕水印"。这个配套技能从**一段产品演示视频**出发，产出两类资产，为流水线补齐输入：

```text
Step 1  ffmpeg 按秒抽帧 + 拼图快览 → 锁定正面 / 侧面 / 俯视 / 细节机位
Step 2  以视频原帧为参考图做图生图（高保真），重绘无字幕、无水印、
        产品结构同款一致的场景图 → 逐张对比验收
Step 3  形态学顶帽 + TELEA inpaint 去除右下角平台水印
Step 4  按 编号_类型_描述.png 归档进资产目录，附图↔时间点对照表
Step 5  从画面提炼 卖点痛点洞察（产品卖点与痛点.md）：产品定位 / 目标人群 /
        痛点清单含画面锚点 / 卖点矩阵含证据与时间点 / 卖点↔痛点对照 /
        三段式话术 / 不可宣称清单
```

实测踩坑都已内置：不传参考图会产品走形、cv2 读不了中文路径、灰底/白底低对比水印的降阈值策略与矩形修复兜底。

- 技能入口：[ecom-product-asset-gen/SKILL.md](ecom-product-asset-gen/SKILL.md)
- 洞察文档骨架：[references/insight-template.md](ecom-product-asset-gen/references/insight-template.md)
- 附带脚本（可独立使用）：
  - [`scripts/extract_keyframes.py`](ecom-product-asset-gen/scripts/extract_keyframes.py) — 视频抽帧 + contact sheet 拼图（仅需 ffmpeg）
  - [`scripts/remove_ai_watermark.py`](ecom-product-asset-gen/scripts/remove_ai_watermark.py) — 平台水印去除（需 Python 3.10+ / numpy / opencv-python，中文路径安全）

### 与流水线的衔接

- **Step 0 收集卖点痛点** → 用户给不出结构化卖点时，直接丢一段演示视频，本技能的洞察输出就是 `concept_brief.md` 的上游素材（来源标注规则与流水线一致：`[画面可见]` / `[用户提供]` / `[推断]`）
- Step 0 收集产品图时缺角度 → 用本技能从已有演示视频补齐三视图与细节图
- Step 3 ref_map 需要场景参考图 → 用本技能重绘"同款产品 + 新场景"的干净图，替代直接截帧（截帧带字幕水印且分辨率受限）
- 提醒：水印去除仅用于处理**自己拥有版权的生成结果或自有素材**，不用于规避他人内容的版权标识。

## 仓库结构

```text
ai-video-role-pipeline/                # 仓库根目录
├── README.md
├── ai-video-role-pipeline/            # 技能文件夹（整体安装这一层）
│   ├── SKILL.md                       # 唯一技能入口：Step 0 + 五角色流水线
│   ├── references/
│   │   ├── role-contracts.md          # 五角色的交付契约与接力规则
│   │   ├── seedance-syntax.md         # Seedance 2.0 @ 语法与硬约束
│   │   ├── h3-syntax.md               # MiniMax H3 官方语法（Base + Ref2VA 六段式 + 标签映射）
│   │   └── type-templates.md          # 七种内容类型的时间轴模板
│   ├── scripts/
│   │   ├── research_creatives.py      # 按商品+类型+市场+平台生成定向搜索查询
│   │   └── format_insight.py          # 把研究结论整理成结构化 Markdown
│   └── examples/
│       └── 01-disposable-toilet-brush-my-tiktok/
│           ├── index.html             # 单文件 HTML 交付物（可一键复制提示词）
│           ├── generated-video.mp4    # 实际生成成片（15s · 9:16）
│           ├── concept_brief.md
│           ├── shot_list.md
│           ├── ref_map.md
│           ├── Seedance_Asset_Package.md   # Seedance 2.0 @Image 版提示词
│           └── H3_Asset_Package.md         # MiniMax H3 Ref2VA 版提示词（同一分镜）
└── ecom-product-asset-gen/            # 配套技能：从演示视频生成产品资产图 + 卖点痛点洞察
    ├── SKILL.md                       # 抽帧审片 → 图生图重绘 → 去水印 → 归档 → 卖点痛点提炼
    ├── references/
    │   └── insight-template.md        # 卖点痛点洞察文档的输出骨架
    └── scripts/
        ├── extract_keyframes.py       # 视频抽帧 + contact sheet 拼图（ffmpeg）
        └── remove_ai_watermark.py     # 平台水印去除（顶帽 + inpaint，中文路径安全）
```

## 使用边界

技能用于电商 AI 视频的前期策划与生成资产制作；不操作投放账户，不代替完整影视编剧，也不自动提交生成任务。

商品功效必须有来源：演绎和特效不冒充实测，杀菌率、除菌率等量化结论没有检测报告就不能进台词。人物参考图使用前确认已获授权。生成结果依赖平台能力与模型版本，同一资产包在不同时间的生成效果可能有差异，上线前按 QA 清单人工复核。

## 参与改进

欢迎 Issue 和 Pull Request。最有帮助的反馈包括：商品类型、目标市场与平台、实际生成的资产包、生成成片与提示词的偏差位置。分享案例前去除品牌机密与个人信息。
