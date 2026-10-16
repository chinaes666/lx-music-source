import urllib.request
import re
import sys

# 你收集到的多个备选源候选链接（请确保每个 URL 都有闭合的双引号和末尾的逗号）
CANDIDATE_SOURCES = [
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/sixyin/latest.js",
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/huibq/latest.js",
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/flower/latest.js",
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/lx/latest.js",
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/changqing/latest.js",
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/huanyin/latest.js",
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/ikun/latest.js",
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/grass/latest.js",
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/juhe/latest.js",
    "https://raw.githubusercontent.com/pdone/lx-music-source/main/qdy/latest.js"
]

def validate_and_filter_sources():
    valid_contents = []
    
    print("开始进行 LX Music 自定义源的精准结构校验...")
    
    for i, url in enumerate(CANDIDATE_SOURCES):
        print(f"正在检测第 {i+1} 个源: {url}")
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                content = response.read().decode('utf-8', errors='ignore')
                
                # 1. 基础防呆：如果内容包含 HTML 标签（说明可能误抓了 404 页面或安全拦截页），直接判定无效
                if '<html' in content.lower() or '<body' in content.lower():
                    print(f" -> [无效] 第 {i+1} 个源返回了 HTML 页面（可能链接失效或触发拦截），已过滤。")
                    continue
                
                # 2. 精准结构校验：
                has_search = re.search(r'search\s*[:\(]', content)
                has_music_url = re.search(r'getMusicUrl|musicUrl|url', content)
                
                if has_search and has_music_url:
                    print(f" -> [通过] 第 {i+1} 个源通过精准结构校验。")
                    valid_contents.append(f"\n// --- Validated Source {i+1} ---\n" + content + "\n")
                else:
                    print(f" -> [不符合规范] 第 {i+1} 个源缺少必要的 API 结构，已剔除。")
                    
        except Exception as e:
            print(f" -> [失效] 第 {i+1} 个源请求发生异常 ({e})，已自动剔除。")
            
    if not valid_contents:
        print("错误：经过精准校验，没有发现任何符合 LX Music 规范的有效源！")
        sys.exit(1)
        
    # 将所有通过校验的健康源合并写入 source.js
    final_content = "".join(valid_contents)
    with open('source.js', 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"成功：精准筛选并合并了 {len(valid_contents)} 个可用源，已生成最终的 source.js！")

if __name__ == '__main__':
    validate_and_filter_sources()
