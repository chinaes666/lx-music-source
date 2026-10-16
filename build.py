import urllib.request
import sys

# 备选源链接列表
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

def download_and_merge_sources():
    valid_contents = []
    
    print("开始拉取并合并 LX Music 自定义源（已启用 UTF-8 强编码保护）...")
    
    for i, url in enumerate(CANDIDATE_SOURCES):
        print(f"正在拉取第 {i+1} 个源: {url}")
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                # 关键修复：强制使用 utf-8 解码，并忽略无法识别的非法字节，防止乱码
                raw_bytes = response.read()
                content = raw_bytes.decode('utf-8', errors='ignore')
                
                # 1. 防呆校验：排除网页拦截页、404或空内容
                if '<html' in content.lower() or '<body' in content.lower() or len(content.strip()) < 50:
                    print(f" -> [无效] 第 {i+1} 个源返回了网页或内容为空，已过滤。")
                    continue
                
                print(f" -> [成功] 第 {i+1} 个源拉取有效，大小: {len(content)} 字符。")
                valid_contents.append(f"\n// --- Source {i+1} ---\n" + content + "\n")
                
        except Exception as e:
            print(f" -> [失效] 第 {i+1} 个源请求失败 ({e})，已自动跳过。")
            
    if not valid_contents:
        print("错误：所有源均拉取失败！")
        sys.exit(1)
        
    # 关键修复：写入文件时明确指定 encoding='utf-8'
    final_content = "".join(valid_contents)
    with open('source.js', 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"成功：共合并了 {len(valid_contents)} 个有效源，已生成无乱码的 source.js！")

if __name__ == '__main__':
    download_and_merge_sources()
