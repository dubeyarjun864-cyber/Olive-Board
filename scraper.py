import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import os

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    return driver

def extract_mock_data(email, password, mock_url):
    driver = get_driver()
    try:
        driver.get("https://www.oliveboard.in/login/")
        time.sleep(5)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-btn").click()
        time.sleep(8)
        
        driver.get(mock_url)
        time.sleep(10)
        page_source = driver.page_source
        
        file_name = f"@ArjunBotz_OliveBoard_Mock_{int(time.time())}.html"
        
        # Premium App-Style HTML Template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: sans-serif; background: #f4f7f6; margin: 0; }}
                .header {{ background: #007bff; color: white; padding: 15px; text-align: center; font-size: 20px; font-weight: bold; }}
                .container {{ padding: 20px; background: white; min-height: 80vh; }}
                .footer {{ text-align: center; padding: 20px; border-top: 2px solid #eee; }}
                .footer a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">@ArjunBotz Premium Mock</div>
            <div class="container">{page_source}</div>
            <div class="footer">
                Developed By: <a href="https://t.me/ArjunBotz">ArjunBotz</a><br>
                Extracted By: <a href="https://t.me/Arjun_Dubey">Arjun Dubey</a>
            </div>
        </body>
        </html>
        """
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html_template)
        return file_name
    finally:
        driver.quit()
