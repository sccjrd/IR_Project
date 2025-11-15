# Scrapy settings for ikea_hacks_scraper project with Playwright

BOT_NAME = "ikea_hacks_scraper"

SPIDER_MODULES = ["ikea_hacks_scraper.spiders"]
NEWSPIDER_MODULE = "ikea_hacks_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Playwright configuration
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Playwright settings
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,  # Set to False to see the browser (useful for debugging)
    "timeout": 60000,  # 60 seconds timeout
}

# Politeness settings
DOWNLOAD_DELAY = 3  # 3 seconds between requests (important with headless browsers)
CONCURRENT_REQUESTS = 4  # Lower concurrency with Playwright
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# User agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Auto-throttle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Disable cookies
COOKIES_ENABLED = False

# Log level
LOG_LEVEL = 'INFO'

# Feed export encoding
FEED_EXPORT_ENCODING = "utf-8"

# Request fingerprinter (required for Playwright)
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

# Retry settings
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 403]