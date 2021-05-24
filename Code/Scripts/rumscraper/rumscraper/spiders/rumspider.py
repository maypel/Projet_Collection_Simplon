import scrapy


class Rumspider(scrapy.Spider):
    name = 'demo'
    
    start_urls = ['https://www.christiandemontaguere.com/']

    liste_provenance = []

    def start_requests(self):
        liste_provenance = ['3396-les-rhums-de-belize', 
                        '3312-les-rhums-de-cuba', 
                        '3498-les-rhums-du-japon', 
                        '3467-les-rhums-de-guyana',
                        '3586-les-rhums-de-republique-dominicaine'
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