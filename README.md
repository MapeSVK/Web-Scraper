## Python Elective Final Project - Web Scraper & Crawler
### About the project:
**_web_scraper_** scraps a website which in different words means to browse (crawl) the website first, and then reformat and extract the data we need. 

Python is a good choice for this manipulation due to its efficiency, simplicity, and stability.

For a better transparency and reusability of the code, I refactored and generalised the variables and functions as much as possible. Therefore variables can be found at the very beginning of the file which is especially usefull when the user wants to quickly change the tags whose content should be included in the result file. 

Transparency of the code was also increased after refactoring the functions and adding comments which help user to understand the code even quicker and deeper.

### How _web_scraper_ works:
The best way how to describe the functionality of _web_scraper_ is by specifying its steps:

1. Firstly, in the case that there is a file which holds the markdown result, _removeAlreadyExistedFile()_ deletes that file.
2. A request to get (GET) data from the website is made via _getLinksInNavigation()_ function. The result is then parsed to BeautifulSoup objects so therefore it is possible to find all links (menu items) in navigation and **crawl** them.
3. _getContentFromMenuLink()_ function will take care of scraping those pages by taking only the content within specified tag. 
4. Then the user can decide which <tags> should be included while scraping the content. These tags are specified at the very beginning of the scraper.
5. Using **generator**, _parse()_ will then check if the tag from the specified list exists also in the already scraped content and if so, yields that value. Then _parse()_ iterates over the contents of that object and call itself on each element. This helps to keep the same order of the tags as it had before scraping.
6. Lastly, _writeRestrictedContentToFile()_ will change HTML tags to markdown syntax and then save the result as a markdown file in the folder.
