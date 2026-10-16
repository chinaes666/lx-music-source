import urllib.request
import sys

# 你的备选源列表（按你心仪的优先级排序）
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

def fetch_best_source():
    print("开始检测并挑选第一个可用的健康源...")
    
    for i, url in enumerate(CANDIDATE_SOURCES):
        print(f"正在尝试拉取第 {i+1} 个源: {url}")
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                raw_bytes = response.read()
                content = raw_bytes.decode('utf-8', errors='ignore')
                
                # 校验：排除网页拦截、404 或内容太短的文件
                if '<html' in content.lower() or '<body' in content.lower() or len(content.strip()) < 100:
                    print(f" -> [跳过] 该源内容异常或返回了网页。")
                    continue
                
                # 成功找到第一个健康的源！将其直接写入 source.js
                with open('source.js', 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"成功：已锁定并生成可用的 source.js（来自第 {i+1} 个源），大小: {len(content)} 字符。")
                return
                
        except Exception as e:
            print(f" -> [跳过] 请求失败 ({e})。")
            
    # 如果所有源都遍历失败
    print("错误：所有备选源均无法正常访问！")
    sys.exit(1)

if __name__ == '__main__':
    fetch_best_source()
