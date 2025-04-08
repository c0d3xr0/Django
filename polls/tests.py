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
        cls.selenium.quit()
        super().tearDownClass()

    def test_crear_user_staff(self):
        # INICIAR SESSIÓ ADMIN
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # Comprovar pàgina actual LOGIN
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        ## Entrar dades de login i fer clic sobre botó "Log in"
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )

        # CREAR USUARI STATFF
        # Anar pàgina Add user
        self.selenium.find_element(By.XPATH, ".//a[@href='/admin/auth/user/add/']").click()

        # Comprovar pàgina actual ADD USER
        self.assertEqual( self.selenium.title , "Add user | Django site admin" )

        # Entrar dades nou usuari staff i continuar editant
        username_input = self.selenium.find_element(By.ID, "id_username")
        username_input.send_keys('staff_user')
        password_input = self.selenium.find_element(By.ID, "id_password1")
        password_input.send_keys('pirineus')
        password_input = self.selenium.find_element(By.ID, "id_password2")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,"//input[@name='_continue']").click()

        # Comprovar pàgina actual CHANGE USER
        self.assertEqual( self.selenium.title , "staff_user | Change user | Django site admin" )

        # Marcar la casella usuari staff
        self.selenium.find_element(By.XPATH,"//input[@id='id_is_staff']").click()

        # Guardar canvis staff_user
        self.selenium.find_element(By.XPATH,"//input[@name='_save']").click()

        # Comprovar que l'usuari staff_user està creat correctament
        # Si el troba no dona error, en cas contrari farà un NoSuchElementException
        self.selenium.find_element(By.XPATH,"//a[text()='staff_user']")

        # Comprovar si l'usuari creat és staff
        self.selenium.find_element(By.CLASS_NAME, "field-is_staff")

        # COMPROVAR STAFF_USER
        # Tancar la sessió actual
        #self.selenium.find_element(By.XPATH,"//button[text()='Log out']").click()
        self.selenium.find_element(By.XPATH, "//form[@id='logout-form']").click()

        # Comprovar pàgina actual LOGGED OUT
        self.assertEqual( self.selenium.title , "Logged out | Django site admin" )

        # Tornar a la pàgina LOGIN
        self.selenium.find_element(By.XPATH, ".//a[@href='/admin/']").click()

        # Comprovar pàgina actual LOGIN
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # Entrar dades inici sessió i fer clic sobre botó "Log in"
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('staff_user')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # Comprovar pàgina actual SITE ADMIN
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )

        # COMPROVAR PRIVILEGIS USER STAFF
        # Accés administració usuaris o grups
        try:
            self.selenium.find_element(By.XPATH, "//a[text()='Authentication and Authorization.']")
            self.fail("Usuari visualitza administració usuaris")
        except NoSuchElementException:
            pass  # OK, element no existeix, el que s'espera

        # Accés a questions o choices
        try:
            self.selenium.find_element(By.XPATH, "//a[text()='Polls']")
            self.fail("Usuari visualitza POLLS")
        except NoSuchElementException:
            pass  # OK, element no existeix, el que s'espera

        # Es verifica que l'usuari no té cap permís
        permissions = self.selenium.find_element(By.ID, 'content-main')
        self.assertIn("You don't have permission to view or edit anything.", permissions.text)
