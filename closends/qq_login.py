def qq_binding(qq="1098427485", password="@zg.DILIGENCE.cn"):
    import time, os
    from selenium import webdriver

    # driver = webdriver.Chrome(executable_path="D:/Running_Software/chromedriver.exe") # 可视化界面
    driver = webdriver.PhantomJS(executable_path="D:/Running_Software/phantomjs.exe", service_log_path=os.path.devnull)

    driver.maximize_window()
    driver.get("https://qzone.qq.com")
    driver.implicitly_wait(5)

    driver.switch_to.frame("login_frame")
    driver.find_element_by_id("switcher_plogin").click()
    driver.find_element_by_id("u").clear()
    driver.find_element_by_id("u").send_keys(qq)
    driver.find_element_by_id("p").clear()
    driver.find_element_by_id("p").send_keys(password)
    driver.find_element_by_id("login_button").click()

    time.sleep(3)
    driver.implicitly_wait(3)

    status = (driver.current_url == 'https://user.qzone.qq.com/' + qq)
    print(status)
    driver.close()

if __name__ == "__main__":
    qq_binding()