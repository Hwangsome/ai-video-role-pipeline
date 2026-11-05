#!/usr/bin/env python3
"""
research_creatives.py

Helper for ai-video-role-pipeline.
Generates targeted search queries for a product + content type + target market
so the agent can collect real creative references, pain points and selling points
from the right platforms and cultural context.

Usage:
  python research_creatives.py "一次性马桶刷" --type 搞怪离谱 --market 中国大陆
  python research_creatives.py "一次性马桶刷" --market "美国"
  python research_creatives.py "一次性马桶刷"          # all types, default market 中国大陆
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

# Market → preferred platforms & language bias
MARKET_CONFIG = {
    "中国大陆": {
        "platforms": ["抖音", "小红书", "B站"],
        "lang": "zh",
        "extra": "抖音 OR 小红书",
    },
    "美国": {
        "platforms": ["TikTok", "YouTube Shorts", "Instagram Reels"],
        "lang": "en",
        "extra": "TikTok OR \"YouTube Shorts\"",
    },
    "日本": {
        "platforms": ["TikTok Japan", "YouTube", "Twitter"],
        "lang": "ja",
        "extra": "TikTok OR 日本",
    },
    "东南亚": {
        "platforms": ["TikTok", "Instagram", "Shopee Video"],
        "lang": "en",
        "extra": "TikTok OR Indonesia OR Thailand OR Vietnam",
    },
    "韩国": {
        "platforms": ["TikTok", "YouTube", "Instagram"],
        "lang": "ko",
        "extra": "TikTok OR 한국",
    },
}

DEFAULT_MARKET = "中国大陆"


def build_queries(product: str, content_type: str = None, market: str = DEFAULT_MARKET) -> List[Dict]:
    queries = []
    types = [content_type] if content_type else CONTENT_TYPES
    cfg = MARKET_CONFIG.get(market, MARKET_CONFIG[DEFAULT_MARKET])
    platform_hint = cfg["extra"]

    for t in types:
        queries.append({
            "type": t,
            "platform": f"{market} 主流短视频",
            "query": f"{product} {t} 视频 创意 OR 脚本 OR 分镜 {platform_hint}",
            "purpose": f"找{market}该类型下真实爆款/高赞创意方向"
        })
        queries.append({
            "type": t,
            "platform": f"{market} 种草/评价",
            "query": f"{product} {t} 种草 OR 推荐 OR review OR funny {platform_hint}",
            "purpose": "找生活化表达与用户真实痛点表述"
        })

    # Always add general pain-point / selling-point research (market biased)
    queries.append({
        "type": "通用",
        "platform": f"{market} 痛点卖点",
        "query": f"{product} 痛点 OR 缺点 OR 使用体验 OR 为什么买 OR 推荐理由 OR review OR complaint {platform_hint}",
        "purpose": f"提取{market}真实用户痛点与核心卖点"
    })
    queries.append({
        "type": "通用",
        "platform": f"{market} 竞品创意",
        "query": f"{product} 广告 创意 OR 短视频 案例 OR 爆款 OR commercial OR ad {platform_hint}",
        "purpose": "找已有广告/短视频创意避免同质化"
    })

    return queries


def main():
    parser = argparse.ArgumentParser(description="Generate research queries for product video creatives")
    parser.add_argument("product", help="Product name, e.g. 一次性马桶刷")
    parser.add_argument("--type", "-t", choices=CONTENT_TYPES, help="Specific content type")
    parser.add_argument("--market", "-m", default=DEFAULT_MARKET,
                        help=f"Target market/country (default: {DEFAULT_MARKET}). Examples: 中国大陆, 美国, 日本, 东南亚, 韩国")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    market = args.market if args.market in MARKET_CONFIG else args.market  # allow free-form
    queries = build_queries(args.product, args.type, market)

    if args.json:
        print(json.dumps({"product": args.product, "market": market, "queries": queries}, ensure_ascii=False, indent=2))
    else:
        print(f"# Research Queries for 「{args.product}」")
        print(f"Target market: {market}\n")
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
        print("- 该市场+类型下已有创意方向 (避免重复)")
        print("- 可借鉴的视觉/节奏/反转手法（符合目标市场风格）")
        print("Then feed into Content Strategist concept_brief.md")


if __name__ == "__main__":
    main()
