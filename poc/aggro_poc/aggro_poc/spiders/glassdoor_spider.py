import scrapy
from scrapy.loader import ItemLoader
from ..items import JobItem


class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'
    start_urls = [
        'https://www.glassdoor.com/Job/thailand-software-engineer-jobs-SRCH_IL.0,8_IN229_KO9,26.htm?fromAge=30', # Thailand
        'https://www.glassdoor.com/Job/singapore-software-engineer-jobs-SRCH_IL.0,9_IC3235921_KO10,27.htm?fromAge=30', # Singapore
        'https://www.glassdoor.com/Job/australia-software-engineer-jobs-SRCH_IL.0,9_IN16_KO10,27.htm?fromAge=30', # Australia
        'https://www.glassdoor.com/Job/malaysia-software-engineer-jobs-SRCH_IL.0,8_IN170_KO9,26.htm?fromAge=30', # Malaysia
    ]

    def parse(self, response):
        for job in response.css('li.jl'):
            # Getting more info from details page
            detail_page = job.css('a').attrib['href']
            detail_url = response.urljoin(detail_page)
            request = scrapy.Request(url=detail_url, callback=self.parse_details, cb_kwargs=dict(
                parent=job))  # passing parent as parameter
            yield request

        num_pages = int(response.css('#ResultsFooter > div::text').get()[-1])
        self.log(num_pages)
        if num_pages > 1:
            for i in range(2, num_pages + 1):
                pagelink = response.css('li.page a::attr(href)').extract_first()
                nextlink = pagelink.replace('IP2', 'IP' + str(i))
                next_page = response.urljoin(nextlink)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_details(self, response, parent):
        # Using Item Loader
        loader = ItemLoader(item=JobItem(), selector=parent)
        loader.add_css('employer', 'div.jobHeader > a > div::text')
        loader.add_css('position', 'a::text')
        loader.add_css('jobLink', 'a::attr(href)')
        loader.add_css('location', 'div.jobInfoItem > span::text')
        #change selector to response
        loader.selector = response
        loader.add_xpath('urgency', '//*[@id="PrimaryModule"]/div/span[1]/text()')
        loader.add_xpath('employerRating', '//*[@id="JobView"]/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/span/text()')
        loader.add_css('details', 'li::text')
        loader.add_css('description', 'div.desc::text')
        yield loader.load_item()
        
''' -------------------------------------------------------------------------------------------------------------------------
DISCARDED CODE

# Getting list of jobs from first page
yield {
    # 'jobContainer': jobs.css('div.jobContainer').get(),
    'employer': jobs.css('div.jobHeader > a > div::text').get(),
    'position': jobs.css('a::text').get(),
    'jobLink': jobs.css('a').attrib['href'],
    'location': jobs.css('div.jobInfoItem > span::text').get(),
}

# Correct way to follow links
for page in response.css('li.page'):
    # self.log(page)
    pagelink = page.css('a::attr(href)').get()
    # self.log(pagelink)
    if pagelink is not None:
        next_page = response.urljoin(pagelink)
        self.log(next_page)
        yield scrapy.Request(next_page, callback=self.parse)

# Using Items with no item loader (not best practice)

item = JobItem() 
item['employer'] = parent.css('div.jobHeader > a > div::text').get(),
item['position'] = parent.css('a::text').get(),
item['jobLink'] = parent.css('a').attrib['href'],
item['location'] = parent.css('div.jobInfoItem > span::text').get(),
item['urgency'] = response.xpath('//*[@id="PrimaryModule"]/div/span[1]/text()').get(),
item['employerRating'] = response.xpath('//*[@id="JobView"]/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/span/text()').get(),
item['details'] = response.css('li::text').getall(),
yield item
      
# yield for debugging
yield {
    'employer': parent.css('div.jobHeader > a > div::text').get(),
    'position': parent.css('a::text').get(),
    'jobLink': parent.css('a').attrib['href'],
    'location': parent.css('div.jobInfoItem > span::text').get(),
    'urgency': response.xpath('//*[@id="PrimaryModule"]/div/span[1]/text()').get(),
    'employerRating': response.xpath('//*[@id="JobView"]/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/span/text()').get(),
    'details': response.css('li::text').getall(),
}

def parse(self, response):
    yield {
        'description': response.css('div.desc::text').get()
    }

## DISCARDED

        self.log(response)
        next_page = response.css('#FooterPageNav > div > ul > li.next a::attr(href)').get()
        self.log(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
        
        next_page = response.xpath(
            "//li[@class='next']/a/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def start_requests(self):
        urls = [
            'https://www.glassdoor.com/Job/bangkok-software-engineer-jobs-SRCH_IL.0,7_IC3179725_KO8,25.htm?fromAge=14'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'glassdoor-se.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
            # f.write(response.xpath('//*[@id="MainCol"]/div[1]/ul/li[1]/div[2]'))
        self.log('Saved file %s' % filename)

'''
