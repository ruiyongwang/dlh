#!/usr/bin/env python3
"""
印象笔记预览和大纲 - 封装脚本
用法: yinxiang_note_view.py --title "标题"
      yinxiang_note_view.py --guid "GUID"
"""
import subprocess
import sys
import os

# 获取脚本目录
script_dir = os.path.dirname(os.path.abspath(__file__))
main_script = os.path.join(script_dir, 'get_note_content.py')

# 构建命令
cmd = [sys.executable, main_script] + sys.argv[1:]
subprocess.run(cmd)
