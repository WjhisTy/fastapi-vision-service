"""简单解码脚本 - 将浏览器下载的 JSON 转为图片"""

import base64
import json
import sys
from pathlib import Path

# 默认查找浏览器下载的文件
default_files = [
    "response.json",  # 常见名称
    Path.home() / "Downloads" / "response.json",  # Windows 下载目录
    Path.home() / "Downloads" / "generate.json",
]

json_file = None

# 如果有命令行参数，使用它
if len(sys.argv) > 1:
    json_file = sys.argv[1]
else:
    # 尝试找到文件
    for f in default_files:
        if Path(f).exists():
            json_file = str(f)
            print(f"[找到] {json_file}")
            break

if not json_file:
    print("[提示] 请将浏览器下载的 JSON 文件拖到此脚本上，或运行:")
    print("       python decode_simple.py 你的文件.json")
    exit(1)

try:
    # 读取 JSON
    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)

    # 提取 base64
    image_base64 = data.get("image_base64", "")

    if not image_base64:
        print("[错误] JSON 中没有找到 'image_base64' 字段")
        exit(1)

    # 解码
    image_bytes = base64.b64decode(image_base64)

    # 保存图片
    output_file = "generated_cat.png"
    Path(output_file).write_bytes(image_bytes)

    print(f"[成功] 图片已保存到: {output_file}")
    print(f"[信息] 图片大小: {len(image_bytes) / 1024:.1f} KB")
    print("[信息] 分辨率: 768x1024")
    print("")
    print("[完成] 现在可以双击打开 generated_cat.png 查看图片了！")

except FileNotFoundError:
    print(f"[错误] 找不到文件: {json_file}")
except json.JSONDecodeError:
    print("[错误] 文件不是有效的 JSON 格式")
except Exception as e:
    print(f"[错误] {e}")
