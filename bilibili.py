from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
from PIL import Image
import os


def login(username, password):
    """模拟登录并且获得两张验证码

    Args:
        username (str): 用户名
        password (str): 密码
    """
    # 构造浏览器登录bilibili登录界面
    wb = webdriver.Chrome(executable_path=r"D:\下载安装包文件\chromedriver.exe")
    wb.maximize_window()
    wb.get("https://passport.bilibili.com/login")

    try:
        # 等待用户名输入框加载完成
        username_input = WebDriverWait(wb, 10).until(
            EC.presence_of_element_located((By.ID, "login-username"))
        )
        username_input.send_keys(username)

        # 密码输入框和登录按钮的定位与操作
        password_input = wb.find_element(By.ID, "login-passwd")
        password_input.send_keys(password)

        login_button = wb.find_element(By.XPATH, '//*[@id="geetest-wrap"]/ul/li[5]/a[1]')
        login_button.click()

        while True:
            # 等待滑动验证码加载完成
            full_picture = WebDriverWait(wb, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_img'))
            )

            # 保存和裁剪验证码图片
            save_screenshot(wb, 'full_picture.png')
            code_picture = crop_image('full_picture.png', (1107, 325, 1423, 517))
            code_picture.save('code.png')

            # 展示完整的验证码并保存图片
            show_full_captcha(wb)
            save_screenshot(wb, 'full_picture.png')
            code_picture = crop_image('full_picture.png', (1107, 325, 1423, 517))
            code_picture.save('code_full.png')

            # 获取滑动距离和滑动轨迹
            space = get_space('code_full.png', 'code.png')
            tracks = get_tracks(space)

            # 定位滑块并进行滑动操作
            slider = wb.find_element(By.CSS_SELECTOR, '.geetest_slider_button')
            slide_to_gap(wb, slider, tracks)

            # 等待2秒并检查登录是否成功
            time.sleep(2)
            check = wb.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[6]').get_attribute('style')
            if check == 'display: none;':
                print("Login successful!")
                break
            else:
                # 如果登录失败，点击刷新按钮并等待2秒
                refresh_button = wb.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[6]/div/div[2]/div/a[2]')
                refresh_button.click()
                time.sleep(2)
    finally:
        # 无论成功与否，最后关闭浏览器
        wb.quit()


def save_screenshot(driver, filename):
    """保存当前页面截图

    Args:
        driver (webdriver.Chrome): 浏览器驱动实例
        filename (str): 截图文件名
    """
    driver.save_screenshot(filename)


def crop_image(image_path, box):
    """裁剪图片

    Args:
        image_path (str): 图片文件路径
        box (tuple): 裁剪区域

    Returns:
        Image.Image: 裁剪后的图片对象
    """
    with Image.open(image_path) as img:
        cropped_img = img.crop(box)
    return cropped_img


def show_full_captcha(driver):
    """展示完整的验证码图片

    Args:
        driver (webdriver.Chrome): 浏览器驱动实例
    """
    captcha_elem = driver.find_element(By.CSS_SELECTOR, 'canvas.geetest_canvas_img')
    driver.execute_script("""
        arguments[0].setAttribute('style', '');
    """, captcha_elem)


def get_space(full_image_path, code_image_path):
    """获取滑动距离

    Args:
        full_image_path (str): 完整验证码图片路径
        code_image_path (str): 缺口验证码图片路径

    Returns:
        int: 滑动距离
    """
    global i
    picture1 = Image.open(full_image_path)
    picture2 = Image.open(code_image_path)
    threshold = 60
    left = 100
    for i in range(left, picture1.size[0]):
        for j in range(picture1.size[1]):
            rgb1 = picture1.load()[i, j]
            rgb2 = picture2.load()[i, j]
            res1 = abs(rgb1[0] - rgb2[0])
            res2 = abs(rgb1[1] - rgb2[1])
            res3 = abs(rgb1[2] - rgb2[2])
            if not (res1 < threshold and res2 < threshold and res3 < threshold):
                return i + 18  # 误差矫正
    return i + 18  # 如果没有识别出不同位置，则象征性的滑动，以刷新下一张验证码


def get_tracks(distance):
    """获取滑动轨迹

    Args:
        distance (int): 滑动距离

    Returns:
        dict: 滑动轨迹信息
    """
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 3 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-2, -2, -2, -2, -3, -3, -2, -5, -5, -4, -5, -10, -3, -4]
    return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}


def slide_to_gap(driver, slider, tracks):
    """滑动到缺口位置

    Args:
        driver (webdriver.Chrome): 浏览器驱动实例
        slider (webdriver.Chrome.find_element): 滑块元素
        tracks (dict): 滑动轨迹信息
    """
    ActionChains(driver).click_and_hold(slider).perform()
    for track in tracks['forward_tracks']:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
    time.sleep(0.5)
    for back_track in tracks['back_tracks']:
        ActionChains(driver).move_by_offset(xoffset=back_track, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=-3, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=3, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()


if __name__ == "__main__":
    username = 'your_username'
    password = 'your_password'
    login(username, password)
