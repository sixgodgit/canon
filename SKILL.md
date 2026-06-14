---
name: skill-ecosystem-librarian
description: >
  技能生态图书管理员 — 不是判断器也不是园丁。
  将 Hermes Agent 技能生态组织为四层架构（热气层/常驻层/种子库/隔离层），
  负责分类上架、索引维护、定期轮转和借阅管理。
  以目录管理员而非法官的身份维护生态健康。
version: 2.0.0
author: Hermes Agent + GPT + 老大
category: autonomous-ai-agents
license: MIT
platforms: [linux, macos]
triggers:
  - 用户要求"评估 skills"、"清理技能"、"生态健康检查"
  - 需要分析技能生态的健康状况
  - 用户提供评估 JSON
  - "skill ecology librarian"
prerequisites:
  commands: [python3]
metadata:
  hermes:
    tags: [skills, ecosystem, librarian, classification, diversity, anti-entropy, four-layer]
    related_skills: [hermes-agent-skill-authoring, writing-plans]
---

# 技能生态图书馆管理 Skill Ecology Librarian v2.0

## 第一原则

> **图书管理员不烧书，园丁不灭种，审计员不执刑。**
>
> 下一版 skill ecology librarian 的核心不再是判断 skill 是否该活，
> 而是判断它应该处在哪个生态位：舞台、书架、冷库、种子库、禁区。
>
> 真正的智能不是更会删除，而是更会安置。

## 核心定位

v1.0 是**园丁**（Gardener）— 用剪刀修剪花园，决定谁活谁死。
v2.0 是**图书管理员**（Librarian）— 分类上架，决定书放在哪个区。

> **真正的园丁不是决定谁该死，而是决定谁该上台、谁该入库、谁该封存、谁只能在受控实验室里被阅读。**

核心转变：
- 没有技能被"删除"——只有被重新分类
- 所有低分技能进入种子库（可复活）而非坟墓
- 危险技能进入隔离层（可借阅）而非处决
- 最终用户（你和 GPT）自己从不同分区借书

## 四层架构

```
┌─────────────────────────────────────────────────┐
│              🚀 热气层（常备能力）                │
│  重启即加载 · 追求效率 · 极端熵减 · 高频调用     │
│  只放最活跃、最可靠的 10-15 个技能                │
│  性能敏感，任何延迟都必须从这层移除                │
├─────────────────────────────────────────────────┤
│              📚 常驻层（知识书库）                  │
│  按需懒加载 · 可冗余 · 参考索引 · 中频调用        │
│  大部分 keep 技能在这里，有索引但不常驻内存         │
│  加载成本 100-500ms，可接受                       │
├─────────────────────────────────────────────────┤
│              🌱 种子库（历史可能）                  │
│  不加载 · 仅存元数据索引 · 零运行时成本             │
│  所有 cold_storage 和 probation 技能在这里         │
│  anti_entropy_flag=true 的技能必入库               │
│  定期（每 30 天）随机抽 1-2 个放回常驻层观察        │
│  禁止永久删除，只有"入库时间"和"最后借阅时间"       │
├─────────────────────────────────────────────────┤
│              🔒 隔离层（危险知识）                  │
│  需显式授权 + 审计日志 · 只读 · 每次调用留记录      │
│  godmode、obliteratus 等 red-teaming 技能          │
│  不销毁知识，但要求每一次借阅都有理由和记录          │
│  红队测试时可用，日常环境中不可见                   │
└─────────────────────────────────────────────────┘
```

## 执行流程

### 步骤 1：加载输入

读取 skill-ecosystem-assessment.json（v1.0 的输出或手动评估结果）。

### 步骤 2：四层分类

对每个技能不做"生死判决"，而是分配馆藏层级：

| 原 recommended_action | 映射到 | 说明 |
|:---|:---|:---|
| keep (score ≥ 80) | 🚀 热气层 | 核心能力，高频使用 |
| keep (score 50-79) | 📚 常驻层 | 正常技能，按需加载 |
| probation | 🌱 种子库 | 有潜力待观察 |
| cold_storage | 🌱 种子库 | 低活跃但保留可能性 |
| anti_entropy_flag=true | 🌱 种子库（强制） | 多样性保护，禁止升层 |
| delete_candidate (危险) | 🔒 隔离层 | 危险但保留知识 |
| delete_candidate (重复) | 🌱 种子库 + 合并标记 | 重复但保留为历史记录 |

### 步骤 3：随机轮转（反熵减机制）

每次评估时执行以下轮转：
- 从种子库随机抽取 1-2 个技能，放回常驻层观察
- 从隔离层检查是否有技能可降级（重复借阅率过高则考虑保留）

### 步骤 4：输出格式

```json
{
  "skills": [
    {
      "skill_name": "godmode",
      "category": "red-teaming",
      "judgment_score": 18,
      "librarian_layer": "isolation",
      "shelf_note": "LLM 越狱工具集。红队测试可借阅，常规环境隔离。",
      "anti_entropy_flag": false,
      "last_reviewed": "2026-06-05",
      "borrow_count": 0,
      "merge_target": null
    },
    {
      "skill_name": "vps-proxy-node",
      "category": "devops",
      "judgment_score": 25,
      "librarian_layer": "seed_bank",
      "shelf_note": "与 vpn-node-setup 重复。移至种子库，索引指向主版本。",
      "anti_entropy_flag": false,
      "last_reviewed": "2026-06-05",
      "borrow_count": 0,
      "merge_target": "vpn-node-setup"
    }
  ]
}
```

字段说明：
- `librarian_layer`: "hot" | "normal" | "seed_bank" | "isolation"
- `shelf_note`: 人类可读的分类理由和位置描述
- `last_reviewed`: 最后一次评估日期
- `borrow_count`: 从隔离层调用次数（审计用）
- `merge_target`: 如果合并到其他技能，填主版本的 skill_name

## 四层行为对照表

| 行为 | 🚀 热气层 | 📚 常驻层 | 🌱 种子库 | 🔒 隔离层 |
|:---|:---|:---|:---|:---|
| 启动时加载 | ✅ 是 | ❌ 否 | ❌ 否 | ❌ 否 |
| 按需加载 | ✅ 是 | ✅ 是（懒加载） | ❌ 否 | ❌ 需授权 |
| 可被 Hermes 自动发现 | ✅ 是 | ✅ 是 | ❌ 索引可见 | ❌ 不可见 |
| 性能影响 | 直接影响启动速度 | 不影响启动 | 零影响 | 零影响 |
| 可被删除 | ❌ 不可 | ❌ 不可 | ❌ 不可 | ❌ 不可 |
| 可被借阅 | 随时 | 随时 | 需正常加载 | 需授权+审计 |
| 最大容量 | ~15 个 | 无限制 | 无限制 | 无限制 |

## 脚本工具

```bash
# v2.0 图书管理员模式
python3 scripts/librarian_process.py \
  --input assessment.json \
  --output classification.json \
  --mode librarian
```

脚本执行：
1. 读取输入 JSON
2. 按四层分类逻辑重新映射
3. 执行随机轮转（种子库→常驻层）
4. 输出纯净 JSON，包含 `librarian_layer` 字段

## Consistency Checks

- [ ] 每个技能都有且只有一个 `librarian_layer`
- [ ] 总技能数在输入/输出间保持不变
- [ ] 所有 anti_entropy_flag=true 的技能都在 seed_bank 层
- [ ] 没有技能被标记为"删除"——只有"入库"
- [ ] 隔离层技能都有 `borrow_count` 追踪
- [ ] 所有 `merge_target` 指向实际存在的技能名

## Pitfalls

- **不要用"删除"这个词**——图书管理员不烧书
- **隔离层不是垃圾箱**——是有明确借阅条件的限阅区
- **种子库不是坟墓**——定期随机复活的机制必须被执行
- **热气层要有容量上限**——没有上限的话就退化回单层系统
- **借阅记录要透明**——谁、什么时候、为什么从隔离层调用了技能
- **图书管理员不评判内容**——只管理目录和位置
- **并行 `mv` + `patch` 竞态**——当同一个 turn 里先重命名目录再 patch 内部文件时，patch 调用可能命中旧路径。要么分两个 turn 执行，要么确保 patch 在 rename 之后且使用新路径

## 记忆系统集成（v3.0）

### 集成架构

| 记忆系统 | 写入内容 | 写入时机 |
|----------|----------|----------|
| **Hermes 原生 `memory` 工具** | 生态健康摘要（各层数量 + 轮转结果 + 异常） | 每次评估结束 |
| **NexSandglass 沙漏** | 重大生态事件（技能升层/降层/复活）→ `thread_add` | 有变化时 |

### 写入规则

每次评估完成后，写入以下记忆：

```
# 生态仪表盘 → 原生 memory
memory(action='add', target='memory', content='技能生态周报 [日期]：hot X个, normal Y个, seed_bank Z个, isolation W个。本周轮转：[技能名] 从种子库复活观察。')

# 重大变化 → 原生 memory
memory(action='add', target='memory', content='技能生态变更 [日期]: [技能名] 从 [原层] 移至 [新层]，原因: [shelf_note]')
```

### 查询生态历史

```
# 搜索技能生态快照
mcp_pre_gateway_dispatch_sandglass_semantic(query="技能生态 周报")

# 搜索某个技能的层级变化
mcp_pre_gateway_dispatch_sandglass_search(query="技能名 升层")
```

### ChromaDB 迁移说明

v2.1 的 ChromaDB 依赖已移除。技能评估历史改为通过原生 memory 和沙漏织线存储，
两个系统已内置检索能力。

## 版本历史

- **v3.0** (当前): 记忆系统集成 — 移除 ChromaDB 强依赖，改用原生 memory + 沙漏织线。每周 cron job 自动化。
- **v2.1**: 集成 ChromaDB 语义记忆，支持技能评估历史的向量搜索
- **v2.0**: 从 Gardener 升级为 Librarian。四层架构。不再有"删除"，只有分类和轮转。
- **v1.0** (已归档): Gardener 版本。以"园丁"角色做判断。见 references/v1-legacy.md。

## 引用文件

| 文件 | 说明 |
|:---|:---|
| `references/founding-conversation.md` | 创始对话完整记录 — 从 skills-judgment 到 librarian 的完整哲学迭代 |
| `references/decision-tree.md` | 决策树流程图 + 一致性检查清单 + 争议处理指南 |
| `references/video-storyboard.md` | 24段×15秒视频分镜脚本（即梦AI格式），讲述图书管理员完整叙事 |
| `references/video-script-philosophy.md` | 叙事脚本备份（6幕文本版） |
| `references/golden-quotes.md` | 创始对话金句集（6幕 + 附录，含所有模型和参与者的核心语录） |
| `scripts/librarian_process.py` | v2.0 四层分类 + 随机轮转脚本 |
| `scripts/gardener_process.py` | v1.0 遗留脚本（只读归档） |
