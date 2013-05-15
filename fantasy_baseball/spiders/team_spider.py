from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from fantasy_baseball.items import TeamPlayerItem

class TeamSpider(BaseSpider):
  name = "fbb"
  allowed_domains = ["games.espn.go.com"]

  def start_requests(self):
    teamRequest = Request("http://games.espn.go.com/flb/clubhouse?leagueId=17692&teamId=8&seasonId=2013", callback=self.parse_team)

    return [teamRequest]

  def parse_team(self, response):
    print response.status
    f = open('/home/kevin/fbb_page.html', 'w')
    f.write(response.body)
    f.close()
    hxs = HtmlXPathSelector(response)
    pRow = hxs.select("//table[@id='playertable_0']/tr[position()>2]")

    items = []    

    for player in pRow:
      
      
      item = TeamPlayerItem()
      pId = player.select('td[position()=1]/@class').extract()
      item ['playerId'] = pId
      print 'class is ' + ''.join(pId)
      items.append(item)
#    pName = hxs.select("//table[@id='playertable_0']/tr[3]/td[2]/a/text()").extract()
#    item = TeamPlayerItem()
#    item['playerName'] = pName
#    print item['playerName']

SPIDER = TeamSpider()
