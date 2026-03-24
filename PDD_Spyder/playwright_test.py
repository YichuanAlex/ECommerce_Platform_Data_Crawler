
from playwright.sync_api import sync_playwright

# 设置 profile 目录（用户数据将被保存到这里）
user_data_dir = "/Users/jiangzixi/Downloads/pdd_user_profile"

with sync_playwright() as p:
    # 使用 WebKit 模拟 iPhone 更接近拼多多移动端行为
    browser = p.webkit.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,  # 要扫码，所以不能无头
        viewport={"width": 375, "height": 667},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
    )

    page = browser.new_page()
    page.goto("https://mobile.yangkeduo.com/")
    print("👉 请在新打开的浏览器窗口中扫码登录拼多多")
    page.wait_for_timeout(60000)  # 等待60秒扫码（可改成更长）
    
    # 可选择保存一下当前页面
    with open("pdd_homepage.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print("✅ 登录完成后请关闭浏览器或按 Ctrl+C 退出")

    


'''
from playwright.sync_api import sync_playwright

goods_id = "363809823554"
user_data_dir = "/Users/jiangzixi/Downloads/pdd_user_profile"

with sync_playwright() as p:
    browser = p.webkit.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=True,  # 现在可以无头运行了
        viewport={"width": 375, "height": 667},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
    )

    page = browser.new_page()
    url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
    page.goto(url)

    page.wait_for_timeout(5000)  # 等待页面内容加载

    # 保存页面源码
    with open(f"/Users/jiangzixi/Downloads/{goods_id}.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print(f"✅ 商品页面源码已保存：/Users/jiangzixi/Downloads/{goods_id}.html")

'''


'''
import pandas as pd
from playwright.sync_api import sync_playwright

# 配置参数
excel_path = "/Users/jiangzixi/Downloads/319_2025_06_26_09_45_42.xlsx"
output_dir = "/Users/jiangzixi/Downloads/PDD_Spyder/"
user_data_dir = "/Users/jiangzixi/Downloads/pdd_user_profile_038d99c2"
base_url = "https://mobile.yangkeduo.com/goods.html?goods_id="

# 读取Excel文件中的所有商品ID
df = pd.read_excel(excel_path)
# 检查列名并获取商品ID
if '商品ID' in df.columns:
    goods_ids = df['商品ID'].dropna().astype(int).tolist()
else:
    print("错误：Excel文件中没有找到名为'商品ID'的列")
    goods_ids = []

with sync_playwright() as p:
    # 启动浏览器
    browser = p.webkit.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=True,  # 无头模式
        viewport={"width": 375, "height": 667},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
    )
    
    page = browser.new_page()
    
    for goods_id in goods_ids:
        try:
            # 构建完整URL并访问
            url = f"{base_url}{int(goods_id)}"
            page.goto(url)
            
            # 等待页面内容加载（可根据需要调整时间）
            page.wait_for_timeout(100000)
            
            # 检查是否为商品不存在页面
            img_element = page.query_selector('img')
            img_src = img_element.get_attribute('src') if img_element else None
            if img_src and "blank.png" in img_src:
                print(f"⚠️ 跳过不存在的商品: {goods_id}")
                continue
            
            # 保存页面源码
            file_path = f"{output_dir}{goods_id}.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(page.content())
            
            print(f"✅ 已保存: {file_path}")
            
        except Exception as e:
            print(f"❌ 错误处理商品 {goods_id}: {str(e)}")
            
    browser.close()
'''




'''
from playwright.sync_api import sync_playwright
import random, os
from uuid import uuid4

# 生成随机用户目录
temp_profile = f"/Users/jiangzixi/Downloads/pdd_user_profile_{uuid4().hex[:8]}"
os.makedirs(temp_profile, exist_ok=True)

# UA 列表
ua_list = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 Chrome/103.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]
ua = random.choice(ua_list)

with sync_playwright() as p:
    browser = p.webkit.launch_persistent_context(
        user_data_dir=temp_profile,
        headless=False,
        viewport={"width": 375, "height": 667},
        user_agent=ua,
        locale="zh-CN"
    )

    page = browser.new_page()
    
    # ✅ 先跳转到拼多多域名，再执行 JS
    page.goto("https://mobile.yangkeduo.com/")
    page.wait_for_timeout(3000)

    # ✅ 现在才可以安全执行清除本地存储
    page.evaluate("localStorage.clear(); sessionStorage.clear();")

    print("👉 请扫码登录（新身份）")
    page.wait_for_timeout(60000)

    with open("pdd_homepage.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    print("✅ 页面内容已保存，profile 路径为：", temp_profile)
'''