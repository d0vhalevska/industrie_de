import scrapy

class IndustrieDeSpiderSpider(scrapy.Spider):
    name = "industrie_de_spider"
    allowed_domains = ["www.industrie.de", "industrie.de"]
    start_urls = ["https://industrie.de/firmenverzeichnis/"]


    def parse(self, response):
      #get all company entries from the list
      company_eitrag = response.css('.infoservice-result-row')
      #extract the links from the company entries and tell scrapy to loop through it
      for link in company_eitrag.css('a::attr(href)').getall():
        #doing so only if link exists
        if link:
          yield scrapy.Request(response.urljoin(link), callback=self.parse_company_page)


    def parse_company_page(self, response):
      #get the company name
      company_name = response.css('.h2 ::text').get()
      if not company_name:
        company_name = ["N/A"]

      #set values on NA in case info is missing
      website = email = phone = fax = address = "N/A"

      # contact_info = response.css('.textwidget dd.info-contact-data::text').getall()
      # contact_info = response.xpath('//div[@class="textwidget"]/dl/dd/text()').getall()

      try:
        #getting info from Daten&Kontakte and format-sorting according to icon class in case some entries are empty in Daten&Kontakte
        if response.css('.info-icon i.fa-globe'):
          website = response.css('dd.info-contact-data::text').extract_first()
        if response.css('.info-icon i.fa-envelope'):
          email = response.css('dd.info-contact-data::text').extract()[1]
        if response.css('.info-icon i.fa-phone'):
          phone = response.css('dd.info-contact-data::text').extract()[2]
        if response.css('.info-icon i.fa-fax'):
          fax = response.css('dd.info-contact-data::text').extract()[3]
        if response.css('.info-icon i.fa-map-pin'):
          address_parts = response.css('dd.info-contact-data::text').extract()[4:8] #could be nicer, but it is what it is
          address = ", ".join(address_parts)
      except Exception as e:
        #double protection against cases where there are icons somewhere, but no infos etc
        print("No information found")

      yield {
        'Company Name': company_name,
        'Website': website,
        'Email': email,
        'Phone': phone,
        'Fax': fax,
        'Address': address,
      }
