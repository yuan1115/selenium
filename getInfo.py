# coding:utf-8
import os
import sys
import time
from selenium import webdriver

# 邮箱登录


def emaillogin(browser, username, password):
    browser.find_element_by_css_selector(".other-type").click()
    browser.find_element_by_css_selector(".email-input").send_keys(username)
    browser.find_element_by_css_selector(".password-input").send_keys(password)
    browser.find_element_by_css_selector('.btnLogin').click()

# qq登录


def qqlogin(browser, username, password):
    browser.find_element_by_css_selector(".login-type-qq").click()
    browser.switch_to_frame(browser.find_elements_by_tag_name("iframe")[0])
    browser.find_element_by_id("switcher_plogin").click()
    browser.find_element_by_id("u").send_keys(username)
    browser.find_element_by_id("p").send_keys(password)
    browser.find_element_by_id('login_button').click()

# 判断登录方式


def login(browser, username, password):
    if username.isdigit() == True & len(username) < 11:
        qqlogin(browser, username, password)
    else:
        emaillogin(browser, username, password)

# 判断记录文件是否存在


def isexists(accounnt):
    if os.path.exists('完成.txt') == False:
        open("完成.txt", 'w').close()
    else:
        f = open('完成.txt').read().split()
        if accounnt in f:
            print('{}已存在'.format(accounnt))
            return 1
    if os.path.exists('异常.txt') == False:
        open("异常.txt", 'w').close()
    else:
        f = open('异常.txt').read().split()
        if accounnt in f:
            print('账号{}异常'.format(accounnt))
            return 1
    print('开始获取账号信息---->{}'.format(accounnt))

# 写入账户信息


def writeInfo(name, strs):
    rePath = sys.path[0]+"\\"+"提取信息"+'\\'+name
    if os.path.exists(rePath) == False:
        os.makedirs(rePath)
    userInfo = rePath+"\\"+"账户信息.txt"
    fp = open(userInfo, 'w')
    fp.write(strs)

# 截图保存


def downImg(browser, data):
    for i in data:
        if i['url']:
            browser.get("https:"+i['url'])
            time.sleep(0.5)
            browser.save_screenshot(
                "./提取信息/{}/{}.jpg".format(i['name'], i['filename']))

# 判断需要保存的记录文件


def isErrorW(accounnt, types=0):
    if types == 0:
        f = open("完成.txt", 'r')
        re = f.read()+accounnt+"\n"
        f.close()
        f = open("完成.txt", 'w')
        f.write(re)
        f.close()
    else:
        f = open("异常.txt", 'r')
        re = f.read()+accounnt+"\n"
        f.close()
        f = open("异常.txt", 'w')
        f.write(re)
        f.close()

# 主函数


def getInfo(username, password):
    isexist = isexists(username)
    if isexist == 1:
        return 1
    try:
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        browser = webdriver.Chrome(chrome_options=option)
        browser.get("https://om.qq.com")
        login(browser, username, password)
        print("开始登录")
        time.sleep(0.5)
        print("开始获取账号信息")
        browser.find_element_by_css_selector(
            ".accountSettings").click()
        time.sleep(0.5)
        # 获取所需要的信息
        name = browser.find_element_by_css_selector(
            ".name").text  # 企鹅号名称
        posturephoto = browser.find_element_by_id(
            "posturephoto").get_attribute("value")  # 手持
        idfrontphoto = browser.find_element_by_id(
            "idfrontphoto").get_attribute("value")  # 身份证正面
        id_name = browser.find_element_by_id(
            "id_name").get_attribute("value")  # 姓名
        id_number = browser.find_element_by_id(
            "id_number").get_attribute("value")  # 身份证号
        tel = browser.find_element_by_id(
            "mobile").get_attribute("value")  # 联系电话
        email = browser.find_element_by_id(
            "email").get_attribute("value")  # 邮箱
        zzcode = browser.find_element_by_id(
            "organization_code").get_attribute("value")  # 组织机构代码
        orgcode_photo = browser.find_element_by_id(
            "orgcode_photo").get_attribute("value")  # 组织扫描件
        organization = browser.find_element_by_id(
            "organization").get_attribute("value")  # 组织名称
        enterprise = browser.find_element_by_id(
            "enterprise").get_attribute("value")  # 企业名称
        enterprise_license = browser.find_element_by_id(
            "enterprise_license").get_attribute("value")  # 企业营业执照注册号
        strs = "登录账号：{}\n密码：{}\n企鹅号昵称：{}\n手持身份证图片链接：{}\n身份证正面图链接：{}\n姓名：{}\n身份证号：{}\n联系电话：{}\n邮箱:{}\n组织机构代码：{}\n组织扫描件链接：{}\n组织名称：{}\n企业名称：{}\n企业营业执照注册号：{}\n".format(username, password, name, posturephoto, idfrontphoto, id_name, id_number,
                                                                                                                                                                     tel, email, zzcode, orgcode_photo, organization, enterprise, enterprise_license)
        writeInfo(name, strs)
        data = [
            {"url": posturephoto, "name": name, "filename": "手持"},
            {"url": idfrontphoto, "name": name, "filename": "身份证正面"},
            {"url": orgcode_photo, "name": name, "filename": "组织扫描件"},
        ]
        downImg(browser, data)
        isErrorW(username)
    except BaseException:
        print('账号异常跳过')
        isErrorW(username, 1)
        browser.close()


if __name__ == "__main__":
    usrPwdL = open('账号.txt', encoding='utf-8').read().split()
    for i in usrPwdL:
        info = i.split(";")
        re = getInfo(info[0], info[1])
        if re == 1:
            continue
        else:
            time.sleep(0.5)
else:
    pass
