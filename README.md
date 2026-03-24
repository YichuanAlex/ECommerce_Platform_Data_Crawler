# E-Commerce Platform Data Crawler | 电商平台数据爬虫

<div align="center">

**Web Scraping Project | 网络爬虫项目**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-blue.svg)](https://playwright.dev/)

**Author | 作者**: YichuanAlex (Zixi Jiang)  
**Email | 邮箱**: jiangzixi1527435659@gmail.com  
**Last Updated | 最后更新**: 2026-03-24

</div>

---

## Overview | 项目概述

**English:**  
This project implements automated web scraping tools for e-commerce platforms (Pinduoduo, Eleme, Meituan) using Playwright and Selenium. The crawler extracts product information, user profiles, and transaction data while maintaining anti-detection measures through browser fingerprint randomization and persistent session management.

**中文:**  
本项目使用 Playwright 和 Selenium 实现电商平台（拼多多、饿了么、美团）的自动化网络爬虫。爬虫提取商品信息、用户画像和交易数据，同时通过浏览器指纹随机化和持久会话管理维持反检测措施。

---

## Features | 功能特性

**English:**
- Multi-platform support (Pinduoduo, Eleme, Meituan)
- Browser automation with Playwright and Selenium
- QR code login for authenticated scraping
- Anti-detection measures (UA rotation, fingerprint randomization)
- Batch HTML/JSON data extraction
- Persistent user profile management

**中文:**
- 多平台支持（拼多多、饿了么、美团）
- 使用 Playwright 和 Selenium 的浏览器自动化
- 用于认证爬取的二维码登录
- 反检测措施（UA 轮换、指纹随机化）
- 批量 HTML/JSON 数据提取
- 持久用户画像管理

---

## Project Structure | 项目结构

```
Spyder/
│
├── PDD_Spyder/                            # Pinduoduo crawler | 拼多多爬虫
│   ├── 3in1.py                            # Main crawler script | 主爬虫脚本
│   ├── selenium_test.py                   # Selenium testing | Selenium 测试
│   ├── playwright_test.py                 # Playwright testing | Playwright 测试
│   ├── demo/                              # HTML samples | HTML 样本
│   └── file/                              # JSON data files | JSON 数据文件
│
├── pdd_user_profile/                      # Pinduoduo user profiles | 拼多多用户画像
├── eleme_user_profile/                    # Eleme user profiles | 饿了么用户画像
└── meituan_user_profile/                  # Meituan user profiles | 美团用户画像
```

---

## Installation and Usage | 安装与使用

**English:**
```bash
# Install dependencies
pip install playwright selenium pandas beautifulsoup4
playwright install

# Run Pinduoduo crawler
cd PDD_Spyder
python 3in1.py
```

**中文:**
```bash
# 安装依赖
pip install playwright selenium pandas beautifulsoup4
playwright install

# 运行拼多多爬虫
cd PDD_Spyder
python 3in1.py
```

---

## License | 许可证

**English:**
This project is licensed under the MIT License.

**中文:**
本项目采用 MIT 许可证。

---

## Contact | 联系方式

**English:**
- **Author**: Zixi Jiang (YichuanAlex)
- **Email**: jiangzixi1527435659@gmail.com
- **GitHub**: https://github.com/YichuanAlex

**中文:**
- **作者**: 姜子溪 (YichuanAlex)
- **邮箱**: jiangzixi1527435659@gmail.com
- **GitHub**: https://github.com/YichuanAlex

---

## Keywords | 关键词

**English:**  
Web Scraping, E-Commerce, Playwright, Selenium, Automation, Data Collection, Pinduoduo, Eleme, Meituan

**中文:**  
网络爬虫、电子商务、Playwright、Selenium、自动化、数据采集、拼多多、饿了么、美团

---

<div align="center">

**Thank you for your interest in this project!**  
**感谢您对本项目的关注!**

⭐ **If you find this project helpful, please give it a star!**  
**如果您觉得本项目有帮助，请给个星星!**

</div>
