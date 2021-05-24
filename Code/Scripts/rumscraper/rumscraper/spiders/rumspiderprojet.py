import scrapy


class Rumspider(scrapy.Spider):
    name = 'rumy'
    
    start_urls = ['https://www.christiandemontaguere.com/']

    liste_provenance = []

    def start_requests(self):
        liste_provenance = ['3317-les-rhums-de-la-barbade', 
                        '3314-les-rhums-de-la-jamaique', 
                        '3365-les-rhums-de-martinique', 
                        '3354-les-rhums-de-guadeloupe'
                        ]
        for liste in liste_provenance:
            yield scrapy.Request('https://www.christiandemontaguere.com/'+liste, callback=self.parse)

            
   
    def parse(self, response):
        for products in response.css('div.product-container'):
            try:
                    
                yield {
                    'name':  products.css('a.product-name').attrib['title'],
                }
            except:
                yield {
                    'name':  "not found",
                }

        next_page = response.css('li.pagination_next a').attrib['href']
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)