# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class FantasyBaseballItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class TeamPlayerItem(Item):
    playerId = Field()
    playerName = Field()
    playerPts = Field()
