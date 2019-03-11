from django.test import LiveServerTestCase, Client
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as ec

class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.live_server_url)
        self.driver.maximize_window()
        self.wait = ui.WebDriverWait(self.driver, 1000)
        self.user = User.objects.create_user("testuser",
                                            "testuser@email.com",
                                            "testpswd")

    def tearDown(self):
        self.driver.quit()
    
    def user_login(self, username, password, waiting):
        """ User path to login """
        element_login = self.driver.find_element_by_id("login")
        element_login.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "signup")))
        username_element = self.driver.find_element_by_name("username")
        username_element.send_keys(username)
        password_element = self.driver.find_element_by_name("password")
        password_element.send_keys(password)
        submit = self.driver.find_element_by_id("submitlogin")
        submit.click()
        self.wait.until(ec.presence_of_element_located((By.ID, waiting)))

    def user_signup(self, username, email, password1, password2):
        """ User path to sign up """
        element_signup = self.driver.find_element_by_id("signup")
        element_signup.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "signupform")))
        username_element = self.driver.find_element_by_name("username")
        username_element.send_keys(username)
        email_element = self.driver.find_element_by_name("email")
        email_element.send_keys(email)
        password1_element = self.driver.find_element_by_name("password1")
        password1_element.send_keys(password1)
        password2_element = self.driver.find_element_by_name("password2")
        password2_element.send_keys(password2)
        submit = self.driver.find_element_by_id("signupsubmit")
        submit.click()

    def test_signup(self):
        old_users_number = User.objects.count()
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="bidule01",
                        password2="bidule01")
        new_users_number = User.objects.count()
        self.assertEqual(new_users_number, old_users_number + 1)
    
    def test_signup_user_already_exists(self):
        self.user_signup(username="testuser",
                email="Fiflo@email.com",
                password1="bidule01",
                password2="bidule01")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Un utilisateur avec ce nom existe déjà.")

    def test_signup_wrong_password(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="bidule01",
                        password2="bidule02")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Les deux mots de passe ne correspondent pas.")

    def test_signup_password_looks_like_username(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="fiflo0102",
                        password2="fiflo0102")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Le mot de passe est trop semblable au champ « nom d'utilisateur ».")
    
    def test_signup_password_too_short(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="bidule",
                        password2="bidule")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Ce mot de passe est trop court. Il doit contenir au minimum 8 caractères.")

    def test_signup_password_only_numeric(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="78904567",
                        password2="78904567")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Ce mot de passe est entièrement numérique.")
    
    def test_signup_password_too_mainstram(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="password",
                        password2="password")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Ce mot de passe est trop courant.")

    def test_login(self):
        self.user_login(username="testuser",
                        password="testpswd",
                        waiting="account")
        self.assertEqual(self.driver.current_url, self.live_server_url + "/")
    
    def test_login_wrong_username(self):
        self.user_login(username="wrongusername",
                        password="testpswd",
                        waiting="login_error")
        error = self.driver.find_element_by_id("login_error")
        self.assertEqual(error.text, "Le nom d'utilisateur et le mot de passe ne correspondent pas.")
    
    def test_login_wrong_password(self):
        self.user_login(username="testuser",
                        password="wrongpswd",
                        waiting="login_error")
        error = self.driver.find_element_by_id("login_error")
        self.assertEqual(error.text, "Le nom d'utilisateur et le mot de passe ne correspondent pas.")
    
    def test_logout(self):
        self.user_login(username="testuser",
                        password="testpswd",
                        waiting="account")
        element_logout = self.driver.find_element_by_id("logout")
        element_logout.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "login")))
        self.assertEqual(self.driver.current_url, self.live_server_url + "/")