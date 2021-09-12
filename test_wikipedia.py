import pytest

from lxml import etree as et
from create_config import CreateConfig
import time


INPUT = {
    "excepted_title": "Wikipedia",
    "expected_url": "https://www.wikipedia.org/"
}
DATA = {}

def create_xml():
    config = CreateConfig('pytest_on_wikipedia')
    for k, v in INPUT.items():
        config.add_child(k, v)
    config.write_to_file('config_for_wikipedia_pytest.xml')


def initiate_data():
    contents_xml_file = et.parse('config_for_wikipedia_pytest.xml')
    for items in contents_xml_file.iter():
        DATA[items.tag] = items.text

@pytest.fixture(scope='module')
def setup():
    create_xml()
    initiate_data()
    yield
    print("---- END ----")



@pytest.mark.usefixtures("setup")
def test_title(get_browser):
    driver = get_browser
    assert driver.title == DATA["excepted_title"], "test title - FAIL"

@pytest.mark.usefixtures("setup")
def test_url(get_browser):
    driver = get_browser
    assert driver.current_url == DATA["expected_url"], "test url - FAIL"

@pytest.mark.usefixtures("setup")
def test_corona_cases(get_browser):
    driver = get_browser
    driver.find_element_by_xpath('//*[@id="js-link-box-he"]/strong').click()
    serch_line = driver.find_element_by_css_selector('input[type="search"]')
    serch_line.send_keys('קורונה בישראל')
    driver.find_element_by_css_selector('button[class="wvui-button wvui-typeahead-search__submit wvui-button--action-default wvui-button--type-normal wvui-button--framed"]').click()
    num_of_cases_by_wiki = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[7]/td/small[1]').text.split()[1]
    driver.get('https://datadashboard.health.gov.il/COVID-19/general?utm_source=go.gov.il&utm_medium=referral')
    num_of_cases_by_heakth_ministry = driver.find_element_by_xpath('/html/body/ngx-app/ngx-pages/nb-layout/div/div/div/div/div/nb-layout-column/ngx-general/section[1]/div/ngx-tile-wrapper[2]/ngx-doughnut-pie-statistic/nb-card/ngx-small-statistics-info/div/div[1]/h4').text
    assert num_of_cases_by_wiki == num_of_cases_by_heakth_ministry, 'test to check the number of corona cases in wikipidia - FAIL'






