import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time, os

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return uc.Chrome(options=options)

def generate_premium_html(content, exam_name):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; margin: 0; padding-bottom: 70px; }}
            .header {{ background: #007bff; color: white; padding: 15px; display: flex; justify-content: space-between; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .q-card {{ background: white; margin: 15px; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .sol-btn {{ background: #28a745; color: white; border: none; width: 100%; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; margin-top: 10px; }}
            .solution {{ display: none; background: #f8f9fa; padding: 15px; border-left: 5px solid #28a745; margin-top: 10px; border-radius: 5px; }}
            .footer {{ position: fixed; bottom: 0; width: 100%; background: white; text-align: center; padding: 15px; border-top: 1px solid #ddd; font-size: 14px; }}
            .footer a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
            [lang="hi"] {{ display: none; }}
        </style>
    </head>
    <body>
        <div class="header">
            <span><b>{exam_name} - ArjunBotz</b></span>
            <button onclick="toggleLang()" style="border-radius:20px; border:none; padding:5px 15px; cursor:pointer; font-weight:bold; background:white; color:#007bff;">HI / EN</button>
        </div>
        <div class="container">{content}</div>
        <div class="footer">
            Developed by <a href="{CHANNEL_LINK}">ArjunBotz</a> | Extracted by <a href="{ADMIN_LINK}">Arjun Dubey</a>
        </div>
        <script>
            function toggleLang() {{
                const en = document.querySelectorAll('[lang="en"]');
                const hi = document.querySelectorAll('[lang="hi"]');
                const isEn = en[0].style.display !== 'none';
                en.forEach(e => e.style.display = isEn ? 'none' : 'block');
                hi.forEach(e => e.style.display = isEn ? 'block' : 'none');
            }}
            function showSol(btn) {{
                const s = btn.nextElementSibling;
                s.style.display = s.style.display === 'block' ? 'none' : 'block';
                btn.innerText = s.style.display === 'block' ? 'Hide Analysis' : 'View Solution & Analysis';
            }}
        </script>
    </body>
    </html>
    """

def run_extraction(email, password, url, exam):
    driver = get_driver()
    try:
        driver.get("https://www.oliveboard.in/login/")
        time.sleep(3)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-btn").click()
        time.sleep(8)
        driver.get(url)
        time.sleep(10)
        
        # Mock HTML structure (Actual Scraping logic here)
        mock_content = '<div class="q-card"><p lang="en"><b>Q.</b> Sample Question Text?</p><p lang="hi"><b>प्रश्न.</b> नमूना प्रश्न?</p><button class="sol-btn" onclick="showSol(this)">View Solution & Analysis</button><div class="solution"><p lang="en">Explanation...</p><p lang="hi">विवरण...</p></div></div>'
        
        filename = f"@ArjunBotz_OliveBoard_Mock_{exam}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(generate_premium_html(mock_content, exam))
        return filename
    finally:
        driver.quit()
