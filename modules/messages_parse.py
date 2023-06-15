from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from django_setup import *
from app.models import IncomingMessage, Account, OutgoingMessage
from selenium.common.exceptions import NoSuchElementException, WebDriverException


class OutlookScraper:
    def __init__(self, login, password, driver):
        self.login = login
        self.password = password
        self.driver = driver

    def login_to_outlook(self):
        self.driver.get("https://outlook.live.com/")

        login_link_element = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "auxiliary-actions"))
        )
        login_link = login_link_element.find_element(
            By.CLASS_NAME, "internal.sign-in-link"
        )
        login_link.click()

        input_login = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "i0116"))
        )
        input_login.send_keys(self.login)

        button_submit = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        button_submit.click()

        input_password = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "i0118"))
        )
        input_password.send_keys(self.password)

        button_submit = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        button_submit.click()

        button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "idBtn_Back"))
        )
        button.click()


class IncomingMessageScraper:
    def __init__(self, driver):
        self.driver = driver

    def scrape_messages(self, acc):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "abF91.bkYAr.rv6Vd"))
            )

            messages = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "hcptT.gDC9O"))
            )
            for message in messages:
                message.click()
                try:
                    letter_subject = (WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "full.UAxMv"))
                    ).text)
                except NoSuchElementException:
                    letter_subject = None

                try:
                    element_message = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "wide-content-host"))
                    )
                except NoSuchElementException:
                    continue

                try:
                    sender = element_message.find_element(By.CLASS_NAME, "OZZZK").text
                except NoSuchElementException:
                    sender = None

                try:
                    recipient = element_message.find_element(
                        By.CLASS_NAME, "lDdSm.l8Tnu"
                    ).text
                except NoSuchElementException:
                    recipient = None

                try:
                    text = element_message.find_element(
                        By.CLASS_NAME, "XbIp4.jmmB7.GNqVo.yxtKT.allowTextSelection").text
                except NoSuchElementException:
                    text = None

                file_path = None
                if self.driver.find_element(By.CLASS_NAME, "l8Tnu.T3idP").text:
                    try:
                        context_menu_button = WebDriverWait(element_message, 5).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, "o4euS"))
                        )
                        context_menu_button.click()
                        download_button = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located(
                                (
                                    By.CSS_SELECTOR, '.ms-ContextualMenu-link[name="Скачать"]'
                                )
                            )
                        )
                        file_name = self.driver.find_element(By.CLASS_NAME, "VlyYV.PQeLQ.QEiYT")
                        file_path = "C:/Users/SCHOO/Downloads/" + file_name.text
                        download_button.click()
                    except NoSuchElementException:
                        pass

                IncomingMessage.objects.create(
                    email=acc,
                    subject=letter_subject,
                    sender=sender,
                    recipient=recipient,
                    text=text,
                    media_file=file_path,
                )

        except WebDriverException as e:
            print(f"Error occurred during scraping incoming messages: {str(e)}")


class OutgoingMessageScraper:
    def __init__(self, driver):
        self.driver = driver

    def scrape_outgoing_messages(self, acc):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "abF91.bkYAr.rv6Vd"))
            )

            outgoing_button = self.driver.find_element(
                By.CSS_SELECTOR, "div[title='Отправленные']"
            )
            outgoing_button.click()

            messages = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "hcptT.gDC9O"))
            )
            for message in messages:
                message.click()

                try:
                    letter_subject = (WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "full.UAxMv"))).text)
                except NoSuchElementException:
                    letter_subject = None

                try:
                    element_message = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "wide-content-host"))
                    )
                except NoSuchElementException:
                    continue

                try:
                    sender = element_message.find_element(By.CLASS_NAME, "OZZZK").text
                except NoSuchElementException:
                    sender = None

                try:
                    recipient = element_message.find_element(
                        By.CLASS_NAME, "lDdSm.l8Tnu"
                    ).text
                except NoSuchElementException:
                    recipient = None

                try:
                    text = element_message.find_element(
                        By.CLASS_NAME, "XbIp4.jmmB7.GNqVo.yxtKT.allowTextSelection"
                    ).text
                except NoSuchElementException:
                    text = None

                file_path = None
                if self.driver.find_element(By.CLASS_NAME, "l8Tnu.T3idP").text:
                    try:
                        context_menu_button = WebDriverWait(element_message, 5).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, "o4euS"))
                        )
                        context_menu_button.click()
                        download_button = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located(
                                (
                                    By.CSS_SELECTOR, '.ms-ContextualMenu-link[name="Скачать"]'
                                )
                            )
                        )
                        file_name = self.driver.find_element(By.CLASS_NAME, "VlyYV.PQeLQ.QEiYT")
                        file_path = "C:/Users/SCHOO/Downloads/" + file_name.text
                        download_button.click()
                    except NoSuchElementException:
                        pass

                OutgoingMessage.objects.create(
                    email=acc,
                    subject=letter_subject,
                    sender=sender,
                    recipient=recipient,
                    text=text,
                    media_file=file_path,
                )

        except WebDriverException as e:
            print(f"Error occurred during scraping outgoing messages: {str(e)}")


def main():
    for acc in Account.objects.filter(status="New"):
        try:
            service = Service()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            driver = webdriver.Chrome(service=service, options=chrome_options)

            scraper = OutlookScraper(acc.login, acc.password, driver)
            scraper.login_to_outlook()

            incoming_scraper = IncomingMessageScraper(driver)
            incoming_scraper.scrape_messages(acc)

            outgoing_scraper = OutgoingMessageScraper(driver)
            outgoing_scraper.scrape_outgoing_messages(acc)

            driver.quit()

            acc.status = "Done"
            acc.save()

        except WebDriverException as e:
            print(f"Error occurred during scraping for account {acc.login}: {str(e)}")


if __name__ == "__main__":
    main()
