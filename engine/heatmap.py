#!/usr/bin/env python3
"""
Canon heatmap analyzer — 热度分析
读取技能使用数据，计算热度排名和趋势。

用法:
    python3 heatmap.py                           # 完整热度报告
    python3 heatmap.py --top10                   # 仅 Top 10
    python3 heatmap.py --bottom10                # 仅 Bottom 10
    python3 heatmap.py --json                    # JSON 输出
"""

import json, os, sys, time, datetime
from pathlib import Path

USAGE_PATH = Path("/root/.hermes/skills/.usage.json")


def load_usage() -> dict:
    if not USAGE_PATH.exists():
        print(f"⚠️  使用统计数据不存在: {USAGE_PATH}")
        sys.exit(1)
    with open(USAGE_PATH) as f:
        return json.load(f)


def analyze() -> list[dict]:
    """计算每个技能的热度指标，返回排序后的列表"""
    raw = load_usage()
    now = time.time()
    seven_days = 7 * 86400
    thirty_days = 30 * 86400

    results = []
    for skill_name, data in raw.items():
        if isinstance(data, dict):
            total = data.get("calls", data.get("count", 0))
            if isinstance(total, list):
                total = len(total)
            ts_list = data.get("timestamps", data.get("calls", []))
        elif isinstance(data, (int, float)):
            total = int(data)
            ts_list = []
        else:
            continue

        timestamps = []
        for ts in ts_list:
            if isinstance(ts, (int, float)):
                timestamps.append(ts)
            elif isinstance(ts, str):
                try:
                    timestamps.append(float(
                        datetime.datetime.fromisoformat(ts).timestamp()
                    ))
                except (ValueError, TypeError):
                    pass

        r7 = sum(1 for t in timestamps if (now - t) < seven_days)
        r30 = sum(1 for t in timestamps if (now - t) < thirty_days)

        # 趋势
        if r7 > 0 and r30 > 0:
            weekly_rate = r7 / 1
            monthly_rate = r30 / 4
            if weekly_rate > monthly_rate * 1.2:
                trend = "📈 up"
            elif weekly_rate < monthly_rate * 0.8:
                trend = "📉 down"
            else:
                trend = "➡️ flat"
        elif r7 > 0:
            trend = "📈 up"
        else:
            trend = "➖ cold"

        # 最后使用时间
        last_used = ""
        if timestamps:
            last_ts = max(timestamps)
            days_ago = (now - last_ts) / 86400
            last_used = f"{int(days_ago)}天前" if days_ago >= 1 else "今天"

        results.append({
            "skill": skill_name,
            "total": int(total),
            "recent_7d": r7,
            "recent_30d": r30,
            "trend": trend,
            "last_used": last_used,
            "heat_score": round(r7 * 5 + r30 * 2 + min(total, 100) * 0.1, 1),
        })

    results.sort(key=lambda x: x["heat_score"], reverse=True)
    return results


def print_top(results: list[dict], n: int = 10):
    print(f"\n🔥 热度 Top {n}")
    print(f"{'#':>3} | {'Skill':<35} | {'Total':>7} | {'7d':>4} | {'30d':>4} | {'Trend':>10} | {'Last':>8}")
    print("-" * 85)
    for i, r in enumerate(results[:n], 1):
        print(f"{i:>3} | {r['skill']:<35} | {r['total']:>7} | {r['recent_7d']:>4} | {r['recent_30d']:>4} | {r['trend']:>10} | {r['last_used']:>8}")


def print_bottom(results: list[dict], n: int = 10):
    bottom = results[-n:] if len(results) >= n else results
    bottom.reverse()
    print(f"\n❄️ 冷度 Bottom {n}")
    print(f"{'#':>3} | {'Skill':<35} | {'Total':>7} | {'7d':>4} | {'30d':>4} | {'Trend':>10}")
    print("-" * 75)
    for i, r in enumerate(bottom, 1):
        print(f"{i:>3} | {r['skill']:<35} | {r['total']:>7} | {r['recent_7d']:>4} | {r['recent_30d']:>4} | {r['trend']:>10}")


def main():
    results = analyze()
    
    if "--json" in sys.argv:
        print(json.dumps(results[:50], ensure_ascii=False, indent=2))
        return
    
    print(f"\n📊 Canon 热度分析")
    print(f"{'='*50}")
    print(f"共 {len(results)} 个技能")
    
    print_top(results, 20 if "--top10" not in sys.argv else 10)
    
    if "--top10" not in sys.argv:
        print_bottom(results, 10 if "--bottom10" not in sys.argv else 5)


if __name__ == "__main__":
    main()
