#!/usr/bin/env python3
"""
Canon promotion/demotion engine — 晋升/降级规则引擎
基于 Skill 使用频率自动推荐层级变更。

用法:
    python3 promotion.py                              # 执行完整评估
    python3 promotion.py --report                     # 只输出报告
    python3 promotion.py --apply                      # 生成推荐变更（不自动执行）
"""

import json, os, sys, time, datetime
from pathlib import Path

CANON_DIR = Path(__file__).parent.parent
CLASSIFICATION_PATH = CANON_DIR / "references" / "librarian-classification.json"
USAGE_PATH = Path("/root/.hermes/skills/.usage.json")

# 层级映射
LAYER_ORDER = {"hot": 0, "normal": 1, "seed_bank": 2, "isolation": 3}

# 阈值
HOT_THRESHOLD_30D = 50    # 30天 > 50次 → 建议升热层
SEED_THRESHOLD_90D = 3    # 90天 < 3次 → 建议入库
STALE_DAYS = 90           # 90天未使用 → 建议降级


def load_classification() -> list[dict]:
    """加载现有分类数据"""
    if not CLASSIFICATION_PATH.exists():
        print(f"⚠️  分类文件不存在: {CLASSIFICATION_PATH}")
        return []
    with open(CLASSIFICATION_PATH) as f:
        data = json.load(f)
    return data.get("skills", data) if isinstance(data, dict) else data


def load_usage() -> dict:
    """加载使用统计数据"""
    if not USAGE_PATH.exists():
        print(f"⚠️  使用统计数据不存在: {USAGE_PATH}")
        return {}
    try:
        with open(USAGE_PATH) as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"⚠️  读取使用统计失败: {e}")
        return {}


def calculate_usage_stats(raw: dict) -> dict[str, dict]:
    """
    从 .usage.json 计算每个技能的使用统计
    返回 {skill_name: {total, recent_7d, recent_30d, trend, last_used, layer}}
    """
    stats = {}
    now = time.time()
    seven_days = 7 * 86400
    thirty_days = 30 * 86400

    for skill_name, usage_data in raw.items():
        # 兼容不同格式
        if isinstance(usage_data, dict):
            calls = usage_data.get("calls", usage_data.get("count", 0))
            if isinstance(calls, list):
                calls = len(calls)
            last = usage_data.get("last_used", usage_data.get("last_call", ""))
        elif isinstance(usage_data, (int, float)):
            calls = int(usage_data)
            last = ""
        else:
            continue

        recent_7d = 0
        recent_30d = 0
        
        # 如果有时间戳列表，计算近期使用
        timestamps = []
        if isinstance(usage_data, dict):
            ts_list = usage_data.get("timestamps", usage_data.get("calls", []))
            if isinstance(ts_list, list):
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
        
        if timestamps:
            recent_7d = sum(1 for t in timestamps if (now - t) < seven_days)
            recent_30d = sum(1 for t in timestamps if (now - t) < thirty_days)
        
        # 趋势判断
        if recent_7d > 0 and recent_30d > 0:
            ratio = recent_7d / max(1, recent_30d / 4)  # 周化月比
            trend = "up" if ratio > 1.2 else ("down" if ratio < 0.8 else "flat")
        else:
            trend = "flat"

        stats[skill_name] = {
            "total_calls": calls if isinstance(calls, int) else 0,
            "recent_7d": recent_7d,
            "recent_30d": recent_30d,
            "trend": trend,
            "last_used": last if isinstance(last, str) else "",
        }

    return stats


def evaluate_skills(
    classification: list[dict],
    usage_stats: dict[str, dict],
) -> list[dict]:
    """
    对每个技能进行升降级评估。
    返回建议变更列表: [{skill_name, current_layer, suggested_layer, reason, confidence}]
    """
    suggestions = []

    for skill in classification:
        name = skill.get("skill_name", "")
        current_layer = skill.get("librarian_layer", "normal")
        judgment_score = skill.get("judgment_score", 0)
        anti_entropy = skill.get("anti_entropy_flag", False)
        
        # 读取前忽略无名的
        if not name:
            continue

        usage = usage_stats.get(name, {})
        recent_30d = usage.get("recent_30d", 0)
        recent_7d = usage.get("recent_7d", 0)
        total = usage.get("total_calls", 0)
        trend = usage.get("trend", "flat")

        # 决定建议层级
        suggested_layer = current_layer
        reasons = []
        confidence = 0.5

        # 晋升条件
        if current_layer in ("normal", "seed_bank") and recent_30d >= HOT_THRESHOLD_30D:
            suggested_layer = "hot"
            reasons.append(f"近30日使用{recent_30d}次（≥{HOT_THRESHOLD_30D}），达热气层标准")
            confidence = 0.8
        elif current_layer == "seed_bank" and recent_30d >= 5:
            suggested_layer = "normal"
            reasons.append(f"近30日使用{recent_30d}次，从种子库回到常驻层")
            confidence = 0.7
        elif current_layer == "seed_bank" and trend == "up" and recent_7d > 0:
            suggested_layer = "normal"
            reasons.append(f"使用趋势上升，建议从种子库回到常驻层观察")
            confidence = 0.6

        # 降级条件（anti_entropy 保护的技能不降级）
        if not anti_entropy:
            if current_layer == "hot" and recent_30d < 10 and total >= 0:
                suggested_layer = "normal"
                reasons.append(f"近30日仅使用{recent_30d}次，从热气层降回常驻层")
                confidence = 0.7
            elif current_layer in ("hot", "normal") and recent_30d < SEED_THRESHOLD_90D and total < 10:
                suggested_layer = "seed_bank"
                reasons.append(f"近30日仅使用{recent_30d}次（<{SEED_THRESHOLD_90D}），建议入库")
                confidence = 0.8
            elif current_layer == "normal" and total == 0:
                suggested_layer = "seed_bank"
                reasons.append("从未使用过，建议放入种子库")
                confidence = 0.6

        if suggested_layer != current_layer:
            suggestions.append({
                "skill_name": name,
                "current_layer": current_layer,
                "suggested_layer": suggested_layer,
                "reasons": reasons,
                "confidence": round(confidence, 2),
                "usage_data": {
                    "total_calls": usage.get("total_calls", 0),
                    "recent_7d": usage.get("recent_7d", 0),
                    "recent_30d": usage.get("recent_30d", 0),
                    "trend": usage.get("trend", "flat"),
                },
                "timestamp": datetime.datetime.now().isoformat(),
            })

    return suggestions


def generate_report(suggestions: list[dict], usage_stats: dict[str, dict]):
    """生成可读报告"""
    if not suggestions:
        print("=" * 50)
        print("📋 Canon 升降级评估报告")
        print("=" * 50)
        print("\n✅ 当前无需任何升降级变更，生态稳定。")
        print(f"   共评估 {len(usage_stats)} 个活跃技能。")
        return

    print("=" * 50)
    print("📋 Canon 升降级评估报告")
    print("=" * 50)
    print(f"\n建议变更: {len(suggestions)} 项\n")
    
    for s in suggestions:
        arrow = "⬆️" if LAYER_ORDER.get(s["suggested_layer"], 9) < LAYER_ORDER.get(s["current_layer"], 9) else "⬇️"
        print(f"  {arrow} {s['skill_name']}")
        print(f"     {s['current_layer']} → {s['suggested_layer']}")
        print(f"     置信度: {s['confidence']}")
        print(f"     原因:")
        for r in s["reasons"]:
            print(f"       · {r}")
        print(f"     近期使用: 7d={s['usage_data']['recent_7d']} 30d={s['usage_data']['recent_30d']} total={s['usage_data']['total_calls']}")
        print()
    
    print("—" * 50)
    print(f"共评估 {len(usage_stats)} 个技能")


def main():
    classification = load_classification()
    if not classification:
        print("❌ 无法加载分类数据，退出")
        sys.exit(1)
    
    raw_usage = load_usage()
    usage_stats = calculate_usage_stats(raw_usage)
    
    print(f"📊 已加载 {len(classification)} 个技能分类")
    print(f"📊 已加载 {len(usage_stats)} 个技能使用记录\n")
    
    suggestions = evaluate_skills(classification, usage_stats)
    
    if "--report" in sys.argv:
        generate_report(suggestions, usage_stats)
    else:
        # 完整输出含 JSON
        output = {
            "evaluated_at": datetime.datetime.now().isoformat(),
            "total_skills": len(classification),
            "active_usage_records": len(usage_stats),
            "suggested_changes": len(suggestions),
            "changes": suggestions,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
