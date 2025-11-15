import scrapy
from scrapy_playwright.page import PageMethod
from ikea_hacks_scraper.items import IkeaHackItem

class IkeaSpider(scrapy.Spider):
    name = 'ikea'
    allowed_domains = ['ikeahackers.net']
    
    def start_requests(self):
        urls = ['https://ikeahackers.net/category/hacks']
        for url in urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "article", timeout=10000),
                    ],
                },
                callback=self.parse
            )
    
    async def parse(self, response):
        """Parse category listing page"""
        page = response.meta["playwright_page"]
        
        try:
            # Extract article links
            article_links = response.css('article h2 a::attr(href)').getall()
            
            # Try alternative selectors if needed
            if not article_links:
                article_links = response.css('article a[rel="bookmark"]::attr(href)').getall()
            if not article_links:
                article_links = response.css('h2.entry-title a::attr(href)').getall()
            if not article_links:
                article_links = response.css('article a::attr(href)').getall()
            
            # Filter for article URLs only
            article_links = [link for link in article_links if link and link.startswith('http') and '/category/' not in link]
            article_links = list(set(article_links))  # Remove duplicates
            
            self.logger.info(f'Found {len(article_links)} articles on: {response.url}')
            
            # Follow each article
            for link in article_links[:20]:  # Limit to 20 per page
                yield scrapy.Request(
                    link,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", "article", timeout=10000),
                        ],
                    },
                    callback=self.parse_article
                )
            
            # Pagination
            next_page = response.css('a.next::attr(href)').get()
            if not next_page:
                next_page = response.css('link[rel="next"]::attr(href)').get()
            
            if next_page:
                self.logger.info(f'Following next page: {next_page}')
                yield scrapy.Request(
                    next_page,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", "article", timeout=10000),
                        ],
                    },
                    callback=self.parse
                )
        finally:
            await page.close()
    
    async def parse_article(self, response):
        """Parse individual article"""
        page = response.meta["playwright_page"]
        
        try:
            item = IkeaHackItem()
            
            item['title'] = response.css('h1.entry-title::text').get()
            if not item['title']:
                item['title'] = response.css('h1::text').get()
            
            if item['title']:
                item['title'] = item['title'].strip()
            
            content_paragraphs = response.css('div.entry-content p::text').getall()
            if not content_paragraphs:
                content_paragraphs = response.css('article p::text').getall()
            item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])
            
            item['author'] = response.css('span.author a::text').get()
            if not item['author']:
                item['author'] = response.css('a[rel="author"]::text').get()
            if not item['author']:
                item['author'] = 'IKEA Hackers'
            
            item['date'] = response.css('time::attr(datetime)').get()
            item['url'] = response.url
            
            item['categories'] = response.css('a[rel="category tag"]::text').getall()
            if not item['categories']:
                item['categories'] = ['ikea-hacks']
            
            item['tags'] = response.css('a[rel="tag"]::text').getall()
            if not item['tags']:
                item['tags'] = ['ikea', 'hack', 'diy']
            
            item['image_url'] = response.css('article img::attr(src)').get()
            if not item['image_url']:
                item['image_url'] = response.css('meta[property="og:image"]::attr(content)').get()
            
            excerpt = item['content'][:200] + '...' if item['content'] and len(item['content']) > 200 else item['content']
            item['excerpt'] = excerpt or item['title']
            
            if item['title']:
                self.logger.info(f'✓ Scraped: {item["title"][:60]}')
                yield item
            else:
                self.logger.warning(f'Skipped: No title at {response.url}')
        finally:
            await page.close()