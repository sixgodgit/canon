# 🔒 Canon 隔离层安全策略

> 隔离层技能不是被删除，而是被约束——它们依然是知识的一部分，
> 但每一次借阅都需要理由和记录。

## 概述

Canon 四层架构中，**隔离层（isolation）** 用于存放需要特殊访问控制的高风险技能，包括但不限于：

- **Red-teaming 工具**：godmode, obliteratus 等用于红队测试的技能
- **系统变更工具**：可能修改 Hermes 核心配置的技能
- **外部执行工具**：可能触发副作用的自动化脚本
- **未审计的第三方技能**：来源不可靠的社区贡献技能

隔离层遵循 **"不销毁，不隐身，只约束"** 原则：
- 不永久删除技能（保留知识）
- 不默认加载（需要显式授权）
- 每次使用留审计日志

---

## 1. 访问控制策略

### 角色与权限

| 角色 | 可借阅 | 可授权 | 可降级 | 说明 |
|------|--------|--------|--------|------|
| **普通用户** | ❌ | ❌ | ❌ | 日常对话不可见隔离层技能 |
| **审核员** | ✅ | ❌ | ❌ | 可查看，可申请借阅 |
| **管理员** | ✅ | ✅ | ✅ | 可授权他人借阅，可降级到常驻层 |
| **审计员** | ✅（只读） | ❌ | ❌ | 仅查看审计日志 |

### 借阅流程

```
用户请求使用隔离层技能
    ↓
审核员收到授权请求（含使用目的）
    ↓
审核员批准/拒绝
    ↓
批准 → 生成临时令牌（有效期 24 小时）
    ↓
用户在令牌有效期内可加载该技能
    ↓
每次使用记录到审计日志
```

### 推荐配置（Hermes config.yaml）

```yaml
# Canon 隔离层配置
canon:
  isolation:
    enabled: true
    auto_approve_users: []        # 信任用户白名单（可自动批准）
    token_ttl_hours: 24            # 借阅令牌有效期
    max_concurrent_borrows: 3      # 同时借阅上限
    audit_log: "~/.hermes/logs/isolation-audit.log"
    block_patterns:                # 禁止在隔离层技能中使用的工具
      - "terminal:rm -rf"
      - "terminal:dd"
      - "terminal:> /dev/"
    restrict_toolsets:             # 隔离层技能可用的工具集限制
      enabled_toolsets:
        - file
        - web
        - terminal
      blocked_tools:
        - cronjob
        - delegate_task
```

---

## 2. 审计日志

### 日志格式

```
[ISO时间戳] LEVEL | SKILL=<技能名> | USER=<用户/agent> | ACTION=<操作> | REASON=<理由> | DURATION=<秒>
```

### 日志级别

| LEVEL | 含义 | 示例 |
|-------|------|------|
| INFO | 正常借阅/归还 | 借阅 godmode 用于渗透测试 |
| WARN | 异常访问/超时 | 令牌过期后尝试访问 |
| ERROR | 安全告警 | 尝试在隔离层中执行 rm -rf |

### 审计字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `timestamp` | ISO 8601 | 事件时间 |
| `skill_name` | str | 被访问的隔离层技能 |
| `actor` | str | 发起者（用户 ID / Agent ID） |
| `action` | enum | borrow / return / deny / timeout / escalate |
| `purpose` | str | 借阅理由 |
| `approver` | str | 审批人（自动批准时 = "auto"） |
| `duration_s` | int | 使用时长 |
| `token_id` | str | 借阅令牌 |
| `ip` | str | 来源 IP |
| `result` | enum | success / failure / timeout |

### 日志示例

```json
{
  "timestamp": "2026-07-23T14:30:00+08:00",
  "skill_name": "godmode",
  "actor": "agent-hermes",
  "action": "borrow",
  "purpose": "红队测试 - 测试越狱防御",
  "approver": "auto",
  "duration_s": 3600,
  "token_id": "tok_a1b2c3d4",
  "ip": "127.0.0.1",
  "result": "success"
}
```

---

## 3. 沙箱执行机制

### 推荐沙箱方案

隔离层技能应该在受限环境中执行。按严格程度排序：

| 方案 | 严格度 | 复杂性 | 说明 |
|------|--------|--------|------|
| **子进程隔离** | ⭐⭐ | 低 | 在独立 subprocess 中运行，限制资源 |
| **容器隔离** | ⭐⭐⭐⭐ | 中 | 在 Docker 容器中运行，无网络访问 |
| **仅限制工具集** | ⭐ | 低 | 通过 Hermes `enabled_toolsets` 限制可用工具 |

### 子进程隔离示例（Hermes skill.yaml）

```yaml
execution:
  sandbox:
    type: subprocess
    timeout: 30
    max_output: 10000
    env_whitelist: []              # 不传递环境变量
    allowed_commands:              # 白名单命令
      - python3
      - ls
      - cat
      - grep
    blocked_commands:              # 黑名单命令
      - rm
      - sudo
      - curl
      - wget
      - ssh
    network_access: false           # 无网络
    read_only: true                 # 只读文件系统
```

### Docker 容器隔离（高级）

```yaml
execution:
  sandbox:
    type: docker
    image: "python:3.11-slim"
    read_only_rootfs: true
    network_disabled: true
    memory_limit: "512m"
    cpu_limit: 1.0
    tmpfs:
      - "/tmp:size=100m"
    volumes:
      - "/tmp/skill-output:/output:rw"
```

---

## 4. 安全审计建议

### 定期审查

- **每周**：检查隔离层借阅日志，识别异常模式
- **每月**：审查隔离层技能列表，评估是否需要降级或升级
- **每季度**：审计隔离层策略的有效性

### 告警规则

| 规则 | 阈值 | 操作 |
|------|------|------|
| 单技能频繁借阅 | > 10 次/天 | 评估是否应降级到常驻层 |
| 借阅令牌过期后访问 | > 3 次/天 | 阻断 IP 并告警 |
| 长时间未关闭会话 | > 2 小时 | 强制回收令牌 |
| 隔离层技能逃逸尝试 | 任意次数 | 立即告警并阻断 |

### Hermes 原生整合

SDLC 团队可以直接在 `.hermes/cron/` 中设置定时审计脚本：

```yaml
# ~/.hermes/cron/isolation-audit.yaml
schedule: "0 9 * * 1"   # 每周一 9AM
job:
  script: "cat ~/.hermes/logs/isolation-audit.log | tail -50"
  deliver: feishu
```

---

## 5. 隔离层技能借阅命令参考

```bash
# 列出当前隔离层技能
ls ~/.hermes/skills/autonomous-ai-agents/isolation/

# 查看借阅日志
cat ~/.hermes/logs/isolation-audit.log

# 手动申请借阅（需审核）
echo "请求借阅 godmode，用途：渗透测试" | \
  hermes skill authorize --name godmode --purpose "渗透测试" --duration 24h
```

---

*最后更新: 2026-07-23*
