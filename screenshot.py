from playwright.sync_api import sync_playwright
import os

html_path = os.path.abspath("C:/Users/kerry/repos/mgmt675/docs/slides/m1-ai-in-finance.html")
url = "file:///" + html_path.replace("\\", "/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    # Load page and wait for embedded JS to fire (1.5s + 3s timers)
    page.goto(url + "#/chatbot")
    page.wait_for_timeout(5000)
    page.screenshot(path="C:/Users/kerry/repos/mgmt675/screenshot_chatbot.png")
    print("Chatbot saved")

    page.goto(url + "#/agent")
    page.wait_for_timeout(5000)
    page.screenshot(path="C:/Users/kerry/repos/mgmt675/screenshot_agent.png")
    print("Agent saved")

    page.goto(url + "#/past-present-and-future-of-personal-computing")
    page.wait_for_timeout(3000)
    page.screenshot(path="C:/Users/kerry/repos/mgmt675/screenshot_ui.png")
    print("UI saved")

    browser.close()
