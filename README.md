# AI Video Role Pipeline Skill (Seedance 2.0 Ready)

Optimized multi-type AI video creation skill. Final output is a **copy-paste-ready Seedance Asset Package** for image-to-video / multimodal generation.

## Key Improvements
- Strict Seedance 2.0 constraints and @ reference syntax
- Exact image role assignments (first frame, character, product detail, etc.)
- Time-segmented prompts
- Type-specific templates for 7 content styles
- Final deliverable format designed for direct upload + paste into Seedance / Jimeng

## Supported Types
产品展示 · 生活种草 · 人物口播 · 搞怪离谱 · 剧情反转 · 感官氛围/ASMR · 伪纪录/采访

## Structure
```
ai-video-role-pipeline/
├── SKILL.md
└── references/
    ├── role-contracts.md
    ├── type-templates.md
    └── seedance-syntax.md
```

## Final Output Example Shape
1. Required Images table (Label + Purpose + Description)
2. Ready-to-Paste Prompt (with correct @Image roles)
3. Generation Parameters
4. Type-specific QA checklist

## Inspired by
- https://github.com/dexhunter/seedance2-skill
- https://github.com/Hwangsome/video-workflow-skills

## License
MIT
