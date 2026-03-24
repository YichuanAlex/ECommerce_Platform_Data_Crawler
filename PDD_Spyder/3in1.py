from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
import random, os, json
from uuid import uuid4

# === 步骤 0：配置路径 ===
excel_path = "/Users/jiangzixi/Downloads/319_2025_06_26_09_45_42.xlsx"
output_dir = "/Users/jiangzixi/Downloads/PDD_Spyder/"
os.makedirs(output_dir, exist_ok=True)

# === 步骤 1：生成随机用户目录并扫码登录 ===
temp_profile = f"/Users/jiangzixi/Downloads/pdd_user_profile_{uuid4().hex[:8]}"
os.makedirs(temp_profile, exist_ok=True)

ua_list = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 Chrome/103.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]
ua = random.choice(ua_list)

with sync_playwright() as p:
    print("🧭 启动浏览器，请扫码登录 PDD...")
    browser = p.webkit.launch_persistent_context(
        user_data_dir=temp_profile,
        headless=False,
        viewport={"width": 375, "height": 667},
        user_agent=ua,
        locale="zh-CN"
    )
    page = browser.new_page()
    page.goto("https://mobile.yangkeduo.com/")
    page.wait_for_timeout(3000)
    page.evaluate("localStorage.clear(); sessionStorage.clear();")

    print("👉 请扫码登录（新身份）")
    page.wait_for_timeout(60000)
    print("✅ 登录完成，cookie 已保存在：", temp_profile)
    browser.close()

# === 步骤 2：读取商品 ID，批量访问商品页面并保存 HTML ===
df = pd.read_excel(excel_path)
if '商品ID' in df.columns:
    goods_ids = df['商品ID'].dropna().astype(int).tolist()
else:
    raise ValueError("Excel 中缺少 '商品ID' 列")

with sync_playwright() as p:
    browser = p.webkit.launch_persistent_context(
        user_data_dir=temp_profile,
        headless=True,
        viewport={"width": 375, "height": 667},
        user_agent=ua
    )
    page = browser.new_page()

    for goods_id in goods_ids:
        try:
            url = f"https://mobile.yangkeduo.com/goods.html?goods_id={int(goods_id)}"
            page.goto(url)
            page.wait_for_timeout(5000)

            img_element = page.query_selector('img')
            img_src = img_element.get_attribute('src') if img_element else None
            if img_src and "blank.png" in img_src:
                print(f"⚠️ 跳过不存在的商品: {goods_id}")
                continue

            file_path = os.path.join(output_dir, f"{goods_id}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(page.content())
            print(f"✅ 已保存 HTML: {file_path}")
        except Exception as e:
            print(f"❌ 错误处理商品 {goods_id}: {str(e)}")
    browser.close()

# === 步骤 3：提取 HTML 中的 window.rawData 并保存为 JSON ===
def process_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")

    script_tags = soup.find_all("script")
    target_script = None
    for tag in script_tags:
        if tag.string and "window.rawData" in tag.string:
            target_script = tag.string
            break

    json_obj = {}
    if target_script:
        try:
            start_marker = "window.rawData="
            start_index = target_script.find(start_marker)
            if start_index != -1:
                start_index += len(start_marker)
                end_index = target_script.find("};", start_index)
                if end_index != -1:
                    raw_json = target_script[start_index:end_index+1]
                    json_obj = json.loads(raw_json)
        except Exception as e:
            json_obj = {"error": f"Failed to parse rawData JSON: {str(e)}"}

    file_dir, file_name = os.path.split(file_path)
    base_name, _ = os.path.splitext(file_name)
    output_path = os.path.join(file_dir, f"{base_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, indent=4, ensure_ascii=False)
    return output_path

output_paths = []
for filename in os.listdir(output_dir):
    if filename.endswith(".html"):
        file_path = os.path.join(output_dir, filename)
        output_path = process_html_file(file_path)
        output_paths.append(output_path)

print("\n📦 所有 JSON 文件已保存：")
for path in output_paths:
    print("📝", path)
