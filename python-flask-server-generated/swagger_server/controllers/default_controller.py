import connexion
import six

from swagger_server.models.item import Item  # noqa: E501
from swagger_server import util


def item_get():  # noqa: E501
    """item_get

    The item resource is endpoint for CRUD operations with the food in the fridge # noqa: E501


    :rtype: List[Item]
    """
    return 'do some magic!'
