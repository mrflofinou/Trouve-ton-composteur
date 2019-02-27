from django.test import TestCase
from unittest.mock import patch

from ..libs.google_map_API import GoogleApiRequest

class GoogleApiRequestTestCase(TestCase):
    
    @patch("composteur.libs.google_map_API.GoogleApiRequest._geocode_api_request")
    def test_get_coordinates(self, mock_geocode_api_request):
        mock_geocode_api_request.return_value = [
        {
            "formatted_address" : "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
            "geometry" : {
                "location" : {
                "lat" : 37.4224764,
                "lng" : -122.0842499
                },
                "location_type" : "ROOFTOP",
                "viewport" : {
                "northeast" : {
                    "lat" : 37.4238253802915,
                    "lng" : -122.0829009197085
                },
                "southwest" : {
                    "lat" : 37.4211274197085,
                    "lng" : -122.0855988802915
                }
                }
            },
        }
        ]

        google_request = GoogleApiRequest("1600 Amphitheatre Parkway, Mountain View, CA") 
        coordinates = google_request.get_coordinates()
        self.assertEqual(coordinates, (37.4224764, -122.0842499))
