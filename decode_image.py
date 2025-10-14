"""快速解码 base64 图片"""

import base64
import json
from pathlib import Path

# 读取 JSON 文件（修改为你的文件路径）
json_file = input("请输入 JSON 文件路径（或直接拖拽文件到这里）: ").strip('"')

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
    output_file = "generated_image.png"
    Path(output_file).write_bytes(image_bytes)

    print(f"[成功] 图片已保存到: {output_file}")
    print(f"[信息] 图片大小: {len(image_bytes)} 字节 ({len(image_bytes) / 1024 / 1024:.2f} MB)")

except FileNotFoundError:
    print(f"[错误] 找不到文件: {json_file}")
except json.JSONDecodeError:
    print("[错误] 文件不是有效的 JSON 格式")
except Exception as e:
    print(f"[错误] {e}")
