import pytest
from driver import WebDriver
from bs4 import BeautifulSoup


@pytest.mark.usefixtures("req_res_page")
class ReqResPage:

    def __init__(self, driver):
        self.driver = WebDriver(driver=driver)
        self.section_list_resource = "//a[contains(text(), 'List <resource>')]/parent::li"
        self.showed_request = "//p[@class='request-title']/descendant::span"
        self.content_element_selector = "//div[@class='response']/child::pre"

    def go_main_page(self, url='https://reqres.in'):
        self.driver.go_to_url(url)

    def chose_action(self):
        self.driver.wait_for_presence_of_element_located(self.section_list_resource)
        self.driver.wait_for_visibility_of_web_element(self.section_list_resource)
        self.driver.click_web_element(self.section_list_resource)
        self.driver.wait_for_visibility_of_web_element(self.content_element_selector)

    def get_endpoint(self, expected):
        self.driver.wait_for_visibility_of_web_element(self.showed_request)
        text = self.driver.get_web_element_text(self.showed_request)
        assert expected in text, \
            "Not expected result for shown request, actual: {}, expected: {}".format(text, expected)
        return text

    def resource_ui_parser(self, id='2', parse=True):
        """

        :param id: id of resource
        :param parse: parsed in dict resource
        :return: parsed resource by id
        """
        resp = []
        source = self.driver.get_page_source()
        self.soup = BeautifulSoup(source, features="html.parser")
        tags = self.soup.find_all("span", text=True)
        for _ in tags:
            if 'data' in _.text:
                indx = tags.index(_)
                tags_ = tags[indx:]
                for _ in tags_:
                    if _.text == id:
                        start_index = tags_.index(_)
                        end_index = start_index + 9
                        resp.append(tags_[start_index:end_index])
        if parse:
            parsed = {"id": int(id)}
            resp = resp[0]
            for _ in resp:
                currnt_index = resp.index(_)
                if 'key' in resp[currnt_index].attrs['class']:
                    value_indx = resp.index(_) + 1
                    if 'number' in resp[value_indx].attrs['class']:
                        parsed[_.text[1:-2]] = int(resp[value_indx].text)
                    else:
                        parsed[_.text[1:-2]] = resp[value_indx].text[1:-1]
            return parsed
        return resp
