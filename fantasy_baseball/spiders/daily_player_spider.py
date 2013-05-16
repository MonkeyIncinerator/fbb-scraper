import re
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from fantasy_baseball.items import TeamPlayerItem

class DailyPlayerSpider(BaseSpider):
  name = "fbb-players"
  allowed_domains = ["games.espn.go.com"]
  start_urls = [
    "http://games.espn.go.com/flb/playertable/prebuilt/freeagency?leagueId=17692&teamId=8&seasonId=2013&avail=-1&view=stats&context=freeagency&startIndex=0&version=last7",
    "http://games.espn.go.com/flb/playertable/prebuilt/freeagency?leagueId=17692&teamId=8&seasonId=2013&avail=-1&view=stats&context=freeagency&startIndex=0&version=last15",
    "http://games.espn.go.com/flb/playertable/prebuilt/freeagency?leagueId=17692&teamId=8&seasonId=2013&avail=-1&view=stats&context=freeagency&startIndex=0&version=last30",
    "http://games.espn.go.com/flb/playertable/prebuilt/freeagency?leagueId=17692&teamId=8&seasonId=2013&avail=-1&view=stats&context=freeagency&startIndex=0&version=bvp",
  ]

  def make_requests_from_url(self, url):
    return Request(url, callback=self.parse_players)

  def parse_players(self, response):
    hxs = HtmlXPathSelector(response)

    num_str = ''
    regex = re.compile('(.*)(startIndex=)(\d+)(.*)')
    m = regex.match(response.url)
    if m:
      num_str = m.group(3)
      next_num = 50 + int(num_str)
      print next_num
      if next_num < 551:
          key_str = m.group(2)
          print key_str
          val_str = str(next_num)
          print val_str
          replace_str = key_str + val_str
          print replace_str

          next_req_url = re.sub(regex, r'\1' + replace_str + r'\4', response.url)
          print next_req_url
          yield Request(next_req_url, callback=self.parse_players)
    
    pRow = hxs.select("//table[@id='playertable_0']/tr[position()>2]")

    for player in pRow:     
      item = TeamPlayerItem()

      pId = player.select('td[position()=1]/@id').extract()
      item ['playerId'] = pId
      print 'id is ' + pId

      pName = player.select('td[position()=1]/a[position()=1]/text()').extract()
      item['playerName'] = pName
      print 'name is ' + item['playerName']
      yield item

SPIDER = DailyPlayerSpider()
