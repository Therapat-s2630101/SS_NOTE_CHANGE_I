import time
import os
from django.test import LiveServerTestCase
from django.contrib.auth.models import AnonymousUser, User
from Homepage.models import Lecture, Profile, Lecture_image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

class NewVisitorTest(LiveServerTestCase):  
    MAX_WAIT = 15  

    def setUp(self):  
        self.browser = webdriver.Firefox(executable_path='/home/therapat/SS_NOTE_CHANGE_I/geckodriver')
        self.browser.implicitly_wait(15)

        self.user = User.objects.create_user(username='steve', email='steve@email.com', password='123456')
        Profile.objects.create(user = self.user)

    def tearDown(self):  
        self.browser.quit()

    def wait_for_page_to_render_text_in_id(self, text, targetID):
        #Start count time
        start_time = time.time() 
        while True:
            #If process in try Error it will continue to except    
            try:    
                #find element by id. Ex <div id="HomepageMainArea"></div> this element
                tag = self.browser.find_element_by_id(targetID)     
                #Check text(input in function) in text in tag(element)?
                self.assertIn(text, tag.text)    
                #As if closing the loop
                return  
            
            #our turn if process in try Error
            except (AssertionError, WebDriverException) as e:   
                #if time now - time start over 15 second
                if time.time() - start_time > self.MAX_WAIT:    
                    #Show that AssertionError
                    raise e  
                #wait 0.5 second before re-start this loop again
                time.sleep(0.5)
        #It can use to just wait that element is Appear but don't check a text, Ex wait_for_page_to_render_text_in_id("","......") ,The empty text(mean "" ) is in every text

    def test_Steve_uploading_a_note(self):
        # Steve's friends invite Steve visit their new lecture sharing site named Save&Share lecture
        # Steve's friends register an account for him and give him username and password of the site
        steveAccount = self.user
        self.assertEqual(steveAccount.username,'steve')

        # Steve have found an amazing seminar about computer networking
        # He was take note of all the lecture and dicide to share it online
        # He is visiting his friend's lecture sharing site
        # He entering the site URL in his browser
        ## live_server_url it launches a live Django server in the background
        self.browser.get(self.live_server_url)

        # He notices the homepage has pop up
        self.wait_for_page_to_render_text_in_id('','HomepageMainArea')
        
        # He's looking for a login button and click it
        ## navbar is a main menu on web
        #self.assertIn('navbar_login',self.browser.page_source)
        login_button = self.browser.find_element_by_id('navbar_login')
        
        login_button.send_keys(Keys.ENTER) 

        # He notice page have redirect to a login form
        self.wait_for_page_to_render_text_in_id('','id_username') 

        # He's entering a username and password that given by his friend and click login
        username = self.browser.find_element_by_id('id_username')
        username.send_keys('steve')
        password = self.browser.find_element_by_id('id_password')  
        password.send_keys('123456')    
        password.send_keys(Keys.ENTER)

        # the page have redirect back to homepage
        self.wait_for_page_to_render_text_in_id('','HomepageMainArea')

        # He found himself login to the site in a navigation bar
        self.assertIn('steve', self.browser.find_element_by_id('navbar_username').text)

        # He also notice a login button has replace by a logout button
        self.assertNotIn('navbar_login', self.browser.page_source)
        self.assertIn('navbar_logout', self.browser.page_source)

        #He click on a Share lecture button he saw on a navigation bar
        #self.assertIn('navbar_upload', self.browser.page_source)
        self.browser.find_element_by_id('navbar_upload').send_keys(Keys.ENTER)

        # the page redirect to upload page
        self.wait_for_page_to_render_text_in_id('','UploadpageMainArea')

        # He start adding photo of the lecture to the given form
        ##os.path.abspath("red.png") is path a localtion, Ex /SS_NOTE_CHANGE_I/red.png, Current working is BASE_DIR in setting 
        absolute_file_path = os.path.abspath("red.png")
        file_input = self.browser.find_element_by_id("id_image")
        file_input.send_keys(absolute_file_path)

        # He filling the form and click upload
        noteTitle = 'Networking fundamental'

        title_textbox = self.browser.find_element_by_id('id_title')
        title_textbox.send_keys(noteTitle)
        description_textbox = self.browser.find_element_by_id('id_description')
        description_textbox.send_keys('Fundamental concept of computer network explained')
        submit_button = self.browser.find_element_by_id('submitbutton')
        submit_button.click()

        # the page redirect to homepage
        self.wait_for_page_to_render_text_in_id('','HomepageMainArea')

        # He found his lecture showing up
        self.wait_for_page_to_render_text_in_id(noteTitle,'latest_note1')

        # He click logout
        #self.assertIn('navbar_logout', self.browser.page_source)
        self.browser.find_element_by_id('navbar_logout').send_keys(Keys.ENTER)

        # self.fail('Finish the test!')
    def test_Linda_save_a_note(self):
        self.test_Steve_uploading_a_note()
        # Linda are willing to know about computer networking
        # She prefer reading a note more than an entire book
        # So, She go to Save&ShareLecture site which is a online note sharing platform
        # She entering the site url in her browser
        
        self.browser.get(self.live_server_url)
        # She notice the homepage have popup
        self.wait_for_page_to_render_text_in_id('','HomepageMainArea')
        # She looking for a computer networking's note
        # She use a search bar to make it quicker
        search_textbox = self.browser.find_element_by_name('keyword_search')
        search_textbox.send_keys('Network')
        #ime.sleep(5)
        search_button=self.browser.find_element_by_name('button_search')
        search_button.send_keys(Keys.ENTER)
        time.sleep(2)
        # She found it!
        self.wait_for_page_to_render_text_in_id('Networking fundamental','latest_note1')
        # She click on the note to view the note's detail
        Click_note=self.browser.find_element_by_link_text('Networking fundamental')
        Click_note.send_keys(Keys.ENTER)
        time.sleep(2)
        # She have quick scrolling through all the note's contents and very enjoy it
        # She decide to save this note onto her profile
        # apparently, she have to login first. So, she follow the links
        Link_login=self.browser.find_element_by_link_text('please login to save notes')
        Link_login.click()
        time.sleep(2)
        # She found herself in a login page. then she realize, she doesn't have an account
        self.wait_for_page_to_render_text_in_id('','login')
        # She follow the link to register page
        Link_SignUp=self.browser.find_element_by_link_text('Sign Up')
        Link_SignUp.click()
        time.sleep(2)
        # She fillup the username and password and click register
        username=self.browser.find_element_by_name('username')
        username.send_keys('Linda')
        password1=self.browser.find_element_by_name('password1')
        password1.send_keys('Linda25422')
        password2=self.browser.find_element_by_name('password2')
        password2.send_keys('Linda25422')
        self.browser.find_element_by_name('submit').send_keys(Keys.ENTER)
        # The site redirect to a login page
        self.wait_for_page_to_render_text_in_id('','login')
        # She fillup the previous username and password and click login
        username = self.browser.find_element_by_id('id_username')
        username.send_keys('Linda')
        password = self.browser.find_element_by_id('id_password')  
        password.send_keys('Linda25422')    
        password.send_keys(Keys.ENTER)
        # The site redirect to homepage
        self.wait_for_page_to_render_text_in_id('','HomepageMainArea')
        # She search for that note again and click on it
        search_textbox = self.browser.find_element_by_name('keyword_search')
        search_textbox.send_keys('Network')
        #ime.sleep(5)
        search_button=self.browser.find_element_by_name('button_search')
        search_button.send_keys(Keys.ENTER)
        time.sleep(2)
        # this time the save button have appear instead of a link
        Click_note=self.browser.find_element_by_link_text('Networking fundamental')
        Click_note.send_keys(Keys.ENTER)
        time.sleep(2)
        # She click save note button
        Click_savenote=self.browser.find_element_by_name('save_note')
        Click_savenote.send_keys(Keys.ENTER)
        time.sleep(1)
        # She navigate to profile page

        Click_Profile=self.browser.find_element_by_link_text('Linda')
        Click_Profile.send_keys(Keys.ENTER)
        time.sleep(1)
        # The site redirect to profile page
        # She found that note show up in saved note's column
        self.wait_for_page_to_render_text_in_id('Networking fundamental','latest_note1')
            
        # She realize she doesn't have a profile picture yet.
        # Just for fancy, She click the button to upload a profile picture
        profile_pic = self.browser.find_element_by_name("profile_picture")
        profile_pic.send_keys(os.path.abspath("red.png"))
        time.sleep(2)
        # The page refreshes again and her profile picture showed up
        Class_img=self.browser.find_element_by_name('img_profile')
        self.assertTrue(Class_img)
        # She logout
        self.browser.find_element_by_id('navbar_logout').send_keys(Keys.ENTER)
        self.wait_for_page_to_render_text_in_id('','HomepageMainArea') 

    def test_Steve_delete_a_note(self):
        ##It use to create note by Steve before we will start test
        self.test_Steve_uploading_a_note()
        #time.sleep(1)

        #Steve will go back to his note
        #He want to delete a note 
        #He entering the site url in her browser
        self.browser.get(self.live_server_url)

        #He login again 
        #self.assertIn('navbar_login',self.browser.page_source)
        login_button = self.browser.find_element_by_id('navbar_login')
        login_button.send_keys(Keys.ENTER)

        # He notice page have redirect to a login form
        self.wait_for_page_to_render_text_in_id('','id_username') 

        # He's entering a username and password again and click login
        username = self.browser.find_element_by_id('id_username')
        username.send_keys('steve')
        password = self.browser.find_element_by_id('id_password')  
        password.send_keys('123456')    
        password.send_keys(Keys.ENTER)
        #time.sleep(1)

        #He going to his profile
        #self.assertIn('navbar_username',self.browser.page_source)
        profile_enter=self.browser.find_element_by_id('navbar_username')
        profile_enter.send_keys(Keys.ENTER)
        #time.sleep(1)
 
        #He continue to a detail note
        click_note=self.browser.find_element_by_link_text('Networking fundamental')
        click_note.send_keys(Keys.ENTER)
        #time.sleep(1)

        #He see a Delete note botton and click a botton Delete note
        #self.assertIn('delete_note',self.browser.page_source)
        click_delete_note=self.browser.find_element_by_name('delete_note')
        click_delete_note.send_keys(Keys.ENTER)
        time.sleep(1)
        #He looking for confirm text and click Yes
        self.assertIn('Are you sure to delete ?',self.browser.page_source)
        self.assertIn('confirm_delete_note',self.browser.page_source)
        confirm_click=self.browser.find_element_by_name('confirm_delete_note')
        confirm_click.send_keys(Keys.ENTER)

        #This page redirect to homepage
        self.wait_for_page_to_render_text_in_id('','HomepageMainArea')

        #He going to profile again 
        #self.assertIn('navbar_username',self.browser.page_source)
        profile_enter=self.browser.find_element_by_id('navbar_username')
        profile_enter.send_keys(Keys.ENTER)
        time.sleep(1)

        #He couldn't find that note anymore.
        self.assertNotIn('Networking fundamental',self.browser.page_source)

    def test_linda_review_a_note_and_steve_read_a_review(self):
        ##It use to create note by Steve before we will start test
        #self.test_Steve_uploading_a_note()
        self.test_Linda_save_a_note()
        self.browser.get(self.live_server_url)

        

        login_button = self.browser.find_element_by_id('navbar_login')
        login_button.send_keys(Keys.ENTER)
        username = self.browser.find_element_by_id('id_username')
        username.send_keys('Linda')
        password = self.browser.find_element_by_id('id_password')  
        password.send_keys('Linda25422')    
        password.send_keys(Keys.ENTER)

        profile_enter=self.browser.find_element_by_id('navbar_username')
        profile_enter.send_keys(Keys.ENTER)

        click_note=self.browser.find_element_by_link_text('Networking fundamental')
        click_note.send_keys(Keys.ENTER)

        click_a_review=self.browser.find_element_by_name("review")
        click_a_review.send_keys(Keys.ENTER)

        radio=self.browser.find_element_by_xpath(".//input[@type='radio' and @value='4']").click()
        time.sleep(2)
        comment=self.browser.find_element_by_name("text_comment")
        comment.send_keys('It a good note')
        self.browser.find_element_by_name("submit_review").send_keys(Keys.ENTER)
        time.sleep(1)
        self.assertIn("It a good note",self.browser.page_source)
        self.browser.find_element_by_id('navbar_logout').send_keys(Keys.ENTER)

        login_button = self.browser.find_element_by_id('navbar_login')
        login_button.send_keys(Keys.ENTER)

        username = self.browser.find_element_by_id('id_username')
        username.send_keys('steve')
        password = self.browser.find_element_by_id('id_password')  
        password.send_keys('123456')    
        password.send_keys(Keys.ENTER)
        #time.sleep(1)

        #He going to his profile
        #self.assertIn('navbar_username',self.browser.page_source)
        profile_enter=self.browser.find_element_by_id('navbar_username')
        profile_enter.send_keys(Keys.ENTER)
        #time.sleep(1)
 
        #He continue to a detail note
        click_note=self.browser.find_element_by_link_text('Networking fundamental')
        click_note.send_keys(Keys.ENTER)
        time.sleep(2)

        self.assertIn("It a good note",self.browser.page_source)





        
        
        

    
    

