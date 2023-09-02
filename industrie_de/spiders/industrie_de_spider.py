import scrapy

class IndustrieDeSpiderSpider(scrapy.Spider):
    name = "industrie_de_spider"
    allowed_domains = ["www.industrie.de", "industrie.de"]
    start_urls = ["https://industrie.de/firmenverzeichnis/"]


    def parse(self, response):
        company_eitrag = response.css('.infoservice-result-row')
        for link in company_eitrag.css('a::attr(href)').getall():
              if link:
                yield scrapy.Request(response.urljoin(link), callback=self.parse_company_page)


    def parse_company_page(self, response):
        company_name = response.css('.h2 ::text').get()
        if not company_name:
          company_name = ["N/A"]

        try:
          contact_info = response.css('.textwidget dd.info-contact-data::text').getall()
          #contact_info = response.xpath('//div[@class="textwidget"]/dl/dd/text()').getall()
          if contact_info:
            website = contact_info[0]
            email = contact_info[1]
            phone = contact_info[2]
            fax = contact_info[3]
            address = ",".join(contact_info[4:8])
          else:
            website = email = phone = fax = address = "N/A"
        except Exception as e:
              #Handle exceptions like failed requests or unexpected HTML structure
              print("No information found")

        yield {
          'Company Name': company_name,
          'Website': website,
          'Email': email,
          'Phone': phone,
          'Fax': fax,
          'Address': address,
        }
