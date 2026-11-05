#!/usr/bin/env python3
"""
format_insight.py

Takes rough research notes (pain points, selling points, creative ideas)
and outputs a clean markdown block ready to insert into concept_brief.md
or the final Asset Package "Product Insight Summary".

Usage (example):
  python format_insight.py --pain "马桶刷用完要洗很恶心" "刷头藏污纳垢" \
                           --benefit "一次性免清洗" "干净卫生" \
                           --ideas "把刷子当麦克风" "认真清洁突然发疯"
"""

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pain", "-p", nargs="+", default=[], help="User pain points")
    parser.add_argument("--benefit", "-b", nargs="+", default=[], help="Selling points / benefits")
    parser.add_argument("--ideas", "-i", nargs="+", default=[], help="Creative directions found")
    parser.add_argument("--how", default="", help="How this video will show the benefit")
    args = parser.parse_args()

    print("## Product Insight Summary\n")
    print("### 用户痛点")
    if args.pain:
        for p in args.pain:
            print(f"- {p}")
    else:
        print("- （待补充）")

    print("\n### 核心卖点")
    if args.benefit:
        for b in args.benefit:
            print(f"- {b}")
    else:
        print("- （待补充）")

    print("\n### 已收集到的创意方向（参考，避免同质化）")
    if args.ideas:
        for idea in args.ideas:
            print(f"- {idea}")
    else:
        print("- （暂无）")

    print("\n### 本视频如何体现")
    print(args.how or "（由 Narrative 角色根据痛点→卖点结构填写）")


if __name__ == "__main__":
    main()
