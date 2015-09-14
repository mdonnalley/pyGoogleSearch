# pyGoogleSearch
Package for collecting and aggregating search results from various Google Sources. 

<b>Exmaple:</b>

from pyGoogleSearch import *

topic = 'hello world'

<p>raw_web_data = Google(topic, pages=5).search()</p>
<p>output_web_data = DataHandler(raw_web_data).aggregate_data()</p>
<p>write_to_csv(output_web_data, 'web_data.csv')</p>
<br></br>
<p>raw_news_data = Google(topic, pages=5).search_news()</p>
<p>output_news_data = DataHandler(raw_news_data).aggregate_data()</p>
<p>write_to_csv(output_news_data, 'news_data.csv')</p>
<br></br>
<p>raw_scholar_data = Google(topic, pages=5).search_scholar()</p>
<p>output_scholar_data = DataHandler(raw_scholar_data).aggregate_data()</p>
<p>write_to_csv(output_scholar_data, 'scholar_data.csv')</p>
<br></br>

<b>The DataHandler module</b>
The module takes the json that is returned from the Google().search() functions and does two things:
<ol>
<li>Scrapes all visible text from URLs that are returned from the search</li>
<li>Formats data for outputting to CSV with the data points below</li>
</ol>

<b>Data points returned for a web search:</b>
<ol>
<li>URL</li>
<li>Link Text</li>
<li>Link Info</li>
<li>Ranking </li>
<li>Content</li>
</ol>
<b>Data points returned for a news search:</b>
<ol>
<li>URL</li>
<li>Link Text</li>
<li>Link Info</li>
<li>Source</li>
<li>Time</li>
<li>Ranking</li>
<li>Content</li>
</ol>
<b>Data points for scholar search:</b>
<ol>
<li>URL</li>
<li>Title</li>
<li>Excerpt</li>
<li>Citations</li>
<li>Year</li>
<li>Ranking</li>
<li>Content</li>
</ol>

<b>The ImportExportFucntions module</b>
Contains the following functions for importing and exporting data<ul>
<li>write_to_txt(data, output_file)</li>
<li>write_to_csv(data, output_file)</li>
<li>write_to_json(data, output_file)</li>
<li>open_json(input_file)</li>
</ul>

<b>Additionally, there are some flaws to be aware of: </b>
<ul>
<li>The scholar function has a few flaws in how it collects data. Part of this is due to inconsistencies in how google renders their scholar results but regardless I need to revisit so that I can handle those inconsistencies better</li>
<li>The function I’ve written to collect all the content from the search results cannot handle select websites and every so often returns nothing. Additionally, some websites will return a 404 error when you try to scrape it. The script does not break when this happens, it merely takes note and continues. It’s just important to know that because the function tries to grab all text from all the urls, it will inevitably miss on a few. Unfortunately, I believe that’s just the nature of the beast.</li>
</ul>
