import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def crawl_pdd_product_info_with_cookie(goods_id, save_path, cookie_path):
    # 设置 Edge 浏览器选项（非无头，方便调试）
    options = webdriver.EdgeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")
    options.binary_location = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

    # 启动浏览器
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

    try:
        # 先访问首页以设置 domain
        driver.get("https://mobile.yangkeduo.com/index.html?refer_page_name=live_tab&refer_page_id=71837_1750859464995_nr5iiru3qu&refer_page_sn=71837&page_id=10002_1750859466173_uk9gubclvn&is_back=1&bsch_is_search_mall=&bsch_show_active_page=")

        # 读取 cookie 并添加到浏览器中
        with open(cookie_path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        for cookie in cookies:
            # Selenium 的 cookie 格式要求必须含有 name 和 value
            if 'sameSite' in cookie:
                del cookie['sameSite']
            driver.add_cookie(cookie)

        # 访问商品页面
        url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
        driver.get(url)

        time.sleep(5)  # 等待页面加载完毕

        # 获取页面源码
        page_source = driver.page_source

        # 解析嵌入的 JSON 数据（注意这只是示例，需要你根据实际 HTML 调整）
        start_marker = "window.rawData="
        end_marker = "</script>"

        start_index = page_source.find(start_marker)
        if start_index != -1:
            start_index += len(start_marker)
            end_index = page_source.find(end_marker, start_index)
            if end_index != -1:
                json_data = page_source[start_index:end_index].strip().rstrip(';')
                try:
                    product_info = json.loads(json_data)
                    with open(save_path, 'w', encoding='utf-8') as json_file:
                        json.dump(product_info, json_file, indent=4, ensure_ascii=False)
                    print(f"✅ 商品信息已保存至 {save_path}")
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
            else:
                print("❌ 未找到结束标记")
        else:
            print("❌ 页面中未找到嵌入的商品 JSON 数据")

    except Exception as e:
        print(f"❌ 爬取过程中出错: {e}")
    finally:
        driver.quit()

# === 调用 ===
goods_id = "363809823554"
save_path = "/Users/jiangzixi/Downloads/363809823554.json"
cookie_path = "/Users/jiangzixi/Downloads/pdd_cookies.json"

crawl_pdd_product_info_with_cookie(goods_id, save_path, cookie_path)





'''
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import json

# 创建浏览器实例（非无头模式，方便手动扫码登录）
options = webdriver.EdgeOptions()
# 不加 --headless，这样你可以扫码登录
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,800")

# 如果你使用的是 macOS Edge，可手动设置路径（否则注释掉）
options.binary_location = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

# 启动浏览器
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

try:
    # 打开拼多多首页
    driver.get("https://mobile.yangkeduo.com/")
    
    # 给你时间手动扫码登录
    print("👉 请在浏览器中完成登录操作（扫码或其他方式）...")
    time.sleep(60)  # 等待 60 秒（你可以改成更长）

    # 登录完成后，获取 cookies
    cookies = driver.get_cookies()
    
    # 保存 cookies 到本地文件
    with open("pdd_cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=4, ensure_ascii=False)
    print("✅ 登录 cookies 已保存为 pdd_cookies.json")

finally:
    driver.quit()
'''
