import unittest

from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from app import app, db
from app.models import User, Party

class AppTestCase(LiveServerTestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['LIVESERVER_TIMEOUT'] = 10
        db.init_app(app)
        with app.app_context():
            db.create_all()
            self.insert_data_to_db()
        return app

    def insert_data_to_db(self):
        db.session.commit()
        watted = User('mohammed', 'watted', '345')
        avoda = Party(u'העבודה',
                      'https://www.am-1.org.il/wp-content/uploads/2015/03/%D7%94%D7%A2%D7%91%D7%95%D7%93%D7%94.-%D7%A6%D7%99%D7%9C%D7%95%D7%9D-%D7%99%D7%97%D7%A6.jpg')
        db.session.add(avoda)
        db.session.add(watted)
        db.session.commit()

    def setUp(self):
        # create a new Firefox session
        self.browser = webdriver.PhantomJS()
        # nevigate to the application home page
        self.browser.get(self.get_server_url())
        self.str = '×”×ž×¦×‘×™×¢ ××™× ×• ×ž×•×¤×™×¢ ×‘×‘×¡×™×¡ ×”× ×ª×•× ×™× ××• ×©×›×‘×¨ ×”×¦×‘×™×¢'

    def test_getting_to_voting_page(self):
        first_name = self.browser.find_element_by_name('first_name')
        first_name.send_keys('mohammed')
        last_name = self.browser.find_element_by_name('last_name')
        last_name.send_keys('watted')
        id = self.browser.find_element_by_name('id')
        id.send_keys('345')
        id.send_keys(Keys.ENTER)

        assert self.str not in self.browser.page_source

    def test_full_vote(self):
        first_name = self.browser.find_element_by_name('first_name')
        first_name.send_keys('mohammed')
        last_name = self.browser.find_element_by_name('last_name')
        last_name.send_keys('watted')
        Id = self.browser.find_element_by_name('id')
        Id.send_keys('345')
        Id.send_keys(Keys.ENTER)
        assert u'לצורך הצבעה, בחר את המפלגה הרצויה' in self.browser.page_source
        # select party
        self.browser.find_element_by_tag_name('img').click()
        self.browser.find_element_by_class_name('btn').submit()

        assert u'האם ברצונך לאשר' in self.browser.page_source

        # confirm selected party
        self.browser.find_element_by_id('ok').click()

        assert u'ברוכים הבאים' in self.browser.page_source

    def test_user_not_in_database(self):
        first_name = self.browser.find_element_by_name('first_name')
        first_name.send_keys('mohammed')
        last_name = self.browser.find_element_by_name('last_name')
        last_name.send_keys('watted')
        Id = self.browser.find_element_by_name('id')
        Id.send_keys('987')
        Id.send_keys(Keys.ENTER)
        # self.browser.find_element_by_name("submit").click()
        # check if user where able to enter parties page
        assert self.str not in self.browser.page_source

    def tearDown(self):
        self.browser.quit()
        with app.app_context():
            db.drop_all()
            db.session.remove()


# Run tests if script was executed directly from the shell
if (__name__ == '__main__'):
    unittest.main()
