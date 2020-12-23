"""
This module provides a class for reference APIs 
creation related calls to the dwolla API.
"""

from integrations.dwolla.errors import NotFoundError
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
                "id": category["id"],
                "industry-classifications": [
                    {"name": subcategory["name"], "id": subcategory["id"]}
                    for subcategory in category["_embedded"][
                        "industry-classifications"
                    ]
                ],
            }
            for category in categories
        ]
        return {"business-classifications": categories}

    def get_business_classifcation(self, id):
        """
        get list of business classifications
        """
        endpoint = f"/business-classifications/{id}"
        try:
            response = self.get(
                endpoint,
                authenticated=True,
                retry=False,
            )
        except NotFoundError:
            return {}
        response = response.json()

        return {
            "name": response["name"],
            "id": response["id"],
            "industry-classifications": [
                {"name": subcategory["name"], "id": subcategory["id"]}
                for subcategory in response["_embedded"][
                    "industry-classifications"
                ]
            ],
        }
