import googlemaps
import json

from .api_keys import google_apis


class GoogleApiRequest:
    """ This class manage the request to the google APIs """

    GEOCODE_API = google_apis["GEOCODE_API"]

    def __init__(self, query):
        self.query = query
    
    def _geocode_api_request(self):
        """ 
        this method make a request to the google maps geocode API
        The geocode API give data on a place like:
            - geolocation coordinates
            - name of the city
            - name of the country, etc...
        """
        gmaps = googlemaps.Client(key=self.GEOCODE_API)
        return gmaps.geocode(self.query)

    def get_coordinates(self):
        """
        This method catch the geolication coordiantes of a place with the
        geocode API
        """
        # geocode request return a list with one element
        coordinates = self._geocode_api_request()[0]["geometry"]["location"]
        return coordinates["lat"], coordinates["lng"]