import scrapy
from scrapy_playwright.page import PageMethod
from ikea_hacks_scraper.items import IkeaHackItem

class LovePropertySpider(scrapy.Spider):
    name = 'loveproperty'
    allowed_domains = ['loveproperty.com']
    
    # Words that indicate junk/non-content items
    JUNK_KEYWORDS = [
        'store and/or access', 'advertising', 'personalised', 'privacy',
        'consent', 'cookie', 'gdpr', 'data', 'profiles', 'measure',
        'understand audiences', 'develop and improve', 'security',
        'fraud', 'deliver and present', 'communicate privacy',
        'match and combine', 'link different devices', 'identify devices'
    ]
    
    def start_requests(self):
        url = 'https://www.loveproperty.com/gallerylist/75470/genius-ikea-hacks-for-every-room'
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_timeout", 4000),
                ],
            },
            callback=self.parse
        )
    
    def is_junk_title(self, title):
        """Check if title contains junk/privacy policy keywords"""
        if not title:
            return True
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.JUNK_KEYWORDS)
    
    async def parse(self, response):
        """Parse gallery/listicle page"""
        page = response.meta["playwright_page"]
        
        try:
            gallery_items = response.css('div.gallery-item')
            
            if not gallery_items:
                gallery_items = response.css('article.gallery-slide')
            if not gallery_items:
                gallery_items = response.css('div.slide')
            if not gallery_items:
                gallery_items = response.css('div:has(h2), div:has(h3)')
            
            self.logger.info(f'Found {len(gallery_items)} potential gallery items on: {response.url}')
            
            if len(gallery_items) == 0:
                self.logger.info('No gallery items found, treating as single article')
                item = await self.parse_single_article(response)
                if item:
                    yield item
            else:
                scraped_count = 0
                for idx, item_section in enumerate(gallery_items[:50]):
                    item = IkeaHackItem()
                    
                    title = item_section.css('h2::text').get()
                    if not title:
                        title = item_section.css('h3::text').get()
                    if not title:
                        title = item_section.css('h4::text').get()
                    
                    if title:
                        title = title.strip()
                    else:
                        continue
                    
                    # Skip junk titles
                    if self.is_junk_title(title):
                        self.logger.debug(f'Skipping junk item: {title[:50]}')
                        continue
                    
                    # Skip duplicates (same title appearing multiple times)
                    # This is a simple check - you might want to track seen titles
                    
                    paragraphs = item_section.css('p::text').getall()
                    content = ' '.join([p.strip() for p in paragraphs if p.strip()])
                    
                    # Skip if no real content
                    if not content or len(content) < 50:
                        continue
                    
                    image = item_section.css('img::attr(src)').get()
                    if not image:
                        image = item_section.css('img::attr(data-src)').get()
                    
                    item['title'] = title
                    item['content'] = content
                    item['author'] = 'Love Property'
                    
                    date = response.css('time::attr(datetime)').get()
                    if not date:
                        date = response.css('meta[property="article:published_time"]::attr(content)').get()
                    item['date'] = date
                    
                    item['url'] = response.url + f'#slide-{idx+1}'
                    item['categories'] = ['ikea-hacks', 'home-improvement']
                    item['tags'] = ['ikea', 'hack', 'diy', 'home']
                    item['image_url'] = image
                    
                    excerpt = content[:200] + '...' if len(content) > 200 else content
                    item['excerpt'] = excerpt
                    
                    scraped_count += 1
                    self.logger.info(f'✓ Scraped gallery item: {title[:60]}')
                    yield item
                
                self.logger.info(f'Scraped {scraped_count} valid items (filtered out junk)')
            
            # Look for related articles
            related_links = response.css('a[href*="ikea"]::attr(href)').getall()
            related_links = [link for link in related_links if '/gallery' in link or '/article' in link]
            related_links = list(set(related_links))[:5]
            
            for link in related_links:
                full_url = response.urljoin(link)
                if full_url != response.url:
                    self.logger.info(f'Following related article: {full_url}')
                    yield scrapy.Request(
                        full_url,
                        meta={
                            "playwright": True,
                            "playwright_include_page": True,
                            "playwright_page_methods": [
                                PageMethod("wait_for_timeout", 4000),
                            ],
                        },
                        callback=self.parse
                    )
        finally:
            await page.close()
    
    async def parse_single_article(self, response):
        """Parse a single long-form article (fallback)"""
        item = IkeaHackItem()
        
        item['title'] = response.css('h1::text').get()
        if not item['title']:
            item['title'] = response.css('title::text').get()
        
        if item['title']:
            item['title'] = item['title'].strip()
        
        paragraphs = response.css('article p::text').getall()
        if not paragraphs:
            paragraphs = response.css('div.content p::text').getall()
        if not paragraphs:
            paragraphs = response.css('p::text').getall()
        
        item['content'] = ' '.join([p.strip() for p in paragraphs if p.strip()])
        
        item['author'] = response.css('span.author::text').get()
        if not item['author']:
            item['author'] = 'Love Property'
        
        item['date'] = response.css('time::attr(datetime)').get()
        if not item['date']:
            item['date'] = response.css('meta[property="article:published_time"]::attr(content)').get()
        
        item['url'] = response.url
        item['categories'] = ['ikea-hacks', 'home-improvement']
        item['tags'] = ['ikea', 'hack', 'diy', 'home']
        
        item['image_url'] = response.css('meta[property="og:image"]::attr(content)').get()
        if not item['image_url']:
            item['image_url'] = response.css('article img::attr(src)').get()
        
        excerpt = item['content'][:200] + '...' if item['content'] and len(item['content']) > 200 else item['content']
        item['excerpt'] = excerpt or item['title']
        
        if item['title'] and not self.is_junk_title(item['title']):
            self.logger.info(f'✓ Scraped single article: {item["title"][:60]}')
            return item
        
        return None