import scrapy


class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'
    start_urls = [
        # Thailand (1 Month)
        'https://www.glassdoor.com/Job/thailand-software-engineer-jobs-SRCH_IL.0,8_IN229_KO9,26.htm?fromAge=30',
    ]

    def parse(self, response):
        for jobs in response.css('li.jl'):
            yield {
                # 'jobContainer': jobs.css('div.jobContainer').get(),
                'employer': jobs.css('div.jobHeader > a > div::text').get().strip(),
                'position': jobs.css('a::text').get().strip(),
                'jobLink': jobs.css('a').attrib['href'].strip(),
                'location': jobs.css('div.jobInfoItem > span::text').get().strip(),
            }
        
        num_pages = int(response.css('#ResultsFooter > div::text').get()[-1])
        self.log(num_pages)
        if num_pages > 1:
            for i in range(2, num_pages + 1):
                pagelink = response.css('li.page a::attr(href)').extract_first()
                nextlink = pagelink.replace('IP2', 'IP' + str(i))
                next_page = response.urljoin(nextlink)
                yield scrapy.Request(next_page, callback=self.parse)

        '''Some missing data'''
        # for page in response.css('li.page'):
        #     # self.log(page)
        #     pagelink = page.css('a::attr(href)').get()
        #     # self.log(pagelink)
        #     if pagelink is not None:
        #         next_page = response.urljoin(pagelink)
        #         self.log(next_page)
        #         yield scrapy.Request(next_page, callback=self.parse)
          


''' DISCARDED CODE

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