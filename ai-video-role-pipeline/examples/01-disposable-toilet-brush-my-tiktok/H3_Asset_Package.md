# H3 Asset Package — 《Toilet Brush Horror Story》（Ref2VA 版）

> 目标市场：马来西亚 ｜ 目标平台：TikTok ｜ **目标模型：MiniMax H3 · Ref2VA** ｜ 15s ｜ 9:16
> 与同目录 `Seedance_Asset_Package.md` 同一分镜、同一素材，仅提示词语法不同

## 0. Product Insight Summary
- 目标市场：马来西亚（明亮、生活化、强情绪）
- 目标平台：TikTok（快剪、relatable chaos、马来语+英语玩梗字幕）
- 目标模型：MiniMax H3 · Ref2VA（9 张图 ≤9 ✓）
- 用户痛点：传统刷毛缠毛发挂污；刷完甩水脏手；底座积水发臭；弯腰腰酸 [用户提供]
- 核心卖点：一次性刷头用完即弃；一按脱头落盒不脏手；蓝色清洁泡沫；海绵压沟槽无死角、长杆免弯腰 [用户提供]
- 本视频如何体现：0–3s 传统刷惨剧 → 3–9s 蓝泡爆发+开挂三连刷 → 9–12s 一按落盒 → 12–15s 冷静收尾
- 素材情况：用户产品图 6 张 + AI 生成脏刷对比图 + 人物三视图 3 张

## 1. Required Assets (upload in this order)

| Label | H3 标签 | Purpose | Description |
|-------|---------|---------|-------------|
| Image1 | `<Picture 1>`（[Shot 1] 首帧）+ `<Subject 1>` 内引 | 场景 + 产品锚点 | 灰墙前白色椭圆收纳盒（ecoco 标）壁挂+白长杆，旁边白马桶 |
| Image2 | `<Subject 1>` 内引 | 清洁力 | 蓝圆环头刷洗内沿，水泛蓝起泡 |
| Image3 | `<Subject 1>` 内引 | 死角 | 长杆直立，刷头压进内沿沟槽 |
| Image4 | `<Picture 4>`（[Shot 2] 构图锚点） | 蓝泡爆发 | 俯拍蓝色泡沫海洋 |
| Image5 | `<Picture 5>`（[Shot 4] 动作/构图锚点） | 翻盖丢弃 | 刷头正落进盒内垃圾袋 |
| Image6 | `<Subject 2>` 内引 | 反派道具 | 同场景传统圆头刷：发黄缠发藏污、积垢底座 |
| Image7 | `<Subject 3>` 内引 | 人物面部锚点 | 灰棕头巾+绿上衣+米白裤，正面 |
| Image8 | `<Subject 3>` 内引 | 侧脸轮廓 | 同一人物侧面 |
| Image9 | `<Subject 3>` 内引 | 背影/头巾 | 同一人物背面 |

## 2. Ready-to-Paste Prompt

```
subject_definitions:
<Subject 1> is the ecoco disposable toilet brush whose appearance is established by <Picture 1>, <Picture 2>, <Picture 3>, and <Picture 5>: a white long handle, a blue ring-shaped sponge head with a center hole, and a white oval wall-mounted storage box with a small lowercase "ecoco" logo.
<Subject 2> is the traditional round toilet brush in <Picture 6>, with yellowed nylon bristles matted with hair and grime, standing in a stained round holder.
<Subject 3> is the Malaysian woman whose face is established by <Picture 7>, whose profile is established by <Picture 8>, and whose headscarf and back view are established by <Picture 9>, wearing a taupe hijab, a sage-green tunic, and cream trousers.
<Picture 1> is the first frame of [Shot 1], showing the bright Malaysian bathroom with the white toilet and the wall-mounted holder.
<Picture 4> is the composition anchor for [Shot 2], defining the overhead framing of the blue foam filling the bowl.
<Picture 5> is the action and composition anchor for [Shot 4], defining how the used head drops into the storage box.

summary:
[reference generation + keyframe completion] The target video is a fast-cut comedic product short in which <Subject 3> first suffers through <Subject 2>, then uses <Subject 1> to clean the toilet with an exploding blue foam, and finally ejects the dirty head into the storage box with one thumb press. <Picture 1> anchors the opening frame, while <Picture 4> and <Picture 5> anchor the foam-reveal and disposal shots.

retention_analysis:
<Subject 1> (appears in [Shot 2], [Shot 3], [Shot 4], [Shot 5]): fully_preserved - the white handle, blue ring sponge head, and white oval storage box remain identical across all shots.
<Subject 2> (appears in [Shot 1]): fully_preserved - the yellowed matted bristles and stained holder are retained as the contrast prop.
<Subject 3> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5]): fully_preserved - her face, hijab, sage-green tunic, and cream trousers stay consistent throughout.
<Picture 1> ([Shot 1] first frame): fully_preserved - the bathroom layout, wall-mounted holder, and lighting are retained.
<Picture 4> ([Shot 2] composition): partially_preserved - the overhead blue-foam composition is kept while the foam expands dynamically.
<Picture 5> ([Shot 4] action): partially_preserved - the disposal composition is kept while the head falls with a fresh motion path.

detailed_description:
The target video is a bright, fast-paced comedic product short shot in a modern Malaysian bathroom, with warm tropical daylight and saturated colors.
[Shot 1] A medium shot begins from <Picture 1>, establishing the white toilet and the wall-mounted holder. <Subject 2>, the traditional round brush with yellowed matted bristles, is pulled from its stained holder by the hand of <Subject 3>. She scrubs twice, and the bristles snag a clump of hair. She flicks the brush; dirty water sprays sideways and speckles her cream trousers. A puff of exaggerated green stink lines rises from the holder as she recoils, fanning the air and staring into the lens with a crumpled, horrified expression. A bold caption "Toilet brush horror story" appears in the lower third. The camera shakes slightly at fast speed with each flick.
[Shot 2] At 00:03.000, the shot cuts to <Subject 3> (S1), who brightens, yanks <Subject 1> from the wall holder, and drives the blue ring sponge head into the water. The water erupts as a blue foam burst fills the bowl in the overhead framing of <Picture 4>, spreading like a wave. The camera pushes in with large amplitude at fast speed toward her face as it is lit blue and her mouth opens into a delighted O shape. A caption "POWER UP" snaps on screen.
[Shot 3] At 00:06.000, the shot cuts to a tight follow shot as the sponge head of <Subject 1> presses into the inner rim groove; yellow stains peel away with the foam. The head sweeps along the porcelain and the surface turns glossy. <Subject 3> stays fully upright using the long handle, no bending, her profile matching <Picture 8>, and she raises an eyebrow in smug satisfaction. Three scrub strokes land on the beat.
[Shot 4] At 00:09.000, the shot cuts to a close-up of her thumb pressing the release button; the blue head detaches cleanly. She flips the lid of the storage box and the used head drops in, landing in the liner exactly as framed by <Picture 5>. The lid snaps shut. She turns to the lens, spreads both hands, and shrugs with a calm, smug "isn't this obvious" look. A caption "Sekali tekan. Siap. Tak kotor tangan" appears.
[Shot 5] At 00:12.000, the shot cuts to a product-focus shot: the slim wall-mounted box and a fresh blue ring sponge head in its small wrapper. <Subject 3> taps the new head twice toward the lens, nods playfully, then the frame settles on the bright bathroom as her back, matching <Picture 9>, walks out of frame.

overall_soundscape:
A squelching wet scrubbing sound and a spray of dirty water open the video, followed by an exaggerated low stink hum. A heavy water burst and dense bubbling rise through the middle as the sponge scrubs the porcelain with three rhythmic swipes. A crisp plastic click, a soft drop into a lined box, and a lid snap close the action, with light footsteps leaving the tiled room at the end.

non_diegetic_music:
A playful comedic score at a fast tempo, built on pizzicato strings and a bright marimba pattern, with a short rising swell at the foam burst and a two-note button ending on the snap of the lid.
```

## 3. Generation Parameters
- **Mode**: Ref2VA（9 张图，符合 ≤9 限制）
- **Duration**: 15s（H3 上限）
- **Resolution**: 1080×1920（9:16 竖屏）
- **Audio**: 开启（24 FPS / 32 kHz 立体声由模型侧决定）

## 4. H3 QA Checklist
- [x] 模式选对：多图身份/场景/道具参考 → Ref2VA
- [x] 六段顺序：subject_definitions → summary → retention_analysis → detailed_description → overall_soundscape → non_diegetic_music
- [x] `subject_definitions` 之后无新标签（summary/retention 只复用已定义标签）
- [x] Subject 与 Picture 语义未混用：人物三视图合并为一个 `<Subject 3>`；仅首帧/构图/动作锚点单独列 Picture
- [x] `[Shot 1]` 无时间戳；后续 00:03.000 / 00:06.000 / 00:09.000 / 00:12.000 严格递增且 < 15s
- [x] 切点均带来新信息；一镜一主导运镜（shake / push in / follow / close-up / product focus）
- [x] 因果桥：甩水→抽新刷；泡沫爆发→刷洗；按按钮→落盒；落盒→收尾背影
- [x] 对白规则：本片无口播，仅有画面字幕（英文双引号原样），未虚构 (Sx) 说话人
- [x] `overall_soundscape` 不复述台词/字幕；`non_diegetic_music` 只写器乐/节奏/动态
- [x] 卖点被动作证明（出泡/沟槽刷净/一按落盒）、痛点被夸张呈现、产品三特征可识别
- [ ] 生成后人工复核：`<Subject 3>` 三视图是否融合成同一人、字幕位置是否遮挡产品、绿臭味特效是否滑稽不恐怖
