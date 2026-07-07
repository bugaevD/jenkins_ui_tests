import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


class RegistrationPage:
    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    GENDER_MALE = (By.CSS_SELECTOR, "label[for=gender-radio-1]")
    GENDER_FEMALE = (By.CSS_SELECTOR, "label[for=gender-radio-1]")
    MOBILE = (By.ID, "userNumber")
    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    MONTH_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")
    DAY_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__day--025:not(.react-datepicker__day--outside-month)")
    SUBJECTS = (By.ID, "subjectsInput")
    HOBBIES_SPORTS = (By.CSS_SELECTOR, "label[for=hobbies-checkbox-1]")
    HOBBIES_READING = (By.CSS_SELECTOR, "label[for=hobbies-checkbox-2]")
    HOBBIES_MUSIC = (By.CSS_SELECTOR, "label[for=hobbies-checkbox-3]")
    UPLOAD_PICTURE = (By.ID, "uploadPicture")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    SUBMIT_BUTTON = (By.ID, "submit")
    RESULT_FORM = (By.ID, "resultModal")
    BANNER_BUTTON = (By.XPATH, "//div[@id='fixedban']//button[@aria-label='Close']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Open url")
    def open(self):
        self.driver.get(self.URL)
        wrapper = self.driver.find_element(By.CSS_SELECTOR, ".practice-form-wrapper")
        assert "Student Registration Form" in wrapper.text

    @allure.step("Close banner")
    def close_commercial_banner(self):
        banner_button = self.wait.until(EC.element_to_be_clickable(self.BANNER_BUTTON))
        banner_button.click()

    @allure.step("Fill first name field with {first_name}")
    def fill_first_name(self, first_name):
        element = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))
        element.clear()
        element.send_keys(first_name)

    @allure.step("Fill last name field with {last_name}")
    def fill_last_name(self, last_name):
        element = self.driver.find_element(*self.LAST_NAME)
        element.clear()
        element.send_keys(last_name)

    @allure.step("Fill first email field with {email}")
    def fill_email(self, email):
        element = self.driver.find_element(*self.EMAIL)
        element.clear()
        element.send_keys(email)

    @allure.step("Select male gender")
    def select_male_gender(self):
        element = self.driver.find_element(*self.GENDER_MALE)
        element.click()

    @allure.step("Fill user number field with {number}")
    def fill_user_number(self, number):
        element = self.driver.find_element(*self.MOBILE)
        element.clear()
        element.send_keys(number)

    @allure.step("Select date of birth")
    def select_birth_date(self, year, month):
        self.driver.find_element(*self.CALENDAR_INPUT).click()
        Select(self.driver.find_element(*self.YEAR_OF_BIRTH_SELECT)).select_by_value(year)
        Select(self.driver.find_element(*self.MONTH_OF_BIRTH_SELECT)).select_by_value(month)
        self.driver.find_element(*self.DAY_OF_BIRTH_SELECT).click()

    @allure.step("Fill user subjects field")
    def fill_user_subjects(self, subject):
        element = self.driver.find_element(*self.SUBJECTS)
        element.clear()
        element.send_keys(subject)
        element.send_keys(Keys.ENTER)

    @allure.step("Select sport hobby")
    def select_sport_hobby(self):
        element = self.driver.find_element(*self.HOBBIES_SPORTS)
        element.click()

    @allure.step("Upload test PNG")
    def upload_test_png(self, test_png):
        self.driver.find_element(*self.UPLOAD_PICTURE).send_keys(test_png)

    @allure.step("Fill current address")
    def fill_current_address(self, current_address):
        element = self.driver.find_element(*self.CURRENT_ADDRESS)
        element.clear()
        element.send_keys(current_address)

    @allure.step("Select state")
    def select_state(self):
        self.driver.find_element(*self.STATE).click()
        state_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='state-city-option'][text()='NCR']")))
        state_dropdown.click()

    @allure.step("Select city")
    def select_city(self):
        self.driver.find_element(*self.CITY).click()
        city_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='state-city-option'][text()='Delhi']")))
        city_dropdown.click()

    @allure.step("Click submit button")
    def click_submit(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    @allure.step("Check form results")
    def check_form_results(self):
        title = self.wait.until(EC.visibility_of_element_located(self.RESULT_FORM))

        assert "Thanks for submitting the form" in title.text
