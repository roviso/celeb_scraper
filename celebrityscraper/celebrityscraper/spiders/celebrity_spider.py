from scrapy import Spider
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NetworthSpider(Spider):
    name = 'networth'
    start_urls = ['https://www.celebritynetworth.com/#search']

    def __init__(self, celeb_name=None, *args, **kwargs):
        super(NetworthSpider, self).__init__(*args, **kwargs)
        self.celeb_name = celeb_name

    def start_requests(self):
        yield SeleniumRequest(
            url=f'https://www.celebritynetworth.com/#search/q={self.celeb_name}',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.request.meta['driver']
        driver.save_screenshot("screenshot0.png")

        # Input the celebrity name into the search box
        # Wait for the search input to be visible and interactable
        wait = WebDriverWait(driver, 5)
        # driver.execute_script("return document.querySelector(\"slick-search-group[id='Top results'] a\");")
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a#name")))

        if not element:
            print("no element found")
            iframe = driver.find_element(By.CSS_SELECTOR, "iframe.some-selector")
            driver.switch_to.frame(iframe)

            element = driver.find_element(By.CSS_SELECTOR, "a#name")

        top_result_element = element

        # top_result_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a#name"))).get_attribute('href')

        top_result_element.click()


        driver.save_screenshot("screenshot1.png")
        wait = WebDriverWait(driver, 5)
        driver.save_screenshot("screenshot2.png")

        # Locate the search input and send the celebrity name
        # search_input = wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
        # search_input.send_keys(self.celeb_name)

        # # If the search isn't triggered automatically, click on the search icon/button
        # # Here, I'm using the soso-icon as a potential search trigger, but you might need to adjust this
        # search_icon = wait.until(EC.element_to_be_clickable((By.ID, "searchInputIcon")))
        # search_icon.click()
        # driver.save_screenshot("screenshot1.png")
        # search_input.send_keys(self.celeb_name)
        # driver.save_screenshot("screenshot2.png")
        


        # # Wait for the <slick-search-list> element to be populated
        # wait = WebDriverWait(driver, 10)
        # wait.until(EC.presence_of_element_located((By.ID, "itemCollection")))

        # # Extract the list of celebrities from the <slick-search-list> element
        # # This is a placeholder; you'll need to adjust based on the actual structure inside the <slick-search-list>
        # celeb_elements = driver.find_elements_by_css_selector("#itemCollection .celebrity-item-class")  # Replace with the actual selector

        # for celeb in celeb_elements:
        #     celeb_name = celeb.text  # Adjust based on the structure
        #     yield {"celebrity_name": celeb_name}

        # Close the driver
        driver.quit()
