import json
import requests
from unidecode import unidecode
from lxml import etree
from lxml.cssselect import CSSSelector
from lxml.html import fromstring

"""
    This class is a bridge between the web crawler and the user
    
    It is in charge of :
    - Holding a list of all the user-created endpoints
    - Returning a JSON representation of what the user asks (as a REST API would do) 
"""


class API:
    # List of all the user-created endpoints
    endpoints = dict()

    # Base URL on which the data should be crawled
    default_endpoint = str()

    # Basic construction with default_endpoint assignation
    def __init__(self, default_endpoint=''):
        self.default_endpoint = default_endpoint

    # Setter for the default api
    def set_api_default_endpoint(self, link):
        self.default_endpoint = link

    # Add an endpoint to the endpoints list stored in self instance
    def register_endpoint(self, identifier, selector, link=None):
        self.endpoints[identifier] = {
            'endpoint': identifier,
            'selector': selector,
            'link': self.default_endpoint if link is None else link,
        }

    # Syntactic sugar as register_endpoint overrides an endpoint if it exists already
    def update_endpoint(self, identifier, selector, link=None):
        self.endpoint_should_exist(identifier)
        self.register_endpoint(identifier, selector, link)

    # Self explanatory
    def remove_endpoint(self, identifier):
        self.endpoint_should_exist(identifier)

        del self.endpoints[identifier]

    # Crawl the web page linked to the identifier representing the endpoint and returns its JSON representation
    # It supports filtering (including or excluding)
    def request_endpoint(self, identifier, filter=None, is_filter_including=False):
        self.endpoint_should_exist(identifier)

        endpoint = self.endpoints[identifier]
        data = {
            identifier: {
                'api_endpoint': endpoint,
                'content': []
            }
        }

        elements = self.crawl_page(endpoint['link'], endpoint['selector'])
        for e in elements:
            api_object = {
                'properties': {attr: unidecode(e.attrib[attr]) for attr in e.attrib},
                'text': unidecode(e.text_content().strip()),
                'tag': e.tag.strip(),
                'html': unidecode(str(etree.tostring(e, pretty_print=True)))
            }
            if (filter is None) or len(filter) == 0 or (
                    any(i.lower() in api_object['text'].lower() for i in filter) and is_filter_including) \
                    or (not (any(i.lower() in api_object['text'].lower() for i in filter)) and not is_filter_including):
                data[identifier]['content'].append(api_object)

        return json.dumps(data, indent=4, ensure_ascii=False)

    # Getter for the self endpoints list
    def endpoints_list(self):
        return self.endpoints

    # Check if the supplied identifier is associated to an existing endpoint
    def endpoint_should_exist(self, identifier):
        if identifier not in self.endpoints:
            raise KeyError('This endpoint does not exist : {}'.format(identifier))

    # Make a GET request and filter the page with the given CSS selector
    @staticmethod
    def crawl_page(url, selector):
        try:
            # Fake browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }
            page_content = fromstring(requests.get(url, headers=headers).content)
            filter = CSSSelector(selector)
            return filter(page_content)
        except:
            raise ConnectionError('Impossible to crawl the web page supplied : {}. '
                                  'Please check your internet connection and the selector supplied : {}.'.format(url,
                                                                                                                 selector))

    # Equivalent of Java toString()
    def __str__(self):
        return str(self.endpoints)
