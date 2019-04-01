# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from mouse import move, click
import pickle
import base64
from zheye import zheye
from tools.yundama_requests import YDMHttp
from urllib import parse
import re
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # question的第一頁answer的請求url
    start_answer_url = 'ttps://www.zhihu.com/api/v4/questions/{0}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&offset={2}&limit={1}&sort_by=default&platform=desktop'

    def parse(self, response):
        """
                提取html 页面中的所有url并跟踪这些url进行下一步爬取
                如果提取的url 中格式为/question/xxx 就下载之后直接进入解析函数
            """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False,
                          all_urls)
        for url in all_urls:
            match_obj = re.match(r'(.*zhihu.com/question/(\d+))(/|$).*', url)
            if match_obj:
                # 如果提取到question相关页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(
                    request_url,
                    callback=self.parse_question,
                    meta={'zhihu_id': question_id})
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url)

    def parse_question(self, response):
        # 处理question页面，从页面中提取出具体的question item
        zhihu_id = response.meta.get('zhihu_id', '')
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css('title', 'h1.QuestionHeader-title::text')
        item_loader.add_css('content', 'div.QuestionHeader-detail')
        item_loader.add_value('url', response.url)
        item_loader.add_value('zhihu_id', zhihu_id)
        item_loader.add_css('answer_num', '.List-headerText span::text')
        item_loader.add_css('comments_num',
                            '.QuestionHeader-Comment button::text')
        item_loader.add_css(
            'watch_user_num',
            '.Button.NumberBoard-item.Button--plain div strong::text')
        item_loader.add_css('topics',
                            '.QuestionHeader-topics .Popover div::text')
        question_item = item_loader.load_item()
        yield question_item

    def start_requests(self):
        chrome_option = Options()
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_experimental_option('debuggerAddress',
                                              '127.0.0.1:9222')
        browser = webdriver.Chrome(
            executable_path='/usr/bin/chromedriver',
            chrome_options=chrome_option)
        try:
            browser.maximize_window()
        except:
            pass
        browser.get("https://www.zhihu.com/signin")
        login_success = False
        cookie_dict = {}
        try:
            browser.find_element_by_css_selector(
                ".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
            browser.find_element_by_css_selector(
                ".SignFlow-accountInput.Input-wrapper input").send_keys(
                    "13984387205")
            browser.find_element_by_css_selector(
                ".SignFlow-password input").send_keys(Keys.CONTROL + "a")
            browser.find_element_by_css_selector(
                ".SignFlow-password input").send_keys("energy2fan")
            browser.find_element_by_css_selector(
                ".Button.SignFlow-submitButton").click()
            time.sleep(10)
        except:
            login_success = True
            Cookies = browser.get_cookies()
            print(Cookies)
            for cookie in Cookies:
                f = open(
                    'ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu',
                    'wb')
                pickle.dump(cookie, f)
                f.close()
                cookie_dict[cookie['name']] = cookie['value']
            # browser.close()
            return [
                scrapy.Request(
                    url=self.start_urls[0],
                    dont_filter=True,
                    cookies=cookie_dict)
            ]

        while not (login_success):
            try:
                notify_ele = browser.find_element_by_class_name(
                    'Popover PushNotifications AppHeader-notifications')
                login_success = True
                Cookies = browser.get_cookies()
                print(Cookies)
                for cookie in Cookies:
                    f = open('../cookies/zhihu/' + cookie['name'] + '.zhihu',
                             'wb')
                    pickle.dump(cookie, f)
                    f.close()
                    cookie_dict[cookie['name']] = cookie['value']
                browser.close()
                return [
                    scrapy.Request(
                        url=self.start_urls[0],
                        dont_filter=True,
                        cookies=cookie_dict)
                ]
            except:
                pass
            try:
                english_captcha_element = browser.find_element_by_class_name(
                    'Captcha-englishImg')
            except:
                english_captcha_element = None
            try:
                chinese_captcha_element = browser.find_element_by_class_name(
                    'Captcha-chineseImg')
            except:
                chinese_captcha_element = None
            if chinese_captcha_element:
                base64_text = chinese_captcha_element.get_attribute('src')
                code = base64_text.replace('data:image/jpg;base64,',
                                           '').replace('%0A', '')
                fh = open('yzm_cn.jpeg', 'wb')
                fh.write(base64.b64decode(code))
                fh.close()
                time.sleep(10)
                self.mouse_simulation(browser, chinese_captcha_element)
                browser.find_element_by_css_selector(
                    ".SignFlow-accountInput.Input-wrapper input").send_keys(
                        Keys.CONTROL + "a")
                browser.find_element_by_css_selector(
                    ".SignFlow-accountInput.Input-wrapper input").send_keys(
                        "13984387205")
                browser.find_element_by_css_selector(
                    ".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(
                    ".SignFlow-password input").send_keys("energy2fan")
                move(916, 661)
                click()
            if english_captcha_element:
                base64_text = english_captcha_element.get_attribute('src')
                code = base64_text.replace('data:image/jpg;base64,',
                                           '').replace('%0A', '')
                fh = open('yzm_en.jpeg', 'wb')
                fh.write(base64.b64decode(code))
                fh.close()
                time.sleep(10)
                yundama = YDMHttp('ean7891', 'enengy2fan', 7100,
                                  'b8bdafee3e8562455cbb0f7f2ac18921')
                code = yundama.decode('yzm_en.jpeg', 5000, 60)
                while True:
                    if code == '':
                        code = yundama.decode('yzm_en.jpeg', 5000, 60)
                    else:
                        break
                browser.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input'
                ).send_keys(Keys.CONTROL + "a")
                browser.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input'
                ).send_keys(code)
                browser.find_element_by_css_selector(
                    ".SignFlow-accountInput.Input-wrapper input").send_keys(
                        Keys.CONTROL + "a")
                browser.find_element_by_css_selector(
                    ".SignFlow-accountInput.Input-wrapper input").send_keys(
                        "13984387205")
                browser.find_element_by_css_selector(
                    ".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(
                    ".SignFlow-password input").send_keys("energy2fan")
                move(981, 643)
                click()

    def mouse_simulation(self, browser, chinese_captcha_element):
        ele_postion = chinese_captcha_element.location
        x_relative = ele_postion['x']
        y_relative = ele_postion['y']
        # 获取标签页与工具栏的高度
        browser_navigation_panel_height = browser.execute_script(
            'return window.outerHeight - window.innerHeight;')
        z = zheye()
        positions = z.Recognize('yzm_cn.jpeg')
        last_positions = []
        if len(positions) == 2:
            if positions[0][1] > positions[1][1]:
                last_positions.append([positions[1][1], positions[1][0]])
                last_positions.append([positions[0][1], positions[0][0]])
            else:
                last_positions.append([positions[0][1], positions[0][0]])
                last_positions.append([positions[1][1], positions[1][0]])
            first_position = [
                int(last_positions[0][0] / 2),
                int(last_positions[0][1] / 2)
            ]
            second_position = [
                int(last_positions[1][0] / 2),
                int(last_positions[1][1] / 2)
            ]
            move(
                x_relative + first_position[0], y_relative +
                browser_navigation_panel_height + first_position[1])
            click()
            time.sleep(3)
            move(
                x_relative + second_position[0], y_relative +
                browser_navigation_panel_height + second_position[1])
            click()
        else:
            last_positions.append([positions[0][1], positions[0][0]])
            first_position = [
                int(last_positions[0][0] / 2),
                int(last_positions[0][1] / 2)
            ]
            move(
                x_relative + first_position[0], y_relative +
                browser_navigation_panel_height + first_position[1])
            click()
