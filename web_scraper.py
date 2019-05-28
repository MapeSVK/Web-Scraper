import requests
from bs4 import BeautifulSoup
import os

############ SETTINGS
main_source = requests.get('https://clbokea.github.io/exam/index.html').text #get HTML structure of the main page

list_of_tags_you_want_to_scrape = ['h1', 'h2', 'h3', 'p', 'li', 'div'] #list of the tags which should be scraped
name_of_file_with_final_content = "file.md" #name of the file which contains the final scraped text
############

def findLinksInNavigationAndOpen():
    soup_main = BeautifulSoup(main_source, "html.parser") #parse this using bs4
    nav_links = soup_main.find("ul", "navbar-nav").find_all("a", "nav-link") #find all links <a> in navigation

    if os.path.exists(name_of_file_with_final_content): #check if markdown file with the content already exists in the folder
       os.remove(name_of_file_with_final_content) #if file already exists then remove it

    for href in nav_links:
        getContentFromOpenedLink(href['href']) #get content from all pages

        
def getContentFromOpenedLink(href_ending):
    particular_page_content = requests.get('https://clbokea.github.io/exam/'+href_ending).text
    soup_each_html = BeautifulSoup(particular_page_content, "html.parser")

    inner_content = soup_each_html.find("article", "container") #gives me content in article tags
    getOnlyContentFromChosenHTMLTags(inner_content)

def getOnlyContentFromChosenHTMLTags(inner_content):
    result = list(parse(inner_content))
    with open(name_of_file_with_final_content, 'a+') as f:
        f.write('\n'.join(map(str, result)))
        f.write('\n<p>------------------------------------------</p>\n')

def parse(content):
   if content.name in list_of_tags_you_want_to_scrape: 
      yield content
   for i in getattr(content, 'contents', []):
      yield from parse(i)

def main():
    findLinksInNavigationAndOpen()

if __name__ == "__main__":
    main()
