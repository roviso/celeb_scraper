# from scrapy import Spider
# from scrapy_selenium import SeleniumRequest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# class NetworthSpider(Spider):
#     name = 'networth'
#     start_urls = ['https://www.celebritynetworth.com/#search']

#     def __init__(self, celeb_name=None, *args, **kwargs):
#         super(NetworthSpider, self).__init__(*args, **kwargs)
#         self.celeb_name = celeb_name

#     def start_requests(self):
#         # Pass the celeb_name into the URL directly
#         yield SeleniumRequest(
#             url=f'https://www.celebritynetworth.com/#search/q={self.celeb_name}',
#             wait_time=3,
#             callback=self.parse
#         )

#     def parse(self, response):
#         driver = response.request.meta['driver']
#         driver.save_screenshot("screenshot0.png")

#         # Here, you can directly start extracting data since the page will already have the results for the given celeb_name
#         # Extract desired data or navigate to results
#         top_result = response.css("slick-search-group[id='Top results'] a::attr(href)").extract_first()
#         if top_result:
#             yield SeleniumRequest(url=top_result, callback=self.parse_details, wait_time=10)

#     def parse_details(self, response):
#         driver = response.request.meta['driver']
#         driver.save_screenshot("screenshot1.png")

#         yield {
#             'url': response.url,
#             'html_content': response.text
#         }
