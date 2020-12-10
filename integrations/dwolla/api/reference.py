"""
This module provides a class for reference APIs 
creation related calls to the dwolla API.
"""

from integrations.dwolla.http import Http

__all__ = "Reference"


class Reference(Http):
    """
    This class provides an interface to the etc. endpoints of the dwolla API.
    """

    def business_classifcations(self):
        """
        get list of business classifications
        """
        response = self.get(
            "/business-classifications",
            authenticated=True,
            retry=False,
        )
        response = response.json()
        categories = response["_embedded"]["business-classifications"]
        categories = [
            {
                "name": category["name"],
                "subcategories": [
                    {"name": subcategory["name"]}
                    for subcategory in category["_embedded"][
                        "industry-classifications"
                    ]
                ],
            }
            for category in categories
        ]
        return categories
