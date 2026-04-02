# 手动上传指南

## 方法一：使用 GitHub 网页上传

1. 访问 https://github.com/ruiyongwang/dlh
2. 点击 "uploading an existing file" 链接
3. 将 `dlh-skills` 文件夹中的所有内容拖拽到上传区域
4. 填写提交信息并点击 "Commit changes"

## 方法二：使用 Git 命令行

```bash
# 1. 克隆仓库（如果已有本地副本可跳过）
git clone https://github.com/ruiyongwang/dlh.git
cd dlh

# 2. 复制 skills 文件夹
cp -r /path/to/dlh-skills/* .

# 3. 提交并推送
git add .
git commit -m "feat: publish Duliangheng OpenClaw skills"
git push origin main
```

## 方法三：生成带权限的 Token

1. 访问 https://github.com/settings/tokens/new
2. 勾选 `repo` 权限
3. 生成 Token 后告诉我
4. 我将自动完成上传

---

**仓库地址:** https://github.com/ruiyongwang/dlh
