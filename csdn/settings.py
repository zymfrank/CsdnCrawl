# Scrapy settings for pointacre project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'csdn'

SPIDER_MODULES = ['csdn.spiders']
NEWSPIDER_MODULE = 'csdn.spiders'

# FEED_URI='userinfo.csv'
# FEED_FORMAT='csv'

ITEM_PIPELINES={
    'csdn.pipelines.CsdnPipeline':100
}
LOG_ENABLED=True
LOG_LEVEL='INFO'
#LOG_FILE='crawl.log'
STATS_DUMP=False

COOKIES_ENABLED=False

RANDOMIZE_DOWNLOAD_DELAY=True
DOWNLOAD_DELAY = 0.1
DOWNLOAD_TIMEOUT=30

USER_AGENt="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36"

#TELNETCONSOLE_PORT=[6023,6024,6025,6026,6073]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pointacre (+http://www.yourdomain.com)'
