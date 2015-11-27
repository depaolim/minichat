import os
import signal
import subprocess

import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djchat.settings")


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def django():
    print ("setup Django")
    import django
    from django.contrib.auth.models import User
    from django.core.management import call_command
    django.setup()

    os.remove("db.sqlite3")
    call_command("migrate")
    call_command("collectstatic", "--noinput")
    User.objects.create_superuser('admin', 'admin@example.com', 'pass')


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


def test_acceptance(django, browser):
    browser.implicitly_wait(3)
    browser.get('http://localhost:5000/admin')
    browser.find_element_by_name('username').send_keys('admin')
    browser.find_element_by_name('password').send_keys('pass' + Keys.RETURN)
    browser.find_element_by_link_text('Chat').click()
    browser.find_element_by_link_text('python').click()
    browser.find_element_by_id('messageinput').send_keys('ciao' + Keys.RETURN)
    messages = browser.find_elements_by_css_selector('#messages li')
    assert [m.text for m in messages] == [u'admin:ciao']
