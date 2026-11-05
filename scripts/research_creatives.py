#!/usr/bin/env python3
"""
research_creatives.py

Helper for ai-video-role-pipeline.
Given a product name and optional content type, outputs a structured research prompt
and suggested search queries that the agent should run via web_search / x_keyword_search
to collect real creative references from short-video platforms.

Usage:
  python research_creatives.py "一次性马桶刷" --type 搞怪离谱
  python research_creatives.py "一次性马桶刷"          # all types
"""

import argparse
import json
from typing import List, Dict

CONTENT_TYPES = [
    "产品展示",
    "生活种草",
    "人物口播",
    "搞怪离谱",
    "剧情反转",
    "感官氛围",
    "伪纪录",
]

PLATFORM_KEYWORDS = {
    "douyin": ["抖音", "douyin"],
    "tiktok": ["tiktok", "TikTok"],
    "xiaohongshu": ["小红书", "xiaohongshu", "red"],
    "bilibili": ["bilibili", "B站"],
}

def build_queries(product: str, content_type: str = None) -> List[Dict]:
    queries = []
    types = [content_type] if content_type else CONTENT_TYPES

    for t in types:
        # Chinese platform focused
        queries.append({
            "type": t,
            "platform": "综合短视频",
            "query": f"{product} {t} 视频 创意 OR 脚本 OR 分镜 site:douyin.com OR 抖音",
            "purpose": "找该类型下真实爆款/高赞创意方向"
        })
        queries.append({
            "type": t,
            "platform": "小红书/种草",
            "query": f"{product} {t} 种草 OR 推荐 小红书",
            "purpose": "找生活化表达与用户真实痛点表述"
        })
        queries.append({
            "type": t,
            "platform": "TikTok/海外",
            "query": f"{product} {t} OR funny OR ASMR OR review TikTok",
            "purpose": "找海外同类创意与视觉手法"
        })

    # Always add general pain-point / selling-point research
    queries.append({
        "type": "通用",
        "platform": "痛点卖点",
        "query": f"{product} 痛点 OR 缺点 OR 使用体验 OR 为什么买 OR 推荐理由",
        "purpose": "提取真实用户痛点与核心卖点"
    })
    queries.append({
        "type": "通用",
        "platform": "竞品创意",
        "query": f"{product} 广告 创意 OR 短视频 案例 OR 爆款",
        "purpose": "找已有广告/短视频创意避免同质化"
    })

    return queries


def main():
    parser = argparse.ArgumentParser(description="Generate research queries for product video creatives")
    parser.add_argument("product", help="Product name, e.g. 一次性马桶刷")
    parser.add_argument("--type", "-t", choices=CONTENT_TYPES, help="Specific content type")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    queries = build_queries(args.product, args.type)

    if args.json:
        print(json.dumps({"product": args.product, "queries": queries}, ensure_ascii=False, indent=2))
    else:
        print(f"# Research Queries for 「{args.product}」\n")
        if args.type:
            print(f"Focused type: {args.type}\n")
        print("Agent should run these via web_search or x_keyword_search:\n")
        for i, q in enumerate(queries, 1):
            print(f"{i}. [{q['type']}] ({q['platform']})")
            print(f"   Query: {q['query']}")
            print(f"   Purpose: {q['purpose']}\n")

        print("\n--- After collecting results ---")
        print("Summarize into:")
        print("- 真实用户痛点 (with source snippets)")
        print("- 高频卖点 / 推荐理由")
        print("- 该类型下已有创意方向 (避免重复)")
        print("- 可借鉴的视觉/节奏/反转手法")
        print("Then feed into Content Strategist concept_brief.md")


if __name__ == "__main__":
    main()
