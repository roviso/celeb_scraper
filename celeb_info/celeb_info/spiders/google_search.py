import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GoogleSearchSpider(scrapy.Spider):
    name = 'google_search'
    allowed_domains = ['google.com']
    start_urls = ['https://www.google.com/']

    def __init__(self, celeb_name='', *args, **kwargs):
        super(GoogleSearchSpider, self).__init__(*args, **kwargs)
        self.celeb_name = celeb_name
        self.driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Update path to chromedriver

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.save_screenshot("screenshot0.png")

        # Input the celebrity name into Google's search box and search
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.send_keys(self.celeb_name)
        search_box.send_keys(Keys.RETURN)

        # Wait for results to load (you can also use explicit waits here)
        self.driver.implicitly_wait(30)

        # Extract information from the search results
        # Extract information from the search results using the provided CSS selectors
        main_container = self.driver.find_element(By.CSS_SELECTOR, 'div.sATSHe')
        main_container_html = main_container.get_attribute('outerHTML')
        self.driver.save_screenshot("screenshot1.png")

#         about_heading = main_container.find_element(By.CSS_SELECTOR, 'div[aria-level="2"][role="heading"]').text
#         description = main_container.find_element(By.CSS_SELECTOR, 'div.kno-rdesc span').text
#         wikipedia_link = main_container.find_element(By.CSS_SELECTOR, 'div.kno-rdesc a.ruhjFe.NJLBac.fl').get_attribute('href')

#         born_info = main_container.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/people/person:born"] .rVusze').text
#         children_info = main_container.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/people/person:children"] .rVusze').text
#         height_info = main_container.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/people/person:height"] .rVusze').text
#         spouse_info = main_container.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/people/person:spouse"] .rVusze').text
#         upcoming_movies_info = main_container.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/people/person:upcoming movie"] .rVusze').text
#         parents_info = main_container.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/people/person:parents"] .rVusze').text
        yield {
            'Main Container HTML': main_container_html  # Storing the HTML content here
        }
        # yield {
        #     'About Heading': about_heading,
        #     'Description': description,
        #     'Wikipedia Link': wikipedia_link,
        #     'Born': born_info,
        #     'Children': children_info,
        #     'Height': height_info,
        #     'Spouse': spouse_info,
        #     'Upcoming Movies': upcoming_movies_info,
        #     'Parents': parents_info
        # }
        self.driver.save_screenshot("screenshot1.png")
        # for result in results:
        #     title = result.find_element(By.CSS_SELECTOR, 'h3').text
        #     link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        #     snippet = result.find_element(By.CSS_SELECTOR, 'span.st').text
        #     yield {
        #         'title': title,
        #         'link': link,
        #         'snippet': snippet
        #     }

        self.driver.quit()
