from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from yattag import Doc
from yattag import indent


def md(url):
    dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), url.split("/")[-2])
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


def modal(url):
    # driver = webdriver.Chrome()
    dirname = md(url)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(2)
    open_buttons = driver.find_elements_by_class_name("modal-button-target")
    i = 0
    report_list = []

    for button in open_buttons[:-1]:
        i += 1
        button.click()
        time.sleep(2)
        img_fname = dirname + "/" + "ss_" + str(i) + ".png"
        pair_set = (img_fname, driver.current_url)
        report_list.append(pair_set)
        driver.get_screenshot_as_file(img_fname)
        driver.find_element_by_class_name("modal-close-button-transform-container").click()
        time.sleep(2)

    return report_list


def html_generate(url_list):
    dirname = md(url_list[0][1])
    doc, tag, text, line = Doc().ttl()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('body'):
            with tag('table'):
                for i in range(len(url_list)):
                    with tag('tr'):
                        with tag('td'):
                            doc.stag('img', src=url_list[i][0], width="50%", height="50%")
                        with tag('td', ('align', 'left')):
                            with tag('a', ('href', url_list[i][1])):
                                text(url_list[i][1])
    with open(dirname + "/report.html", "w") as f:
        f.write(indent(doc.getvalue()))


html_generate(modal("https://www.apple.com/apple-watch-series-3/"))
