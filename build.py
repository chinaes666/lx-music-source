import urllib.request
import sys

# 远程源地址（这里以某个公开的、维护中的 LX Music 自定义源原始链接为例，你也可以换成你自己的源地址）
SOURCE_URL = "https://raw.githubusercontent.com/example/lx-music-source/main/source.js"

def build_source():
    print(f"正在从远端拉取音源规则: {SOURCE_URL}")
    try:
        # 请求远端脚本内容
        req = urllib.request.Request(
            SOURCE_URL,
                headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            source_content = response.read().decode('utf-8')
            
        # 简单校验内容是否为空
        if not source_content.strip():
            print("错误：获取到的音源内容为空！")
            sys.exit(1)
            
        # 写入本地根目录的 source.js
        with open('source.js', 'w', encoding='utf-8') as f:
            f.write(source_content)
            
        print("成功：source.js 已生成并更新！")
        
    except Exception as e:
        print(f"构建失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    build_source()
