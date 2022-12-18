import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from config import PATH_DRIVER, TEST_EMAIL, TEST_PASSWORD


@pytest.fixture(autouse=True)
def testing():
    pytest_driver = webdriver.Chrome(PATH_DRIVER)
    # Переходим на страницу авторизации
    pytest_driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest_driver.find_element(By.ID, 'email').send_keys(TEST_EMAIL)
    # Вводим пароль
    pytest_driver.find_element(By.ID, 'pass').send_keys(TEST_PASSWORD)
    # Нажимаем на кнопку входа в аккаунт
    pytest_driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    yield pytest_driver

    pytest_driver.quit()

def test_autorization(testing):
    pytest_driver = testing

    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest_driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

def test_num_my_pets(testing):
    pytest_driver = testing

    # переходим на страницу "мои питомцы"
    pytest_driver.find_element(By.XPATH, '/ html / body / nav / button / span').click()
    pytest_driver.find_element(By.XPATH, '// *[ @ id = "navbarNav"] / ul / li[1] / a').click()

    # устанавливаем неявное ожидание для отображения всех карточек питомцев
    pytest_driver.implicitly_wait(10)

    cards = pytest_driver.find_elements(By.CSS_SELECTOR, 'tbody tr')

    num = pytest_driver.find_element(By.CSS_SELECTOR, ('div[class=".col-sm-4 left"]')).text

    assert len(cards) == int(num.split(":")[1].split("\n")[0])


def test_all_pets_have_name_age_type(testing):
    pytest_driver = testing
    # устанавливаем неявное ожидание
    pytest_driver.implicitly_wait(10)
    # переходим на страницу "мои питомцы"
    pytest_driver.find_element(By.XPATH, '/ html / body / nav / button / span').click()
    # устанавливаем неявное ожидание для отображения всех карточек питомцев
    pytest_driver.implicitly_wait(10)
    pytest_driver.find_element(By.XPATH, '// *[ @ id = "navbarNav"] / ul / li[1] / a').click()

    # добавляем явные ожидания элементов на странице
    names = WebDriverWait(pytest_driver, 10).until(ec.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[1]')))
    types = WebDriverWait(pytest_driver, 10).until(ec.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[2]')))
    ages = WebDriverWait(pytest_driver, 10).until(ec.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[2]')))

    # Text имен
    text_names = [x.text for x in names]
    # Text породы
    text_types = [x.text for x in types]
    # Text возраста
    text_ages = [x.text for x in ages]

    # проверяем, что количество имен равно количеству пород и количеству возрастов
    assert len(text_names) == len(text_types) == len(text_ages)