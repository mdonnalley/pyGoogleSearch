# pyGoogleSearch
Package for collecting and aggregating search results from various Google Sources. 

DataHandler contains a web scraping function that will open each of the returned links and collect all the visible text from that web page.

Exmaple:

from pyGoogleSearch import *

topic = 'hello world'

raw_web_data = Google(topic, pages=5).search()
output_web_data = DataHandler(raw_web_data).aggregate_data()
write_to_csv(output_web_data, 'web_data.csv')

raw_news_data = Google(topic, pages=5).search_news()
output_news_data = DataHandler(raw_news_data).aggregate_data()
write_to_csv(output_news_data, 'news_data.csv')

raw_scholar_data = Google(topic, pages=5).search_scholar()
output_scholar_data = DataHandler(raw_scholar_data).aggregate_data()
write_to_csv(output_scholar_data, 'scholar_data.csv')


Data points returned for a web search:
•	URL
•	Link Text
•	Link Info
•	Ranking 
•	Content

Data points returned for a news search:
•	URL
•	Link Text
•	Link Info
•	Source
•	Time
•	Ranking
•	Content

Data points for scholar search:
•	URL
•	Title
•	Excerpt
•	Citations
•	Year
•	Ranking
•	Content

