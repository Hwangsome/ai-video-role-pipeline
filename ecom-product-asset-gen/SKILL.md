---
name: ecom-product-asset-gen
description: 从电商产品演示/带货视频生成与视频同款一致的产品资产图（三视图、细节图、场景图），供 AI 图生视频使用。触发词：提取产品图、生成产品场景图、产品三视图、视频生成参考图、产品资产、去 AI 生成水印、图生图保持产品一致。覆盖：ffmpeg 抽帧审片、ImageGen 图生图保真参数、产品一致性校验、平台水印去除、资产归档。
agent_created: true
---

# Ecom Product Asset Gen

## Overview

把一段产品演示视频转化为**可用于 AI 视频生成的干净产品资产图**。核心目标不是截帧，而是以视频帧为参考，重绘出无字幕、无水印、产品结构与视频完全一致的高质量场景图，并归档到用户的电商资产目录。

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

## Pitfalls（实测踩坑）

1. **忘记传 image1** → 产品结构自创，整张作废。生成前检查参数。
2. **cv2 中文路径** → 一律用脚本内封装的读写，不要裸调 `cv2.imread/imwrite`。
3. **Windows Git Bash 缺 coreutils** → 把 Git 安装目录的 `usr/bin` 加入 PATH，或改用 PowerShell / cmd。
4. **白底低对比水印** → 默认阈值检不出（mask_px=0 是信号），降 `--thresh`。
5. **亮色泡沫/金属高光** → 阈值法会整片误修，顶帽法默认已规避；若仍涂抹，升阈值。
6. 用户说"根据视频生成产品图"指的是**重绘**，不是截帧——先确认意图再动手。

## Resources

- `scripts/extract_keyframes.py` — 视频抽帧 + contact sheet 拼图（ffmpeg）
- `scripts/remove_ai_watermark.py` — 平台水印去除（cv2 顶帽 + inpaint，中文路径安全）
