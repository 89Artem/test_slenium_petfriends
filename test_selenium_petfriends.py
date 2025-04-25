from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_petfriends(selenium):
    # Настройка неявных ожиданий
    selenium.implicitly_wait(10)  # Устанавливаем неявное ожидание в 10 секунд

    # Открываем базовую страницу PetFriends
    selenium.get("https://petfriends.skillfactory.ru/")

    # Кликаем по кнопке нового пользователя
    btn_newuser = selenium.find_element(By.XPATH, "//button[@onclick="
    document.location = '/new_user';
    "]")
    btn_newuser.click()

    # Кликаем по кнопке существующего пользователя
    btn_exist_acc = selenium.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # Вводим email (ввести свою почту)
    field_email = selenium.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("<your_email>")

    # Вводим пароль (ввести свой пароль)
    field_pass = selenium.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys("<your_password>")

    # Кликаем по кнопке отправки
    btn_submit = selenium.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    # Явные ожидания для проверки URL после входа
    WebDriverWait(selenium, 10).until(EC.url_to_be('https://petfriends.skillfactory.ru/all_pets'))

    if selenium.current_url == 'https://petfriends.skillfactory.ru/all_pets':
        # Делаем скриншот окна браузера
        selenium.save_screenshot('result_petfriends.png')

        # Добавляем явные ожидания для элементов карточек питомцев
        pet_cards = WebDriverWait(selenium, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-deck .card")))

        for card in pet_cards:
            # Проверяем наличие фото питомца
            photo = card.find_element(By.TAG_NAME, 'img')
            assert photo.is_displayed(), "Фото питомца не отображается"

            # Проверяем наличие имени питомца
            name = card.find_element(By.CSS_SELECTOR, '.card-title')
            assert name.text != "", "Имя питомца отсутствует"

            # Проверяем наличие возраста питомца
            age = card.find_element(By.CSS_SELECTOR, '.card-text')
            assert age.text != "", "Возраст питомца отсутствует"

    else:
        raise Exception("Login error")