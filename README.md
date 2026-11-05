# AI Video Role Pipeline Skill

A modular skill for creating short-form AI videos with Seedance 2.0 using five non-overlapping roles.

## Supported Content Types
- 产品展示 (Product Showcase)
- 生活种草 (Lifestyle Seeding)
- 人物口播 (Talking Head)
- 搞怪离谱 (Absurd Comedy)
- 剧情反转 (Plot Twist)
- 感官氛围 / ASMR
- 伪纪录 / 采访 (Mockumentary / Interview)

## Structure
```
ai-video-role-pipeline/
├── SKILL.md
└── references/
    ├── role-contracts.md
    └── type-templates.md
```

## How to Use
Install the skill into your agent skills directory, then trigger with phrases like:
- "用角色流水线做搞怪离谱视频"
- "Seedance 产品展示流程"
- "多类型视频角色 skill"

The agent will execute the five roles in order and produce the required markdown contracts + Seedance-ready prompts.

## License
MIT
