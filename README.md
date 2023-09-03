# Scrapy Project: Industrie.de Spider

This Scrapy project is designed to scrape company details from [industrie.de/firmenverzeichnis/](https://industrie.de/firmenverzeichnis/). The spider extracts each company's information from the section "Daten und Kontakte" on its website.

### 1. Use a web scraping library (e.g., Beautiful Soup, Scrapy) to extract data from the website.

First I explored the structure of the web-site in shell, not to overload the website.
Starting by inspecting of HTML code of the web-side to acquire the selectors and trying out to get pieces of information.

`r = scrapy.Request(url='https://industrie.de/firmenverzeichnis/')`
`fetch(r)` <br>
`response.css('div.infoservice-result-row')` <br>
`response.css('div a::attr(href)').get()` <br>
`response.css('#post-2020 a')` <br>
`response.css('#post-2020 a::attr(href)').getall()` <br>
`response.css('div.h2 ::text').getall()` <br>
`response.xpath('//dd').getall()` <br>
`response.xpath('//div[@class="textwidget"]/dl/dd').getall()` <br>
`response.xpath('//div[@class="textwidget"]/dl/dd/text()').getall()` <br>
`etc.`

After working with shell, the following flaws/challenges were discovered:
* Some of the company links do not exist anymore.
* Some entries in "Daten und Kontakte" are missing, so we have to format check each entry not to mess the dataset we are creating.
For this I used an icon class for each entry type.
* After building up the first version of a spider and looking at the data, I noticed that very few companies have more icon classes such as revenue etc.
So I looked for all possible icon classes in shell:
  * fa fa-globe
  * fa fa-envelope
  * fa fa-phone
  * fa fa-fax
  * fa fa-group
  * fa fa-flag
  * fa fa-money
  * fa fa-map-pin
  * fa-facebook-square
  * fa-google-plus-square
  * fa-twitter-square
  * fa-youtube-square
  * fa-instagram
  * fa-rss-square
  * fa-xing-square
  * fa-linkedin-square

* Since address info consists of several lines, they were joined together and separated with a comma.


