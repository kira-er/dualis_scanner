from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import configparser
from pyvirtualdisplay import Display



def get_grades (username, password):
    data = list()

    options = Options()
    options.headless = True

    display = Display(visible=0, size=(1024, 768))
    display.start()

    driver = webdriver.Firefox(options = options)
    driver.implicitly_wait(1)
    driver.get("https://dualis.dhbw.de/")

    #Username
    elem = driver.find_element_by_id("field_user")
    elem.clear()
    elem.send_keys(username)

    #Password
    elem = driver.find_element_by_id("field_pass")
    elem.clear()
    elem.send_keys(password)

    #LogIn
    elem = driver.find_element_by_id("logIn_btn")
    elem.click()


    #switch to Prüfungsergebnisse
    elem = driver.find_element_by_id("link000307")
    elem.click()


    #select Semester
    elem = driver.find_element_by_id("semester")
    all_semesters_len = len(elem.find_elements_by_tag_name("option"))

    for semester_index in range(all_semesters_len):
        elem = driver.find_element_by_id("semester")
        all_semesters = elem.find_elements_by_tag_name("option")
        semester = all_semesters[semester_index]
        semester.click()

        #select course
        elem = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[2]/div[2]/div/table/tbody")
        all_courses = elem.find_elements_by_tag_name("tr")[0:-1]
        for course in all_courses:
            link = course.find_elements_by_tag_name("td")[5]
            link.click()

            main_window = driver.window_handles[0]
            driver.switch_to.window(driver.window_handles[1])


            elem = driver.find_element_by_xpath("/html/body/div/form/table[1]/tbody")
            all_tests = elem.find_elements_by_tag_name("tr")[4:-1]

            last_semester = "no semester found"

            for test in all_tests:
                try:
                    grade = test.find_elements_by_tag_name("td")[3]
                    name = test.find_elements_by_tag_name("td")[1]
                    module = test.find_element_by_xpath("/html/body/div/form/h1")
                    sem = test.find_elements_by_tag_name("td")[0]
                    if(sem.text != " "):
                        last_semester = sem.text
                except IndexError:
                    continue

                data.append({
                    "Name" : name.text,
                    "Note" : grade.text,
                    "Modul": module.text,
                    "Semester" : last_semester
                })

            driver.close()
            driver.switch_to.window(main_window)

    driver.close()
    driver.quit()

    return data

