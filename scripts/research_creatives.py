#!/usr/bin/env python3
"""
research_creatives.py

Helper for ai-video-role-pipeline.
Generates targeted search queries for a product + content type + target market + platform
so the agent can collect real creative references from the right place.

Usage:
  python research_creatives.py "一次性马桶刷" --type 搞怪离谱 --market 中国大陆 --platform 抖音
  python research_creatives.py "一次性马桶刷" --market 美国 --platform TikTok
  python research_creatives.py "一次性马桶刷"          # defaults: 中国大陆 + 抖音
"""

import argparse
import json
from typing import List, Dict, Optional

CONTENT_TYPES = [
    "产品展示", "生活种草", "人物口播", "搞怪离谱",
    "剧情反转", "感官氛围", "伪纪录",
]

# Market defaults
MARKET_CONFIG = {
    "中国大陆": {"default_platform": "抖音", "lang": "zh"},
    "美国":     {"default_platform": "TikTok", "lang": "en"},
    "日本":     {"default_platform": "TikTok", "lang": "ja"},
    "东南亚":   {"default_platform": "TikTok", "lang": "en"},
    "韩国":     {"default_platform": "TikTok", "lang": "ko"},
}

# Platform → search bias
PLATFORM_CONFIG = {
    "抖音": {
        "query_extra": "抖音 OR douyin",
        "style_note": "快节奏、强反差、卡点、直接卖点、竖屏",
    },
    "小红书": {
        "query_extra": "小红书 OR xiaohongshu OR rednote",
        "style_note": "精致生活感、种草语气、真实分享、美图",
    },
    "TikTok": {
        "query_extra": "TikTok OR \"tik tok\"",
        "style_note": "trend audio、口语、irony、relatable、竖屏",
    },
    "YouTube Shorts": {
        "query_extra": "\"YouTube Shorts\" OR \"YT Shorts\"",
        "style_note": "稍完整叙事、可稍长、清晰信息点",
    },
    "Instagram Reels": {
        "query_extra": "\"Instagram Reels\" OR Reels",
        "style_note": "视觉美观、生活方式、轻剧情",
    },
    "B站": {
        "query_extra": "B站 OR bilibili",
        "style_note": "可稍长、弹幕感、知识/趣味结合",
    },
    "Shopee Video": {
        "query_extra": "Shopee OR \"Shopee Video\"",
        "style_note": "强转化、展示使用、价格/优惠感",
    },
}

DEFAULT_MARKET = "中国大陆"
DEFAULT_PLATFORM = "抖音"


def resolve_platform(market: str, platform: Optional[str]) -> str:
    if platform and platform in PLATFORM_CONFIG:
        return platform
    # fallback to market default
    return MARKET_CONFIG.get(market, {}).get("default_platform", DEFAULT_PLATFORM)


def build_queries(product: str, content_type: Optional[str], market: str, platform: str) -> List[Dict]:
    queries = []
    types = [content_type] if content_type else CONTENT_TYPES
    pcfg = PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG[DEFAULT_PLATFORM])
    platform_hint = pcfg["query_extra"]

    for t in types:
        queries.append({
            "type": t,
            "platform": f"{market} · {platform}",
            "query": f"{product} {t} 视频 创意 OR 脚本 OR 分镜 OR funny OR review {platform_hint}",
            "purpose": f"找 {market}/{platform} 该类型下真实爆款/高赞创意方向"
        })
        queries.append({
            "type": t,
            "platform": f"{market} · {platform} 种草/评价",
            "query": f"{product} {t} 种草 OR 推荐 OR review OR 使用体验 {platform_hint}",
            "purpose": "找生活化表达与用户真实痛点表述"
        })

    queries.append({
        "type": "通用",
        "platform": f"{market} · {platform} 痛点卖点",
        "query": f"{product} 痛点 OR 缺点 OR 使用体验 OR 为什么买 OR 推荐理由 OR review OR complaint {platform_hint}",
        "purpose": f"提取 {market} 真实用户痛点与核心卖点"
    })
    queries.append({
        "type": "通用",
        "platform": f"{market} · {platform} 竞品创意",
        "query": f"{product} 广告 创意 OR 短视频 案例 OR 爆款 OR commercial OR ad {platform_hint}",
        "purpose": "找已有广告/短视频创意避免同质化"
    })

    return queries


def main():
    parser = argparse.ArgumentParser(description="Generate research queries for product video creatives")
    parser.add_argument("product", help="Product name, e.g. 一次性马桶刷")
    parser.add_argument("--type", "-t", choices=CONTENT_TYPES, help="Specific content type")
    parser.add_argument("--market", "-m", default=DEFAULT_MARKET,
                        help=f"Target market/country (default: {DEFAULT_MARKET})")
    parser.add_argument("--platform", "-p", default=None,
                        choices=list(PLATFORM_CONFIG.keys()),
                        help="Target platform (default depends on market)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    market = args.market
    platform = resolve_platform(market, args.platform)
    queries = build_queries(args.product, args.type, market, platform)
    style_note = PLATFORM_CONFIG.get(platform, {}).get("style_note", "")

    result = {
        "product": args.product,
        "market": market,
        "platform": platform,
        "style_note": style_note,
        "queries": queries,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"# Research Queries for 「{args.product}」")
        print(f"Target market : {market}")
        print(f"Target platform: {platform}")
        print(f"Style note    : {style_note}\n")
        if args.type:
            print(f"Focused type  : {args.type}\n")
        print("Agent should run these via web_search or x_keyword_search:\n")
        for i, q in enumerate(queries, 1):
            print(f"{i}. [{q['type']}] ({q['platform']})")
            print(f"   Query: {q['query']}")
            print(f"   Purpose: {q['purpose']}\n")

        print("--- After collecting results ---")
        print("Summarize into:")
        print("- 真实用户痛点 (with source snippets)")
        print("- 高频卖点 / 推荐理由")
        print(f"- 该市场({market}) + 平台({platform})下已有创意方向")
        print("- 可借鉴的视觉/节奏/反转手法（符合平台风格）")
        print("Then feed into Content Strategist concept_brief.md")


if __name__ == "__main__":
    main()
