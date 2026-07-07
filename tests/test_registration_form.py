import allure

from base_jenkins_ui_tests.pages.registration_page import RegistrationPage


@allure.title("Successful fill form")
def test_successful(setup_browser, create_test_file):
    registration_page = RegistrationPage(setup_browser)
    first_name = "Alex"
    last_name = "Egorov"
    email = "alex@egorov.com"
    number = "1234567890"
    maths = "Maths"
    current_address = "Some street 1"
    birth_year = "2020"
    birth_month = "11"

    with allure.step("Open registration form"):
        registration_page.open()
        registration_page.close_commercial_banner()

    with allure.step("Fill form"):
        registration_page.fill_first_name(first_name)
        registration_page.fill_last_name(last_name)
        registration_page.fill_email(email)
        registration_page.select_male_gender()

        sport_hobby = setup_browser.find_element(*RegistrationPage.HOBBIES_SPORTS)
        setup_browser.execute_script("arguments[0].scrollIntoView();", sport_hobby)

        registration_page.fill_user_number(number)
        registration_page.select_birth_date(birth_year, birth_month)
        registration_page.fill_user_subjects(maths)
        registration_page.select_sport_hobby()
        registration_page.upload_test_png(create_test_file)
        registration_page.fill_current_address(current_address)

        city = setup_browser.find_element(*RegistrationPage.CITY)
        setup_browser.execute_script("arguments[0].scrollIntoView();", city)

        registration_page.select_state()
        registration_page.select_city()
        registration_page.click_submit()

    with allure.step("Check form result"):
        registration_page.check_form_results()
