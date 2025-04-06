from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Create your tests here.

class MySeleniumTests(StaticLiveServerTestCase):
# no crearem una BD de test en aquesta ocasió (comentem la línia)
#fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        #cls.selenium.quit()
        super().tearDownClass()

    def test_crear_usuari_staff(self):
        # iniciar sessió admin
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )

        # Crear usuari staff
        # Entrar a la vista USER ADD
        self.selenium.find_element(By.XPATH, ".//a[@href='/admin/auth/user/add/']").click()

        # testejem que hem entrat a la vista de crear usuari
        self.assertEqual( self.selenium.title , "Add user | Django site admin" )
