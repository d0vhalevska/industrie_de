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
        #get company name
        company_name = response.css('.h2 ::text').get()
        if not company_name:
            company_name = "N/A"

        #setting up dictionary for icon classes and their respective data labels
        icon_map = {
          'fa-globe': 'Website',
          'fa-envelope': 'Email',
          'fa-phone': 'Phone',
          'fa-fax': 'Fax',
          'fa-map-pin': 'Address',
          'fa-group': 'Employees',
          'fa-flag': 'Established',
          'fa-money': 'Revenue'
        }

        #default values for the outcome
        data = {
          'Company Name': company_name,
          'Website': 'N/A',
          'Email': 'N/A',
          'Phone': 'N/A',
          'Fax': 'N/A',
          'Address': 'N/A',
          'Employees': 'N/A',
          'Established': 'N/A',
          'Revenue': 'N/A'
        }

        # get contact data and icons
        icons = response.css('.info-icon i::attr(class)').getall()
        contact_info = response.css('dd.info-contact-data').getall()

        #loop through the icon classes storen in "icons" and update the data dictionary accordingly
        for i, icon in enumerate(icons):
          if "fa-globe" in icon:
            data['Website'] = contact_info[i].replace('<dd class="info-contact-data">', '').replace('</dd>', '').strip()

          elif "fa-envelope" in icon:
            data['Email'] = contact_info[i].replace('<dd class="info-contact-data">', '').replace('<br>', '').replace(
              '</dd>', '').strip()

          elif "fa-phone" in icon:
            data['Phone'] = contact_info[i].replace('<dd class="info-contact-data">', '').replace('</dd>', '').strip()

          elif "fa-fax" in icon:
            data['Fax'] = contact_info[i].replace('<dd class="info-contact-data">', '').replace('</dd>', '').strip()

          elif "fa-group" in icon:
            data['Employees'] = contact_info[i].replace('<dd class="info-contact-data">', '').replace('</dd>', '').strip()

          elif "fa-flag" in icon:
            data['Established'] = contact_info[i].replace('<dd class="info-contact-data">', '').replace('</dd>', '').strip()

          elif "fa-money" in icon:
            data['Revenue'] = contact_info[i].replace('<dd class="info-contact-data">', '').replace('</dd>', '').strip()

          elif "fa-map-pin" in icon:
            address_parts = contact_info[i].split('<br>')
            data['Address'] = ', '.join(
              [part.strip() for part in address_parts if part and not part.startswith('<dd')]).replace(', </dd>',
                                                                                                       '').strip()
        #dictionary for the social media icons that are not visible in inspect mode. It is pure evil...
        social_media_map = {
          'fa-facebook-square': 'Facebook',
          'fa-google-plus-square': 'Google+',
          'fa-twitter-square': 'Twitter',
          'fa-youtube-square': 'YouTube',
          'fa-instagram': 'Instagram',
          'fa-rss-square': 'RSS',
          'fa-xing-square': 'Xing',
          'fa-linkedin-square': 'LinkedIn'
        }

        #default values for the social media
        for key in social_media_map:
          data[social_media_map[key]] = 'N/A'

        #extract social media links and add them to data
        for key, value in social_media_map.items():
          link = response.css(f'a i.{key}').xpath('..').css('::attr(href)').get()
          if link:
            data[value] = link
        yield data

