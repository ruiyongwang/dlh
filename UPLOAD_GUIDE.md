# 度量衡智库 · GitHub 发布指南

## 📁 目录结构

```
dlh-skills/
├── README.md              # 中文主文档
├── README_en.md           # English README
├── UPLOAD_GUIDE.md       # 上传指南（本文件）
└── skills/                # 技能文件夹
    ├── cn-project-management/
    ├── cn-cost-control/
    └── ...
```

## 🚀 发布到 GitHub

### 方式一：手动上传（推荐）

1. **Fork 仓库**
   - 访问 https://github.com/ruiyongwang/dlh
   - 点击 Fork 创建您的副本

2. **上传文件**
   - 进入仓库页面
   - 点击 "Add file" → "Upload files"
   - 将 `dlh-skills` 目录下的所有技能文件夹拖入上传区域

3. **提交更改**
   - 填写 commit message
   - 点击 "Commit changes"

### 方式二：Git 命令行

```bash
# 1. 克隆仓库
git clone https://github.com/ruiyongwang/dlh.git
cd dlh

# 2. 创建技能目录结构
mkdir -p skills/cn-project-management
mkdir -p skills/cn-cost-control
# ... 其他技能目录

# 3. 复制技能文件
cp -r ~/.openclaw/skills/cn-project-management/* skills/cn-project-management/
# ... 复制其他技能

# 4. 添加 README
cp dlh-skills/README.md ./
cp dlh-skills/README_en.md ./

# 5. 提交并推送
git add .
git commit -m "feat: 发布度量衡智库 OpenClaw 技能包"
git push origin main
```

### 方式三：使用脚本自动上传

```powershell
# 在 PowerShell 中运行
.\upload-to-github.ps1 -RepoOwner "ruiyongwang" -RepoName "dlh"
```

---

## 📝 文件说明

每个技能文件夹包含：

| 文件/目录 | 说明 |
|----------|------|
| `SKILL.md` | 技能主文件（包含中英文简介） |
| `references/` | 参考文档目录 |
| `scripts/` | 脚本文件目录 |
| `*.json` | 数据文件 |
| `*.py` | Python 脚本 |

---

## ✅ 检查清单

上传前请确认：

- [ ] 所有 SKILL.md 文件包含 `description`（中文简介）
- [ ] 所有 SKILL.md 文件包含 `description_en`（英文简介）
- [ ] 所有 SKILL.md 文件包含 `name_en`（英文名称）
- [ ] 所有技能文件夹结构完整
- [ ] README.md 已更新

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/ruiyongwang/dlh
- **OpenClaw 市场**: https://openclawmp.cc
- **个人主页**: https://openclawmp.cc/user/u-4018ff26e39e41559113

---

*度量衡智库 · 让复杂决策更简单*
