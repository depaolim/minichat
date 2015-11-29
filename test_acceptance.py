import signal
import subprocess

import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="module")
def browser(request):
    print ("setup uWSGI")
    uwsgi = subprocess.Popen(["uwsgi", "uwsgi.ini"])
    print ("setup browser")
    browser = webdriver.Firefox()

    def fin():
        print ("teardown uWSGI")
        uwsgi.send_signal(signal.SIGQUIT)
        print ("teardown browser")
        browser.quit()
    request.addfinalizer(fin)
    return browser  # provide the fixture value


def test_acceptance(browser):
    browser.implicitly_wait(3)
    browser.get('http://localhost:5000')
    assert 'Main' in browser.title
    browser.find_element_by_id('user_id').send_keys('admin' + Keys.RETURN)
    browser.find_element_by_link_text('python').click()
    browser.find_element_by_id('messageinput').send_keys('ciao' + Keys.RETURN)
    messages = browser.find_elements_by_css_selector('#messages li')
    assert [m.text for m in messages] == [u'admin:ciao']
