from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from time import sleep
import pandas as pd
import random

class webscraping():

    def __init__(self):
        self.driver = self.SetupDriver()

    # Configura el WebDriver.
    def SetupDriver(self):
        ua = UserAgent()
        options = Options()
        options.set_preference("general.useragent.override", ua.random)
        options.add_argument("--kiosk")
        driver = webdriver.Firefox(options=options)
        
        return driver

    # Espera a que el elemento este visible
    def WaitElement(self, by, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((by, locator)))

    # Espera a que los elementos esten visibles
    def WaitElements(self, by, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((by, locator)))

    # Crea un tiempo de espera
    def Delay(self):
        sleep(random.randint(5,6))
        
    # Simular click
    def ClickButton(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element).click().perform()
        self.Delay()

    # Mueve elementos
    def MoveElement(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        self.Delay()
        
    # Ingresa informacion al campo de texto
    def TextField(self, element, text):
        self.MoveElement(element)
        element.clear()
        for letra in text:
            element.send_keys(letra)
            sleep(random.uniform(0.1, 0.2))

    # Realiza el login
    def Login(self,username,password):
        try:
            self.driver.get('https://www.saucedemo.com')

            input_name = self.WaitElement(By.ID, 'user-name')
            self.TextField(input_name,username)
            
            input_password = self.WaitElement(By.ID, 'password')
            self.TextField(input_password,password)

            submit_button = self.WaitElement(By.ID, 'login-button')
            self.ClickButton(submit_button)

            print("Logiado con Exito")
        except Exception as e:
            print("Error en el login: {e}")
            
    # Abre el menú Hamburgesa
    def OpenBurgerMenu(self):
        try:
            menu_button = self.WaitElement(By.ID, 'react-burger-menu-b')
            
            assert menu_button.is_displayed(),"El Menu Hamburguesa no esta visible"
            
            self.ClickButton(menu_button)
            
            print("Botón Hamburgesa abierto")
        except Exception as e:
            print(f"Error al abrir el menu hamburguesa: {e}")
            
    # Valida el botón Logout
    def ValidateLogin(self):
        try:
            logout_button = self.WaitElement(By.ID, 'react-burger-menu-btn')
            self.ClickButton(logout_button)
            print("Botón logout visible")
        except Exception as e:
            print(f"Error al encontrar el boton logout en el menu: {e}")
    
    # Cierra el menú Hamburguesa
    def CloseBurgerMenu(self):
        try:
            menu_button = self.WaitElement(By.ID, 'react-burger-cross-btn')
            
            assert menu_button.is_displayed(),"El Menu Hamburguesa no esta visible"
            
            self.ClickButton(menu_button)
            
            print("Botón Hamburgesa Fue Cerrado")
        except Exception as e:
            print(f"Error al cerrar el menu hamburguesa: {e}")
            
    # Añade productos al carrito
    def AddToCart(self):
        try:
            products = self.WaitElements(By.XPATH, "//button[contains(text(), 'Add to cart')]")
   
            for product in products:
                self.driver.execute_script("arguments[0].scrollIntoView();", product)
                self.driver.execute_script("arguments[0].click();", product)
                self.Delay()
            
            remove_button = self.WaitElement(By.ID, 'remove-sauce-labs-backpack')
            assert remove_button.is_displayed(), "El botón Remove no está visible."
            
            self.Delay()
            
            print(f"Productos agregados correctamente")
        except Exception as e:
            print(f"Error al añadir productos al carrito: {e}") 
            
    # Navega a la página del carrito.
    def GoToCart(self):
        self.WaitElement(By.CLASS_NAME, "shopping_cart_link").click()
        self.Delay()  
        
    # Procede al checkout y verifica la página de checkout
    def ProceedToCheckout(self):
        try:
            checkout_title = self.WaitElements(By.CLASS_NAME, 'cart_item')
            assert len(checkout_title) > 0, "No hay producto en el carrito"
            
            self.ExportCart()
            
            checkout_button = self.WaitElement(By.ID, 'checkout')
            assert checkout_button.is_displayed(), "El boton checkout no esta visible"
            checkout_button.click()
            
            print("Página de checkout verificada correctamente.")
            self.Delay()
        except Exception as e:
            print(f"Error al proceder al checkout: {e}")

    def PaymentInformation(self):
        try:
            first_name_field = self.WaitElement(By.CSS_SELECTOR, 'input[id="first-name"]')
            last_name_field = self.WaitElement(By.CSS_SELECTOR, 'input[id="last-name"]')
            postal_code_field = self.WaitElement(By.CSS_SELECTOR, 'input[id="postal-code"]')
            continue_button = self.WaitElement(By.CSS_SELECTOR, 'input[id="continue"]')

            #input_script = """
            #    const input = arguments[0];
            #    const value = arguments[1];

            #    input.value = value;
            #    input.dispatchEvent(new Event('input', { bubbles: true }));
            #    input.dispatchEvent(new Event('change', { bubbles: true }));
            #    input.dispatchEvent(new Event('blur', { bubbles: true }));
            #"""

            # Completar el formulario
            #self.driver.execute_script(input_script, first_name_field, "Eduan")
            #self.driver.execute_script(input_script, last_name_field, "Villegas")
            #self.driver.execute_script(input_script, postal_code_field, "12345")
            self.driver.execute_script("arguments[0].value = 'Eduan';", first_name_field)
            self.driver.execute_script("arguments[0].value = 'Villegas';", last_name_field)
            self.driver.execute_script("arguments[0].value = '12345';", postal_code_field)
            
            sleep(2) 
            #continue_button.click()
            #form = self.driver.find_element(By.CSS_SELECTOR, 'form')  # Selecciona el formulario
            #form.submit()
            #self.driver.execute_script("arguments[0].submit();", form)

            self.Delay()
        except Exception as e:
            print(f"Error al proceder al checkout: {e}")
            
    # Exporta la información de los productos en el carrito a un archivo Excel.        
    def ExportCart(self):
        try:
            cart_items = self.WaitElements(By.CLASS_NAME, "cart_item")
            data = []
            
            for item in cart_items:
                product_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                product_description = item.find_element(By.CLASS_NAME, "inventory_item_desc").text[:50]
                product_price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
                data.append({"Producto": product_name,"Descripcion": product_description, "Precio": product_price})

            if data:
                df = pd.DataFrame(data)
                df.to_excel("Productos del carrito.xlsx", index=False)
                print("Información del carrito exportada")
            else:
                print("No hay productos en el carrito para exportar.")
        except Exception as e:
            print(f"Error al exportar el carrito a Excel: {e}")
  
    # Cierra navegador    
    def Close(self):
        self.driver.quit()

    # Inicio de todo
    def Home(self):
        try:    
            username = "problem_user"
            password = "secret_sauce"
            
            self.Login(username,password)# paso 1
            self.OpenBurgerMenu() # paso 2
            self.ValidateLogin() # paso 3
            self.CloseBurgerMenu() # paso 4
            self.AddToCart() # paso 5
            self.GoToCart() # paso 6
            self.ProceedToCheckout() # paso 7
            self.PaymentInformation() #paso 8
        except:
            print('Ocurrio un error en el Main')
        finally:
            self.Close()

if __name__ == "__main__":
    robot = webscraping()
    robot.Home()