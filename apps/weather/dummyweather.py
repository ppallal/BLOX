import urllib2, urllib,json

baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = "select item from weather.forecast where woeid in (select woeid from geo.places where text='GB-LND') and u='c'"
yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
result = urllib2.urlopen(yql_url).read()
data = json.loads(result)
current_temp = data['query']['results']['channel']['item']['condition']['temp']
current_condition = data['query']['results']['channel']['item']['condition']['text']
today_high = data['query']['results']['channel']['item']['forecast'][0]['high']
today_low = data['query']['results']['channel']['item']['forecast'][0]['low']
print "temp:",current_temp," condition: ",current_condition," today high: ",today_high," today low: ",today_low