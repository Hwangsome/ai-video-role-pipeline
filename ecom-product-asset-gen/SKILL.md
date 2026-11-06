---
name: ecom-product-asset-gen
description: 从电商产品演示/带货视频生成与视频同款一致的产品资产图（三视图、细节图、场景图），并从视频画面提炼产品卖点痛点洞察，供 AI 图生视频使用。触发词：提取产品图、生成产品场景图、产品三视图、视频生成参考图、产品资产、去 AI 生成水印、图生图保持产品一致、提炼卖点痛点、产品洞察。覆盖：ffmpeg 抽帧审片、ImageGen 图生图保真参数、产品一致性校验、平台水印去除、卖点痛点提炼、资产归档。
agent_created: true
---

# Ecom Product Asset Gen

## Overview

把一段产品演示视频转化为两类资产：**可用于 AI 视频生成的干净产品资产图**（三视图 / 细节图 / 场景图）与**卖点痛点洞察文档**。图的核心不是截帧，而是以视频帧为参考重绘出无字幕、无水印、产品结构同款一致的高质量场景图；洞察则全部基于画面可验证的事实提炼，两类产出归档到同一产品目录。

## Workflow

### Step 0 — 明确需求与成本

- 与用户确认：产品是什么、需要哪些机位（默认：正面 / 侧面 45° / 俯视 / 全身立视 + 关键细节 + 1-2 个使用场景）。
- **必须先告知成本**：ImageGen 每张约消耗 5-10 积分，报出总预算（张数 × 5-10）再动手。

### Step 1 — 抽帧审片

用 `scripts/extract_keyframes.py` 对视频按秒抽帧并生成拼图（contact sheet），每张拼图含 25 帧，Read 一次即可审 25 个机位：

```bash
python extract_keyframes.py --video "视频.mp4" --out frames/          # 1fps 全量 + 拼图
python extract_keyframes.py --video "视频.mp4" --out frames/ --shot 4.5 6.5 9.0   # 精确时刻补抽
```

- 前置条件：ffmpeg / ffprobe 在 PATH 中；Python 3.10+（remove_ai_watermark.py 另需 numpy + opencv-python）。
- Windows Git Bash 若缺 coreutils（`ls` 报 command not found），把 Git 安装目录的 `usr/bin` 加入 PATH，或改用 PowerShell / cmd。
- 从拼图挑出机位（哪个时刻是正面、侧面、俯视、细节特写），再用 `--shot` 抽 `-q:v 2` 高质量单帧。

### Step 2 — 图生图重绘（产品一致性的关键）

用 ImageGen **图生图模式**，把 Step 1 挑出的原视频帧作为 `image1`：

- **必须传 `image1`**（参考帧）并设 `input_fidelity: "high"`、`quality: "high"`、`size: "1024x1536"`（竖屏带货）。
- 不传 `image1` 的纯文生图会**自创产品结构**（实测：头型、刷毛布局全跑偏），必须重做。
- Prompt 模板（关键句不可省）：

```
Recreate this scene as a clean commercial product photo. Keep the product EXACTLY
as in the reference: <逐条列出产品结构特征，如 white flat head / grey V-arranged
bristles / rubber squeegee lip / rotating joint / steel pole>. <场景与动作描述>.
Remove all subtitle text and watermarks. Photorealistic, bright soft lighting,
vertical 9:16, e-commerce style. Do not redesign the product.
```

- **逐张校验**：每生成一张就 Read 对比原帧，重点核对产品结构特征。第一张先验证通过，再批量生成其余的。

### Step 3 — 去除「AI生成 / WORKBUDDY」水印

生成的图右下角固定有平台水印。用 `scripts/remove_ai_watermark.py`：

```bash
python remove_ai_watermark.py --input "图片目录或单图" --output "输出目录" --sheet "检查拼图.jpg"
```

- 原理：右下角窄带 ROI（默认宽 28%、高 8%）内做**形态学顶帽**检测细亮笔画 → 膨胀 → TELEA inpaint，只擦文字、保背景。
- 调参决策规则：
  - 输出 `mask_px=0` 或水印仍可见（典型：白字压白台面/白泡沫，对比度极低）→ 降 `--thresh 15~20` 重跑该图。
  - 灰字压灰墙等更低对比场景 → 继续降 `--thresh 12`（实测一批 1024x1536 图，默认 45 全军覆没，12 全清）。
  - `--thresh 5` 仍有残影且角落是**平滑纯色面**（白瓷、白墙）→ 放弃阈值法，直接矩形整体修复：mask 填满水印所在小矩形（如 `[1440:1536, 860:1024]`）后 `cv2.inpaint(img, mask, 7, TELEA)`，平滑面重建无痕。
  - 角落出现涂抹感（亮背景被误修）→ 升 `--thresh 55~65`。
  - 必看 `--sheet` 输出的角落拼图验收，8 张一批一眼看完。
- 脚本已处理 **中文路径**（cv2.imread 读不了非 ASCII 路径会返回 None，脚本内部走 `np.fromfile + imdecode / imencode + write_bytes`），支持整目录批处理、`--corner` 四角、原地覆盖或输出到新目录。

### Step 4 — 归档

- 归档到用户自己的资产目录（示例：`D:\电商工作流\视频流程\3.资产\图片资产\`，产品图放其下 `产品资产\<产品名>\`），命名 `编号_类型_描述.png`（如 `01_正面全身_手持展示.png`）。
- 交付时列出全部成品图，并附一张「图 ↔ 视频场景时间点」对照表。

### Step 5 — 卖点痛点提炼（可独立执行）

从视频画面提炼产品洞察，输出 `产品卖点与痛点.md`，与资产图放**同一产品目录**。即使不生成图（用户只要洞察），本步骤也可单独跑——审片用 Step 1 的抽帧拼图即可。

**提炼规则（硬约束）：**

1. **只写画面可验证的事实**：视频里看不到的成分、参数、检测数据一律不写。杀菌率、除菌 99.9% 等量化结论没有检测报告就是红线。
2. **来源标注**：每条卖点/痛点标注 `[画面可见]` / `[用户提供]` / `[推断]`，不把推断伪装成画面事实。
3. **痛点来自对比**：一次性/耗材类产品的痛点本质是"传统替代方案的脏、臭、烦"，从产品机制反推它解决了什么。
4. **可溯源**：每条卖点挂上「支撑画面 + 视频时间点 + 对应资产图编号」，脚本和详情页可直接引用。
5. **适配市场**：话术、目标人群按视频语言/平台判断（如马来语字幕 → Lazada/TikTok 马来站），给本地化建议但不硬造当地俚语。
6. **规避项单独列出**：视频里出现的第三方 IP（卡通贴纸、商标）、平台水印、不可宣称词，都写进"注意事项"，防止下游脚踩坑。

**输出结构**：按 `references/insight-template.md` 的骨架写（产品定位 → 目标人群 → 痛点清单含画面锚点 → 卖点矩阵含证据 → 卖点↔痛点对照 → 三段式话术 → 注意事项 → 资产清单对照）。

**卖点矩阵分层**：主卖点 ≤3 条（一句话能打动人的机制级差异）→ 支撑点（长杆/壁挂/包装等结构性优势）→ 场景点（适用范围）。超过 3 条主卖点说明还没想清楚核心。

## Pitfalls（实测踩坑）

1. **忘记传 image1** → 产品结构自创，整张作废。生成前检查参数。
2. **cv2 中文路径** → 一律用脚本内封装的读写，不要裸调 `cv2.imread/imwrite`。
3. **Windows Git Bash 缺 coreutils** → 把 Git 安装目录的 `usr/bin` 加入 PATH，或改用 PowerShell / cmd。
4. **白底低对比水印** → 默认阈值检不出（mask_px=0 是信号），降 `--thresh`。
5. **亮色泡沫/金属高光** → 阈值法会整片误修，顶帽法默认已规避；若仍涂抹，升阈值。
6. 用户说"根据视频生成产品图"指的是**重绘**，不是截帧——先确认意图再动手。
7. **卖点痛点靠脑补** → 离开画面事实自由发挥，写出视频根本没有的功能。每条都要能在抽出的帧里指出来源。

## Resources

- `scripts/extract_keyframes.py` — 视频抽帧 + contact sheet 拼图（ffmpeg）
- `scripts/remove_ai_watermark.py` — 平台水印去除（cv2 顶帽 + inpaint，中文路径安全）
- `references/insight-template.md` — 卖点痛点洞察文档的输出骨架（Step 5 用）
