import os
from selenium import webdriver
import random
from IPython import embed
import time
import json
import base64


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

driver = webdriver.Chrome(executable_path='/home/dell/PycharmProjects/selenium/chromedriver',chrome_options = chrome_options)
driver.set_window_size(1920, 1080)
driver.get('https://www.csis.org/analysis/defense-budget-priorities-biden-administration')
def get_screenshot(driver, unique_id, path_suffix, options = {'landscape' : False}, comp_det={}):
    try:
        
        unique_id = str(random.randint(10,99))
        folder_path = os.path.join('/home/dell/client/webpages', unique_id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        def send_devtools(driver, cmd, params={}):
            resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
            url = driver.command_executor._url + resource
            body = json.dumps({'cmd': cmd, 'params': params})
            response = driver.command_executor._request('POST', url, body)
            # if response['status']:
            #     raise Exception(response.get('value'))
            return response.get('value')


        def save_as_pdf(driver, path, options=options):
            result = send_devtools(driver, "Page.printToPDF", options)
            with open(pdf_path, 'wb') as file:
                file.write(base64.b64decode(result['data']))
        time.sleep(5)

        pdf_path = os.path.join('/home/dell/client/webpages', unique_id+ path_suffix + '.pdf')
        if os.path.exists(pdf_path):
            pdf_path = os.path.join('/home/dell/client/webpages', unique_id + path_suffix + str(randint(11, 99)) + '.pdf')
        save_as_pdf(driver, pdf_path, options)
        return pdf_path
    except Exception as e:
        raise Exception("get screenshot failed")


unique_id = str(random.randint(10,99))
pdf = get_screenshot(driver,unique_id,'_url_')
print(pdf)