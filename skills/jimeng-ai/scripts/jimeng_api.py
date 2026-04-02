#!/usr/bin/env python3
"""
即梦AI API 调用脚本
基于火山引擎视觉智能服务

用法:
    python jimeng_api.py text2image --prompt "描述" --output result.jpg
    python jimeng_api.py image2image --input test.jpg --prompt "描述" --output result.jpg
    python jimeng_api.py upscale --input test.jpg --output result.jpg
"""

import json
import os
import sys
import time
import base64
import argparse
import configparser
import requests
from pathlib import Path
import hashlib
import hmac
from datetime import datetime

# 配置
CONFIG_PATH = os.path.expanduser("~/.config/jimeng/credentials.ini")
API_HOST = "visual.volcengineapi.com"
API_REGION = "cn-north-1"
SERVICE = "cv"

# 输出目录
OUTPUT_DIR = Path(os.path.expanduser("~/.workbuddy/outputs/jimeng"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR = OUTPUT_DIR / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


def load_credentials():
    """加载凭证"""
    config = configparser.ConfigParser()
    
    # 检查配置目录
    config_path = os.path.expanduser("~/.config/jimeng/credentials.ini")
    if not os.path.exists(config_path):
        # 尝试用户workbuddy目录
        alt_path = os.path.expanduser("~/.workbuddy/jimeng_credentials.ini")
        if os.path.exists(alt_path):
            config_path = alt_path
        else:
            print(f"错误: 找不到凭证文件")
            print(f"请在以下位置创建配置文件: {config_path}")
            print("[volcengine]")
            print("access_key = 您的AccessKey")
            print("secret_key = 您的SecretKey")
            sys.exit(1)
    
    config.read(config_path, encoding='utf-8')
    
    if 'volcengine' not in config:
        print("错误: 配置文件缺少 [volcengine] 部分")
        sys.exit(1)
    
    return config['volcengine']['access_key'], config['volcengine']['secret_key']


def sign_request(method, uri, params, headers, secret_key):
    """生成火山引擎签名"""
    # 简化版本：使用Authorization header
    timestamp = headers.get('X-Date', '')
    
    # 简化签名（实际生产环境请使用完整的签名算法）
    string_to_sign = f"{method}{uri}"
    signature = base64.b64encode(hmac.new(
        secret_key.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()).decode('utf-8')
    
    return signature


def get_auth_headers(access_key, secret_key):
    """获取认证头"""
    now = datetime.utcnow()
    timestamp = now.strftime('%Y%m%dT%H%M%SZ')
    
    headers = {
        'X-Date': timestamp,
        'X-Content-Sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'Content-Type': 'application/json',
    }
    
    # 简化认证（实际生产环境使用完整签名）
    auth = f"HMAC-SHA256 Credential={access_key}/2022-08-31/{SERVICE}/request, SignedHeaders=content-type;host;x-content-sha256;x-date, Signature="
    
    return headers, auth


def call_api(action, version, payload, access_key, secret_key):
    """调用API"""
    headers, auth = get_auth_headers(access_key, secret_key)
    
    # 构造请求
    uri = f"/?Action={action}&Version={version}"
    url = f"https://{API_HOST}{uri}"
    
    headers['Authorization'] = auth
    
    # 打印请求信息（调试用）
    print(f"调用API: {action}")
    print(f"URL: {url}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if result.get('code') == 10000 or result.get('status') == 10000:
            return result.get('data', {})
        else:
            print(f"API错误: {result}")
            return None
            
    except Exception as e:
        print(f"请求错误: {e}")
        return None


def text2image(prompt, width=1024, height=1024, image_num=1, ratio="1:1", model_version="general-v3.1", output=None):
    """文生图"""
    print(f"正在生成图片: {prompt}")
    
    access_key, secret_key = load_credentials()
    
    # 解析宽高比
    ratio_map = {
        "1:1": (1024, 1024),
        "4:3": (1472, 1104),
        "3:2": (1584, 1056),
        "16:9": (1664, 936),
        "21:9": (2016, 864),
    }
    
    if ratio in ratio_map:
        width, height = ratio_map[ratio]
    
    # 模型版本映射
    model_map = {
        "general-v3.0": "general-v3.0",
        "general-v3.1": "general-v3.1", 
        "general-v4.0": "general-v4.0",
    }
    
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "image_num": image_num,
        "model_version": model_map.get(model_version, "general-v3.1"),
    }
    
    data = call_api("CVMattingSubmitTask", "2022-08-31", payload, access_key, secret_key)
    
    if not data:
        print("生成失败")
        return None
    
    # 异步任务，轮询结果
    task_id = data.get('task_id')
    if not task_id:
        # 有些API是同步返回的
        image_urls = data.get('image_urls', [])
        if image_urls:
            return download_image(image_urls[0], output)
        print(f"未知响应: {data}")
        return None
    
    # 轮询任务状态
    print(f"任务ID: {task_id}, 等待生成...")
    for i in range(60):
        time.sleep(2)
        status_data = query_task(task_id, access_key, secret_key)
        if status_data:
            status = status_data.get('status')
            print(f"状态: {status}")
            if status == 'done':
                image_urls = status_data.get('image_urls', [])
                if image_urls:
                    return download_image(image_urls[0], output)
                break
            elif status == 'failed':
                print("生成失败")
                break
    
    return None


def query_task(task_id, access_key, secret_key):
    """查询任务状态"""
    headers, auth = get_auth_headers(access_key, secret_key)
    
    url = f"https://{API_HOST}/?Action=CVTaskGet&Version=2022-08-31"
    payload = {"task_id": task_id}
    
    headers['Authorization'] = auth
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if result.get('code') == 10000:
            return result.get('data', {})
    except:
        pass
    
    return None


def image2image(input_image, prompt, output=None):
    """图生图"""
    print(f"正在处理图片: {prompt}")
    
    # 读取输入图片
    input_path = Path(input_image)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_image}")
        return None
    
    with open(input_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    access_key, secret_key = load_credentials()
    
    payload = {
        "prompt": prompt,
        "reference_image": {
            "data": image_data,
            "type": "base64"
        }
    }
    
    data = call_api("CVImageEditSubmitTask", "2022-08-31", payload, access_key, secret_key)
    
    if not data:
        print("处理失败")
        return None
    
    task_id = data.get('task_id')
    if not task_id:
        print(f"未知响应: {data}")
        return None
    
    print(f"任务ID: {task_id}, 等待处理...")
    for i in range(60):
        time.sleep(2)
        status_data = query_task(task_id, access_key, secret_key)
        if status_data:
            status = status_data.get('status')
            print(f"状态: {status}")
            if status == 'done':
                image_urls = status_data.get('image_urls', [])
                if image_urls:
                    return download_image(image_urls[0], output)
                break
            elif status == 'failed':
                print("处理失败")
                break
    
    return None


def upscale(input_image, scale=2, output=None):
    """智能超清"""
    print(f"正在提升清晰度...")
    
    input_path = Path(input_image)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {input_image}")
        return None
    
    with open(input_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    access_key, secret_key = load_credentials()
    
    payload = {
        "image": {"data": image_data, "type": "base64"},
        "scale": scale
    }
    
    data = call_api("CVSuperResolutionSubmitTask", "2022-08-31", payload, access_key, secret_key)
    
    if not data:
        print("处理失败")
        return None
    
    task_id = data.get('task_id')
    if not task_id:
        print(f"未知响应: {data}")
        return None
    
    print(f"任务ID: {task_id}, 等待处理...")
    for i in range(60):
        time.sleep(2)
        status_data = query_task(task_id, access_key, secret_key)
        if status_data:
            status = status_data.get('status')
            print(f"状态: {status}")
            if status == 'done':
                image_urls = status_data.get('image_urls', [])
                if image_urls:
                    return download_image(image_urls[0], output)
                break
            elif status == 'failed':
                print("处理失败")
                break
    
    return None


def download_image(url, output_path):
    """下载图片"""
    if not output_path:
        output_path = OUTPUT_DIR / f"jimeng_{int(time.time())}.jpg"
    else:
        output_path = Path(output_path)
    
    print(f"下载图片: {url}")
    
    try:
        response = requests.get(url, timeout=60)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"图片已保存: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"下载失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="即梦AI API 调用工具")
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 文生图
    txt2img = subparsers.add_parser('text2image', help='文生图')
    txt2img.add_argument('--prompt', '-p', required=True, help='图像描述')
    txt2img.add_argument('--width', '-w', type=int, default=1024, help='宽度')
    txt2img.add_argument('--height', '-H', type=int, default=1024, help='高度')
    txt2img.add_argument('--num', '-n', type=int, default=1, help='生成数量')
    txt2img.add_argument('--ratio', '-r', default='1:1', help='宽高比')
    txt2img.add_argument('--model', '-m', default='general-v3.1', help='模型版本')
    txt2img.add_argument('--output', '-o', help='输出文件路径')
    
    # 图生图
    img2img = subparsers.add_parser('image2image', help='图生图')
    img2img.add_argument('--input', '-i', required=True, help='输入图片路径')
    img2img.add_argument('--prompt', '-p', required=True, help='修改描述')
    img2img.add_argument('--output', '-o', help='输出文件路径')
    
    # 超清
    up = subparsers.add_parser('upscale', help='智能超清')
    up.add_argument('--input', '-i', required=True, help='输入图片路径')
    up.add_argument('--scale', '-s', type=int, default=2, help='放大倍数')
    up.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.command == 'text2image':
        text2image(
            args.prompt, args.width, args.height, 
            args.num, args.ratio, args.model, args.output
        )
    elif args.command == 'image2image':
        image2image(args.input, args.prompt, args.output)
    elif args.command == 'upscale':
        upscale(args.input, args.scale, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
