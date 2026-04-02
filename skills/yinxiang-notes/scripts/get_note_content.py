#!/usr/bin/env python3
"""
获取印象笔记内容并生成大纲
用法: python get_note_content.py --guid "笔记GUID"
      python get_note_content.py --title "笔记标题"
"""
import sys
import os
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 设置环境变量
os.environ['EVERNOTE_TOKEN'] = os.getenv('EVERNOTE_TOKEN', 'S=s11:U=2bfbb1:E=19d56b38c07:C=19d32a705a0:P=1cd:A=en-devtoken:V=2:H=17fcb643321d9b6df99336b1cff8a758')
os.environ['EVERNOTE_NOTESTORE_URL'] = os.getenv('EVERNOTE_NOTESTORE_URL', 'https://app.yinxiang.com/shard/s11/notestore')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import thrift.transport.THttpClient as THttpClient
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import re

token = os.environ['EVERNOTE_TOKEN']
note_store_url = os.environ['EVERNOTE_NOTESTORE_URL']

# 连接
transport = THttpClient.THttpClient(note_store_url)
transport.setCustomHeaders({"Authorization": f"Bearer {token}"})
protocol = TBinaryProtocol.TBinaryProtocol(transport)
note_store = NoteStore.Client(protocol)


def get_note_by_title(title):
    """根据标题搜索笔记"""
    filter = NoteStore.NoteFilter()
    filter.words = title
    result_spec = NoteStore.NotesMetadataResultSpec(includeTitle=True)
    result = note_store.findNotesMetadata(token, filter, 0, 10, result_spec)
    for note in result.notes:
        if note.title == title:
            return note_store.getNote(token, note.guid, True, True, False, False)
    return None


def get_note_by_guid(guid):
    """根据 GUID 获取笔记"""
    return note_store.getNote(token, guid, True, True, False, False)


def extract_outline(content):
    """从 ENML 内容中提取大纲"""
    # 移除 ENML 标签
    text = re.sub(r'<[^>]+>', '\n', content)
    text = re.sub(r'\n+', '\n', text)
    text = text.strip()
    
    lines = text.split('\n')
    outline = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 识别标题行
        if line.startswith('#') or line.startswith('【') or line.endswith('】'):
            outline.append(line)
        elif any(kw in line for kw in ['一、', '二、', '三、', '四、', '五、', '（一）', '（二）', '1.', '2.', '3.']):
            outline.append(line)
        elif len(line) < 50 and line[0:1].isupper() == False and any(c in line for c in '：:'):
            outline.append(line)
    
    return outline[:20]  # 最多返回20条


def main():
    guid = None
    title = None
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--guid' and i + 1 < len(args):
            guid = args[i + 1]
            i += 2
        elif args[i] == '--title' and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        else:
            i += 1
    
    if not guid and not title:
        print("用法: python get_note_content.py --guid '笔记GUID'")
        print("       python get_note_content.py --title '笔记标题'")
        sys.exit(1)
    
    # 获取笔记
    if guid:
        note = get_note_by_guid(guid)
    else:
        note = get_note_by_title(title)
    
    if not note:
        print("❌ 未找到笔记")
        sys.exit(1)
    
    print("=" * 50)
    print(f"📝 标题: {note.title}")
    print(f"📓 GUID: {note.guid}")
    print(f"📅 创建: {note.created}")
    print(f"🔄 更新: {note.updated}")
    print("=" * 50)
    print()
    
    # 提取内容
    if note.content:
        # 移除 ENML 标签获取纯文本
        text = re.sub(r'<[^>]+>', '\n', note.content)
        text = re.sub(r'\n+', '\n', text)
        text = text.strip()
        
        print("【内容预览 (前1000字)】")
        print("-" * 40)
        preview = text[:1000]
        if len(text) > 1000:
            preview += "..."
        print(preview)
        print()
        
        # 生成大纲
        outline = extract_outline(note.content)
        if outline:
            print("【纲要】")
            print("-" * 40)
            for i, item in enumerate(outline, 1):
                print(f"{i}. {item}")
        else:
            print("【纲要】(无明确标题结构)")
            print("-" * 40)
            # 显示前5行作为概要
            lines = [l.strip() for l in text.split('\n') if l.strip()][:5]
            for i, item in enumerate(lines, 1):
                print(f"{i}. {item}")
    else:
        print("笔记内容为空")


if __name__ == '__main__':
    main()
