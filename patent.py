import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from phone_login import *
from db import DbOperate
from Common import Common


class FunctionName(type):
    def __new__(cls, name, bases, attrs, *args, **kwargs):
        count = 0
        attrs["__Func__"] = []
        for k, v in attrs.items():
            # 专利
            if "patent_" in k:
                attrs["__Func__"].append(k)
                count += 1

        attrs["__FuncCount__"] = count
        return type.__new__(cls, name, bases, attrs)


class Execute(object, metaclass=FunctionName):
    def __init__(self):
        self.common = Common()
        self.timetemp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())  # 存储Excel表格文件名编号
        self.db = "case"
        self.dboperate = DbOperate()

    # 执行下单
    def execute_function(self, callback):
        try:
            eval("self.{}()".format(callback))
        except Exception as e:
            print("错误信息:", e)
            self.common.write_error_log(callback)
            time.sleep(0.5)
            self.common.write_error_log(str(e))


    # 1 发明专利,实用新型，同日申请
    def patent_invention_normal(self):
        all_type = [u'发明专利', u'实用新型', u'发明新型同日申请']
        type_code = ["invention", "shiyongxinxing", "tongrishenqing"]
        self.common.driver.get("https://m.zgg.com/shenqing/list.html?#zl")
        for index, patent_type in enumerate(all_type):
            if self.dboperate.exists(type_code[index]):
                try:
                    locator = (By.XPATH, "(.//div[@class='list-detail']/ul[5]/li[3]/a)")
                    WebDriverWait(self.common.driver, 30, 0.5).until(EC.element_to_be_clickable(locator))
                    # 专利申请
                    self.common.driver.find_element_by_xpath(".//div[@class='list-detail']/ul[1]/li[1]/a").click()
                    # 进入分类页面
                    self.common.driver.get("https://m.zgg.com/shenqing/{}.html?pro=1".format(type_code[index]))

                    for num in range(1, 8):
                        if self.dboperate.is_member(type_code[index], num):
                            print("num:", num)
                            # 服务类型选择，
                            if num < 4:
                                self.common.driver.find_element_by_xpath(
                                    ".//ul[@id='ulType']/li[{}]/a".format(num)).click()
                            elif num == 4:
                                self.common.driver.find_element_by_xpath(".//ul[@id='ulType']/li[1]/a").click()
                                self.common.driver.find_element_by_xpath(
                                    "(.//div[@class='zgg-zlsq-sq-ul']/ul/li[1]/a)[2]").click()
                            elif num == 5:
                                self.common.driver.find_element_by_xpath(".//ul[@id='ulType']/li[2]/a").click()
                                self.common.driver.find_element_by_xpath(
                                    "(.//div[@class='zgg-zlsq-sq-ul']/ul/li[1]/a)[2]").click()
                            elif num == 6:
                                time.sleep(0.5)
                                self.common.driver.find_element_by_xpath(".//ul[@id='ulType']/li[3]/a").click()
                                self.common.driver.find_element_by_xpath(
                                    "(.//div[@class='zgg-zlsq-sq-ul']/ul/li[1]/a)[2]").click()
                            else:
                                self.common.driver.find_element_by_xpath(".//li[@id='liguarantee']/a").click()
                            # 数量加1
                            # self.common.number_add()
                            # 数量减1
                            # # self.common.number_minus()
                            # 判断价格是否加载成功
                            while not self.common.driver.find_element_by_id("totalfee").is_displayed():
                                time.sleep(0.5)
                            # 获取详情页 价格
                            detail_price = self.common.driver.find_element_by_xpath(
                                "(.//label[@id='totalfee'])").text
                            print("详情页价格", detail_price)

                            self.common.apply_now()
                            # 获取下单页价格
                            case_name, case_number, case_price, totalprice = self.common.commit_order()
                            all_info = [case_name, case_number, detail_price, case_price, totalprice]
                            self.common.row = self.common.row + 1
                            time.sleep(0.5)
                            pay_totalprice = self.common.pay()
                            all_info.append(pay_totalprice)
                            print(all_info, pay_totalprice)
                            if float(all_info[2]) == float(all_info[3]) and float(all_info[2]) == float(
                                    pay_totalprice) and \
                                    float(all_info[4]) == float(all_info[2]):
                                status = 'True'
                            else:
                                status = "False"
                            all_info.append(status)
                            self.common.excel_number(all_info)
                            time.sleep(1)
                            self.common.driver.back()
                            self.common.driver.back()
                            self.common.driver.back()
                            screen_name = "_".join([case_name, case_number, case_price])
                            # self.common.qr_shotscreen(screen_name)
                            self.dboperate.del_elem(type_code[index], num)
                            print("{}{}执行结束".format(type_code[index], num))
                            time.sleep(1)
                except Exception as e:
                    print(e)
                    self.common.driver.get("https://m.zgg.com/shenqing/list.html?#zl")
                time.sleep(1)

