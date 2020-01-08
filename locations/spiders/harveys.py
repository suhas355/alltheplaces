# -*- coding: utf-8 -*-
import json
import re

import scrapy

from locations.items import GeojsonPointItem
from locations.hours import OpeningHours


class HarveysSpider(scrapy.Spider):
    name = "harveys"
    item_attributes = {'brand': "Harvey's"}
    allowed_domains = ['harveys.ca']
    start_urls = [
        'https://aws-api.harveys.ca/CaraAPI/servlet/VESBCmdServlet?application=VECOMV1&service=OrganizationService&command=getStoreList&reqJSON=%7B%22request%22%3A%7B%22requestHeader%22%3A%7B%22caller%22%3A%22Mobile%22%2C%22sessionId%22%3A%224297736%22%7D%2C%22requestContent%22%3A%7B%22@class%22%3A%22storeListRqstModel%22%2C%22eCommOnly%22%3A%22N%22%2C%22fromLatitude%22%3A90.000%2C%22toLatitude%22%3A0.000%2C%22fromLongitude%22%3A-180.000%2C%22toLongitude%22%3A-1.56301%7D%7D%7D',
    ]
    download_delay = 2

    def parse(self, response):
        places = json.loads(response.body_as_unicode())

        for place in places["response"]["responseContent"]["storeModel"]:
            properties = {
                'ref': place["storeNumber"],
                'name': place["storeName"],
                'addr_full': str(place["streetNumber"]) + " " + place["street"],
                'city': place["city"],
                'state': place["province"],
                'postcode': place["postalCode"],
                'country': 'CA',
                'lat': place["latitude"],
                'lon': place["longitude"],
                'phone': place["phoneNumber"]
            }

            yield GeojsonPointItem(**properties)
