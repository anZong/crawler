import re
import urlparse

from bs4 import BeautifulSoup


class HtmlParser(object):

    def parse(self, page_url,content):
        if page_url is None or content is None:
            return
        dom = BeautifulSoup(content,'html.parser',from_encoding='utf-8')

        new_urls = self._get_new_urls(page_url, dom)
        new_data = self._get_new_data(page_url, dom)


        return new_urls,new_data

    def _get_new_urls(self, page_url, cont):
        new_urls = set()
        #/item/
        links = cont.find_all('a',href=re.compile(r'/item/\w+'))

        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, dom):

        res_data = {}
        #url
        res_data['url'] = page_url

        #<dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        title_node = dom.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        res_data['title'] = title_node.get_text()

        #<div class="lemma-summary" label-module="lemmaSummary">
        summary_node = dom.find('div',class_='lemma-summary')
        res_data['summary'] = summary_node.get_text()

        return res_data