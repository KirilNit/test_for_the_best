import pytest
from selenium import webdriver
from utils.api_utils import ReqResAPI
from utils.reqres_page import ReqResPage


@pytest.fixture(scope='class')
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('w3c', False)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    request.cls.driver = driver
    yield
    driver.close()


@pytest.fixture(scope='class')
def api_utils(request):
    api_util = ReqResAPI()
    request.cls.api_util = api_util
    yield

@pytest.mark.usefixtures('driver')
@pytest.fixture('class')
def reqres_page(request):
    req_page = ReqResPage(request.cls.driver)
    request.cls.req_page = req_page
    yield