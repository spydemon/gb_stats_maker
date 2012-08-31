# Scrapy settings for gb_stats_maker project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'gb_stats_maker'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['gb_stats_maker.spiders']
NEWSPIDER_MODULE = 'gb_stats_maker.spiders'
DEFAULT_ITEM_CLASS = 'gb_stats_maker.items.GbStatsMakerItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

