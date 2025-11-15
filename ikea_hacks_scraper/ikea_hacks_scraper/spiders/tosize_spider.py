import scrapy
from scrapy_playwright.page import PageMethod
from ikea_hacks_scraper.items import IkeaHackItem

class TosizeSpider(scrapy.Spider):
    name = 'tosize'
    allowed_domains = ['tosize.it']
    
    def start_requests(self):
        urls = ['https://www.tosize.it/en-it/diy/type/ikea-hacks']
        for url in urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_timeout", 3000),
                    ],
                },
                callback=self.parse
            )
    
    async def parse(self, response):
        """Parse listing page"""
        page = response.meta["playwright_page"]
        
        try:
            # Try multiple selectors
            project_links = response.css('article a::attr(href)').getall()
            
            if not project_links:
                project_links = response.css('a.project-link::attr(href)').getall()
            if not project_links:
                project_links = response.css('div.project-item a::attr(href)').getall()
            if not project_links:
                project_links = response.css('a[href*="/diy/"]::attr(href)').getall()
            
            # Filter for project URLs
            project_links = [link for link in project_links if link and '/diy/' in link and '/type/' not in link]
            project_links = list(set(project_links))
            
            self.logger.info(f'Found {len(project_links)} projects on: {response.url}')
            
            for link in project_links[:20]:
                full_url = response.urljoin(link)
                yield scrapy.Request(
                    full_url,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_timeout", 2000),
                        ],
                    },
                    callback=self.parse_project
                )
            
            # Pagination
            next_page = response.css('a.next::attr(href)').get()
            if not next_page:
                next_page = response.css('link[rel="next"]::attr(href)').get()
            
            if next_page:
                self.logger.info(f'Following next page: {next_page}')
                yield scrapy.Request(
                    response.urljoin(next_page),
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_timeout", 3000),
                        ],
                    },
                    callback=self.parse
                )
        finally:
            await page.close()
    
    async def parse_project(self, response):
        """Parse individual project"""
        page = response.meta["playwright_page"]
        
        try:
            item = IkeaHackItem()
            
            item['title'] = response.css('h1::text').get()
            if not item['title']:
                item['title'] = response.css('title::text').get()
            
            if item['title']:
                item['title'] = item['title'].strip()
            
            content_parts = response.css('div.description p::text').getall()
            if not content_parts:
                content_parts = response.css('article p::text').getall()
            if not content_parts:
                content_parts = response.css('div.content p::text').getall()
            item['content'] = ' '.join([p.strip() for p in content_parts if p.strip()])
            
            item['author'] = response.css('span.author::text').get() or 'Tosize Community'
            item['date'] = response.css('time::attr(datetime)').get()
            item['url'] = response.url
            item['categories'] = ['ikea-hacks', 'diy']
            item['tags'] = ['ikea', 'hack', 'diy']
            item['image_url'] = response.css('img::attr(src)').get()
            
            excerpt = item['content'][:200] + '...' if item['content'] and len(item['content']) > 200 else item['content']
            item['excerpt'] = excerpt or item['title']
            
            if item['title']:
                self.logger.info(f'✓ Scraped: {item["title"][:60]}')
                yield item
        finally:
            await page.close()