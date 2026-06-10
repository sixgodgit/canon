# Hermes 技能生态图书管理员 v4.0

> 图书管理员不烧书，园丁不灭种，审计员不执刑。韧性优先，不是效率优先。

## 项目简介

本项目记录了 Hermes Agent 技能生态管理系统的设计演进、核心文档和实现代码。

**v4.0 核心特性：**
- 🏷️ **柔性标签系统** — 多标签并存，取代硬性分层
- ⚖️ **动态权重评分** — 按技能类型和生态上下文自动调整
- 🔄 **复兴引擎** — 主动验证休眠技能的潜在价值
- 🗄️ **归档深冻层** — 解决僵尸技能堆积问题
- 🗳️ **社区共识治理** — RFC 流程式的技能审核

**设计驱动：** 由 Claude Sonnet 4 / DeepSeek R1 / Qwen3 235B / GPT-4.1 四模型深度分析驱动优化。

## 历史演进

| 版本 | 名称 | 定位 | 核心改进 |
|------|------|------|----------|
| v1.0 | skills-judgment | 审判系统 | 六维评分，自动清理 |
| v2.0 | hermes-skill-curation | 园丁系统 | 反熵保护，对抗性辩护 |
| v3.0 | skill-ecosystem-librarian | 图书管理员 | 四层架构，三不原则 |
| **v4.0** | **skill-ecosystem-librarian** | **韧性生态系统** | **柔性标签，动态权重，主动活化** |

## 目录结构

```
├── README.md                    # 项目说明
├── docs/                        # 文档目录
│   ├── evolution.md             # 演进历史（v1.0→v4.0）
│   ├── architecture.md          # 架构设计 v4.0
│   └── scoring-system.md        # 评分体系详解 v4.0
├── src/                         # 代码目录
│   ├── ecosystem-librarian.md   # 核心系统 v4.0
│   └── skill-curation.md        # 园丁系统 v2.0（历史）
└── references/
    └── evaluation-example.json  # 评估示例 v4.0
```

## 快速开始

```python
from src.ecosystem_librarian import SkillEcosystemLibrarianV4

# 初始化
librarian = SkillEcosystemLibrarianV4(ecosystem_context="stability")

# 组织技能
results = librarian.organize(skills, skill_types={"pixel-art": "creative"})

# 生成报告
report = librarian.generate_report(skills)
```

## 核心概念

### 柔性标签
每个技能可拥有多个标签，不再非此即彼：
```
pixel-art: [cold, unique, potential, degraded, mature]
hermes-agent: [hot, unique, core, healthy, mature]
```

### 动态权重
按技能类型自动调整评分权重：
- **工具型**：活跃度30% + 稳健度25%（可靠性优先）
- **创意型**：独特性30% + 完整度20%（创新优先）
- **研究型**：独特性25% + 适应度20%（探索优先）

### 归档深冻
超过90天未使用的技能自动归档，保存元数据但释放资源，保留复活可能性。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request。

---

## 📄 License

This project is licensed under **CC BY-NC 4.0** — [Creative Commons Attribution-NonCommercial 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

- ✅ **Free to use** — personal, educational, and open-source projects
- ✅ **Free to modify and distribute**
- ✅ **Attribution required** — Credit: **sixgod** ([@sixgodgit](https://github.com/sixgodgit))
- ❌ **No commercial use** — Selling or profit-making from this code is prohibited

**Author:** sixgod | **GitHub:** [github.com/sixgodgit](https://github.com/sixgodgit)

