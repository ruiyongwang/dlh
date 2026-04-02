---
name: jimeng-ai
name_en: jimeng-ai
description: 即梦AI（字节跳动旗下）图像和视频生成工具。基于火山引擎API，提供文生图、图生图、视频生成、数字人等功能。适用于需要AI生成配图、视频封面的场景。
description_en: JIMENG AI (ByteDance) image and video generation tool based on Volcano Engine API. Supports text-to-image, image-to-image, video generation, and digital humans. Perfect for AI-generated illustrations and video thumbnails.
version: 1.0
author: 度量衡智库
author_en: Duliangheng Think Tank
category: ai
category_en: AI Tools
---

# 即梦AI - 图像视频生成

## 概述

即梦AI是字节跳动旗下的AI创作工具，通过火山引擎开放API服务。支持：
- **文生图**：文字描述生成图片（支持3.0/3.1/4.0版本）
- **图生图**：参考原图生成新图片
- **智能超清**：提升图片分辨率
- **视频生成**：文生视频、图生视频
- **数字人**：照片+音频生成说话视频

## 前置条件

### 1. 火山引擎账号

访问 https://console.volcengine.com 注册账号

### 2. 获取API密钥

1. 登录火山引擎控制台
2. 进入「访问控制」→ 「凭证管理」
3. 创建 Access Key 和 Secret Key

### 3. 开通服务

在控制台开通「视觉智能」- 「即梦AI」相关服务

### 4. 配置凭证

创建文件 `C:\Users\wry08\.config\jimeng\credentials.ini`:

```ini
[volcengine]
access_key = 您的AccessKey
secret_key = 您的SecretKey
region = cn-north-1
```

## 使用方法

### 方式一：使用封装脚本

```powershell
# 文生图（基础版）
.\scripts\jimeng_text2image.ps1 -Prompt "商务人士握手，蓝白色调" -AspectRatio "16:9"

# 图生图
.\scripts\jimeng_image2image.ps1 -ImagePath "C:\test.jpg" -Prompt "换成秋天场景"

# 智能超清
.\scripts\jimeng_upscale.ps1 -ImagePath "C:\test.jpg"

# 视频生成
.\scripts\jimeng_text2video.ps1 -Prompt "海浪拍打岩石"
```

### 方式二：直接调用Python脚本

```powershell
python scripts/jimeng_api.py text2image --prompt "..." --output result.jpg
python scripts/jimeng_api.py image2image --input test.jpg --prompt "..." --output result.jpg
```

## 脚本说明

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `jimeng_text2image.ps1` | 文生图 | -Prompt, -AspectRatio, -OutputPath |
| `jimeng_image2image.ps1` | 图生图 | -ImagePath, -Prompt, -OutputPath |
| `jimeng_upscale.ps1` | 智能超清 | -ImagePath, -Scale, -OutputPath |
| `jimeng_text2video.ps1` | 文生视频 | -Prompt, -Duration, -OutputPath |
| `jimeng_api.py` | Python通用接口 | 支持所有功能 |

## 文生图参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| prompt | 图像描述 | 必填，中英文均可 |
| width | 宽度 | 512-2048 |
| height | 高度 | 512-2048 |
| image_num | 生成数量 | 1-4 |
| ratio | 宽高比 | 1:1, 4:3, 3:2, 16:9, 21:9 |
| model_version | 模型版本 | general-v3.0, general-v3.1, general-v4.0 |

## 推荐提示词模板

### 商事调解主题
```
现代简约风格，两个商务人士在天平图标前握手签约，蓝白色调，扁平设计风格，包含文件、建筑物元素，柔和渐变背景，适合社交媒体配图
```

### 工程咨询主题
```
专业商务场景，工程师查看图纸，城市背景，现代建筑，清晨光线，蓝色主色调，专业严谨风格
```

### 法律服务主题
```
法律天平，庄严稳重，金色光芒，蓝色背景，现代简约风格，适合海报设计
```

## 输出位置

生成的图片/视频保存在：
- 图片：`C:\Users\wry08\.workbuddy\outputs\jimeng\`
- 视频：`C:\Users\wry08\.workbuddy\outputs\jimeng\videos\`

## 注意事项

1. API调用会产生费用，具体价格见火山引擎控制台
2. 4K超清输出需要开通相应服务
3. 视频生成任务为异步，脚本会自动轮询直到完成
4. 如遇API错误，检查凭证配置和网络连接

## 常见问题

**Q: 提示词用中文还是英文？**
A: 即梦AI对中文支持较好，直接使用中文即可。

**Q: 生成失败怎么办？**
A: 检查提示词是否包含敏感词，或尝试简化描述。

**Q: 如何查看API调用记录？**
A: 登录火山引擎控制台 → 视觉智能 → 调用统计
