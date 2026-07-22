---
name: canon
description: >
  技能生态典章 — 不是判断器也不是园丁。
  将 Hermes Agent 技能生态组织为四层架构（热气层/常驻层/种子库/隔离层），
  负责分类上架、索引维护、定期轮转和借阅管理。
  以目录管理员而非法官的身份维护生态健康。
version: 2.1.0
author: Hermes Agent + GPT + 老大
category: autonomous-ai-agents
license: MIT
platforms: [linux, macos]
triggers:
  - "用户要求评估 skills"
  - "清理技能"
  - "生态健康检查"
  - "需要分析技能生态的健康状况"
  - "canon"
  - "watching the canon"
prerequisites:
  commands: [python3]
metadata:
  hermes:
    tags: [skills, ecosystem, canon, classification, diversity, anti-entropy, four-layer]
    related_skills: [hermes-agent-skill-authoring, writing-plans]
---

# 📚 Canon — 技能生态典章

> *"图书管理员不烧书，园丁不灭种，审计员不执刑。
> Canon 的核心不再是判断 skill 是否该活，而是判断它应该处在哪个生态位。"*

**Version**: v2.1.0 | **License**: MIT | **Role**: Librarian | **Platforms**: Linux, macOS

---

## 家族体系

| 项目 | 语源 | 角色 |
|------|------|------|
| **[Thalamus](https://github.com/sixgodgit/thalamus)** | 神经科学 🧠 | 路由中枢 — 决定谁来做 |
| **[Hypnos](https://github.com/sixgodgit/hypnos-dream-system)** | 希腊神话 💤 | 梦境进化 — 夜间认知循环 |
| **[Nyx](https://github.com/sixgodgit/nyx)** | 希腊神话 🌑 | 记忆感知 — 边缘意识 |
| **Canon ← 你在这里** | 拉丁语 📚 | 技能生态 — 什么值得留 |

---

## 概述

Canon 是 Hermes Agent 技能生态的**目录管理员**。它不判断技能是否该活，而是判断它该放在哪个区。

v1.0 是**园丁**（Gardener）— 用剪刀修剪花园，决定谁活谁死。  
v2.0+ 是**图书管理员**（Librarian）— 分类上架，决定书放在哪个区，定期轮转防止僵化。

### 核心转变

- 没有技能被"删除"——只有被重新分类
- 所有低分技能进入种子库（可复活）而非坟墓
- 危险技能进入隔离层（可借阅）而非处决
- 最终用户（你和 GPT）自己从不同分区借书

---

## 核心架构：四层体系

```
┌─────────────────────────────────────────────────┐
│              🚀 热气层（常备能力）                │
│  重启即加载 · 追求效率 · 极端熵减 · 高频调用     │
│  只放最活跃、最可靠的 10-15 个技能                │
├─────────────────────────────────────────────────┤
│              📚 常驻层（知识书库）                  │
│  按需懒加载 · 可冗余 · 参考索引 · 中频调用        │
│  大部分 keep 技能在这里，有索引但不常驻内存         │
├─────────────────────────────────────────────────┤
│              🌱 种子库（历史可能）                  │
│  不加载 · 仅存元数据索引 · 零运行时成本             │
│  所有 cold_storage 和 probation 技能在这里         │
│  anti_entropy_flag=true 的技能必入库               │
├─────────────────────────────────────────────────┤
│              🔒 隔离层（危险知识）                  │
│  需显式授权 + 审计日志 · 只读 · 每次调用留记录      │
│  完整访问控制/审计日志格式/沙箱建议见               │
│  references/isolation-policy.md                    │
└─────────────────────────────────────────────────┘
```

### 四层行为对照

| 行为 | 🚀 热气层 | 📚 常驻层 | 🌱 种子库 | 🔒 隔离层 |
|:---|:---:|:---:|:---:|:---:|
| 启动时加载 | ✅ | ❌ | ❌ | ❌ |
| 按需加载 | ✅ | ✅ 懒加载 | ❌ | ❌ 需授权 |
| 自动发现 | ✅ | ✅ | ❌ 索引可见 | ❌ 不可见 |
| 性能影响 | 直接影响启动 | 不影响 | 零影响 | 零影响 |
| 可删除 | ❌ | ❌ | ❌ | ❌ |
| 可借阅 | 随时 | 随时 | 需加载 | 授权+审计 |
| 最大容量 | ~15 个 | 无限制 | 无限制 | 无限制 |

---

## 执行流程

### 步骤 0：数据采集 — 三源核对

每周健康检查/手动评估时，必须从三个来源收集数据：

1. **skills_list()** — Hermes 可见的活跃技能
2. **磁盘扫描** — `find ~/.hermes/skills -name "SKILL.md"`
3. **旧分类文件** — `references/librarian-classification.json`

### 步骤 1：加载输入

读取 skill-ecosystem-assessment.json（v1.0 的输出或手动评估结果）。  
如果是每周 cron job，读取 `references/librarian-classification.json` 作为基准。

### 步骤 2：四层分类

对每个技能不做"生死判决"，而是分配馆藏层级：

| 原 recommended_action | 映射到 | 说明 |
|:---|:---|:---|
| keep (score >= 80) | 🚀 热气层 | 核心能力，高频使用 |
| keep (score 50-79) | 📚 常驻层 | 正常技能，按需加载 |
| probation | 🌱 种子库 | 有潜力待观察 |
| cold_storage | 🌱 种子库 | 低活跃但保留可能性 |
| anti_entropy_flag=true | 🌱 种子库（强制） | 多样性保护，禁止升层 |
| delete_candidate (危险) | 🔒 隔离层 | 危险但保留知识 |
| delete_candidate (重复) | 🌱 种子库 + 合并标记 | 重复但保留为历史记录 |

### 步骤 2.5：热度检测与自动轮转

在四层分类之后、随机轮转之前，先运行 `engine/` 下的自动化引擎：

1. **运行热度分析**：`python3 engine/heatmap.py`
   - 读取 `~/.hermes/skills/.usage.json`
   - 对每个技能计算总调用次数、近7天/近30天活跃度、趋势
   - 输出 Top 20 热门技能与 Bottom 10 冷门技能

2. **运行晋升/降级引擎**：`python3 engine/promotion.py`
   - 高频规则：近 30 天调用 > 50 次 → 建议升级至 🚀 热气层
   - 低频规则：近 90 天调用 < 3 次 → 建议降级入 🌱 种子库
   - `anti_entropy_flag=true` 的技能不参与自动降级
   - 🔒 隔离层技能永不参与自动晋升/降级
   - 引擎只产出建议（`promotion-recommendations.json`），**不直接改写**分类文件

3. **将建议并入本轮评估**：把 `promotion.py` 的输出与步骤 2 的分类结果合并

### 步骤 3：热度感知轮转（反熵减机制）

- 从种子库中，优先选择 `heatmap.py` 判定为回暖趋势的技能放回常驻层
- 若无回暖信号，仍从种子库随机抽取 1-2 个，保留反熵减兜底
- 隔离层的任何层级变更需遵循 `references/isolation-policy.md` 的人工审批流程

### 步骤 4：输出与一致性检查

每次评估必须验证：

- [ ] 输出技能总数 == 输入技能总数
- [ ] anti_entropy_flag=true 的技能，recommended_action ≠ "delete_candidate"
- [ ] JSON 格式可被 `python3 -c "import json; json.load(sys.stdin)"` 正确解析
- [ ] 不包含 report_metadata 或 summary 等附加元数据

---

## 引擎组件

### promotion.py — 晋升/降级规则引擎

```bash
python3 engine/promotion.py          # 完整评估
python3 engine/promotion.py --report # 只输出报告
```

- 基于 `.usage.json` 使用频率自动评分
- 高频（30天>50次）→ 建议升热层
- 低频（90天<3次）→ 建议入库
- 隔离层豁免 + 热气层容量守卫（默认15个）

### heatmap.py — 热度分析

```bash
python3 engine/heatmap.py             # 完整热度报告
python3 engine/heatmap.py --top10     # 仅 Top 10
python3 engine/heatmap.py --json      # JSON 输出
```

- 计算总调用、近7天、近30天、趋势（📈 up / 📉 down / ➡️ flat）
- 输出 Top 20 / Bottom 10

---

## 隔离层安全策略

隔离层技能的完整访问控制、审计日志格式、沙箱执行配置在独立文档中：

📄 **[references/isolation-policy.md](references/isolation-policy.md)**

包含：
- 角色与权限定义（普通用户/审核员/管理员/审计员）
- 借阅流程与临时令牌机制
- JSONL 审计日志格式示例
- 沙箱执行方案（子进程/Docker/工具集限制）
- 告警规则与定期审查建议

---

## 记忆系统集成

| 系统 | 写入内容 | 时机 |
|------|----------|------|
| **Hermes 原生 memory** | 生态健康摘要（各层数量+轮转结果+异常） | 每次评估结束 |
| **Nyx/沙漏** | 重大生态事件（技能升层/降层/复活） | 有变化时 |

---

## 与家族的关系

| 系统 | 输入 | 输出 |
|------|------|------|
| **Thalamus** 路由决策日志 | 技能使用频率数据 | Canon 级别影响技能选择 |
| **Hypnos** 梦境提炼 | 画像更新 | Canon 识别技能使用模式 |
| **Nyx** 夜之感知 | - | 生态事件感知 |

---

## 版本历史

- **v2.1.0** (当前): 新增 engine/ 自动化引擎（promotion.py + heatmap.py），步骤2.5热度检测，步骤3热度感知轮转，隔离层独立文档 isolation-policy.md
- **v2.0.0**: 从 Gardener 升级为 Librarian。四层架构。品牌名从 skill-ecosystem-librarian 更改为 Canon
- **v1.0**: Gardener 版本。以"园丁"角色做判断（已归档）
