import requests
from bs4 import BeautifulSoup
import os

############ SETTINGS
### crawling:
# main
main_source = 'https://clbokea.github.io/exam/' #get HTML structure of the main page
main_page_href_ending = "index.html"
# navigation specification. Container - container with all nav items. Nav_item - particular nav_item (link) specification
nav_container_tag = "ul"
nav_container_class = "navbar-nav"
nav_item_tag = "a"
nav_item_class = "nav-link"
# restricted content - the content within specified tag and class
restricted_content_tag = "article"
restricted_content_class = "container"

### scraping:
list_of_tags_you_want_to_scrape = ['h1', 'h2', 'h3', 'p', 'li'] #list of the tags which should be scraped

### saving:
name_of_file_with_final_content = "file.md" #name of the file which contains the final scraped text


############ FUNCTIONS

### initial process:
def removeAlreadyExistedFile():
    if os.path.exists(name_of_file_with_final_content): #check if markdown file with the content already exists in the folder
       os.remove(name_of_file_with_final_content) #if file already exists then remove it

### crawling:
# crawling main 3 steps are: 
# 1. get an HTML content from the specified web domain
# 2. parse this HTML to BeautifulSoup object
# 3. find - crawl what you are looking for
def crawlingAndScraping():
    # crawling - crawl content of the page
    # scraping - get only the content from navigation-pages
    nav_links = getLinksInNavigation()

    # crawling - all links in navigation - got from function getLinksInNavigation()
    # scraping - get restricted content from these links
    for nav_link in nav_links:
        restricted_content = getContentFromMenuLink(nav_link['href']) 
        writeRestrictedContentToFile(restricted_content) #calling saving function

def getLinksInNavigation():
    # main_source and main_page_href_ending can be found in settings
    main_page_content = requests.get(main_source+main_page_href_ending).text
    # parse the main_source (specified in settings) and main_page_href_ending (usually index.html) to BeautifulSoup object
    soup_main = BeautifulSoup(main_page_content, "html.parser") 
    #find all navigation links (specified in settings) in navigation AND get only their content
    nav_links = soup_main.find(nav_container_tag, nav_container_class).find_all(nav_item_tag, nav_item_class) 
    return nav_links

        
#get content from the page by adding path ending to the link
def getContentFromMenuLink(href_ending):
    particular_page_content = requests.get(main_source+href_ending).text 
    soup_each_page = BeautifulSoup(particular_page_content, "html.parser")
    # restricted_content - content within specified tag (with class). Can be found in settings
    restricted_content = soup_each_page.find(restricted_content_tag, restricted_content_class)
    return restricted_content


### saving: 
# takes restricted_content after scraping as a parameter and saving to the file
def writeRestrictedContentToFile(restricted_content):
    # parse restricted_content. Parsed_content then has correct order as it has in original webpage and can be saved
    # list will convert the generator to list (iterable) form
    parsed_content = list(parse(restricted_content))

    # creating list which will be populated with converted HTML -> md tags
    md_list = []
    with open(name_of_file_with_final_content, 'a+') as f:
        for line in parsed_content:
                if line.name == "p":
                        md_list.append("\n" + line.text.strip() + "\n")
                elif line.name == "h1":
                        md_list.append("\n# " + line.text.strip())
                elif line.name == "h2":
                        md_list.append("\n## " + line.text.strip())
                elif line.name == "h3":
                        md_list.append("\n### " + line.text.strip())
                elif line.name == "li":
                        md_list.append("\n* " + line.text.strip() + "\n")
                else:
                        print("writeRestrictedContentToFile: Found unexpected value while adding: " +line.name)
        for md_line in md_list:
                f.write(md_line)
        f.write("\n<hr>\n")


def parse(content):
    #parse uses a generator to first check if the passed bs4 object has a tag that belongs to the "list_of_tags_you_want_to_scrape" list
    #if tag name is in the list, yield the value
    #.name attribute is the tag name itself (only "p", or "h1", etc.)
   if content.name in list_of_tags_you_want_to_scrape:
      yield content #the value is one bs4.element.Tag object (e.g. <p>example</p> - so <p> Tag object is yield)

    # get attr (field) from yield Tag (content). this attr is "contents" which is content of the Tag. Default contents will be [], if not found
   for i in getattr(content, 'contents', []): 
      yield from parse(i)


def main():
    removeAlreadyExistedFile()
    crawlingAndScraping()

if __name__ == "__main__":
    main()