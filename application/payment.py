import xml.etree.cElementTree as etree

try:
    # Python 3
    from html import escape
except ImportError:
    # Python 2
    from cgi import escape

from . import oauth
from .oauth import OAuthConsumer, OAuthRequest

SIGNATURE_METHOD = oauth.OAuthSignatureMethod_HMAC_SHA1()

from django.conf import settings


class MissingKeyError(Exception):
    pass


class InvalidOption(Exception):
    pass


# method to validate passed options
def validateOptions(options, default_options):
    for k, v in list(options.items()):
        if k not in default_options:
            msg = 'Option %s not found in %s' % (k, list(default_options.keys()))
            raise InvalidOption(msg)


# method to build and return oauth request
def createOauthRequest(http_url, params, default_params):
    validateOptions(params, default_params)

    default_params.update(params)
    params = default_params

    http_method = 'GET'
    token = params.pop('token', None)

    base_url = 'https://www.pesapal.com/api/'
    if settings.TESTING:
        base_url = 'https://demo.pesapal.com/api/'

    url = base_url + http_url

    if not settings.PESAPAL_CONSUMER_KEY:
        raise MissingKeyError('provide consumer key')
    if not settings.PESAPAL_SECRET_KEY:
        raise MissingKeyError('provide consumer consumer_secret')
    oauth_consumer = oauth.OAuthConsumer(settings.PESAPAL_CONSUMER_KEY, settings.PESAPAL_SECRET_KEY)

    request = OAuthRequest.from_consumer_and_token(
        oauth_consumer,
        http_url=url,
        http_method=http_method,
        parameters=params
    )
    request.sign_request(SIGNATURE_METHOD, oauth_consumer, token)
    return request.to_url()


def postDirectOrder(params, request_data):
    """
    PostPesapalDirectOrderV4
    ---
    Use this to post a transaction to PesaPal.
    PesaPal will present the user with a page which contains the available payment
    options and will redirect to your site once the user has completed the payment process.
    """

    default_request_data = {
        'Amount': '',
        'Description': '',
        'Type': 'MERCHANT',
        'Reference': '',
        'Email': '',
        'PhoneNumber': '',
        # optional
        'Currency': '',
        'FirstName': '',
        'LastName': '',
        'LineItems': [
            # {
            #     'uniqueid': '',
            #     'particulars': '',
            #     'quantity': '',
            #     'unitcost': '',
            #     'subtotal': ''
            # }
        ]
    }

    # validate xml data
    validateOptions(request_data, default_request_data)
    default_request_data.update(request_data)
    request_data = default_request_data

    root_xml = etree.Element('PesapalDirectOrderInfo')
    root_xml.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
    root_xml.attrib['xmlns:xsd'] = 'http://www.w3.org/2001/XMLSchema'
    root_xml.attrib['xmlns'] = 'http://www.pesapal.com'

    # populate line items
    line_items = request_data.pop('LineItems')
    if len(line_items) > 0:
        line_items_xml = etree.SubElement(root_xml, 'lineitems')
        for item in line_items:
            item_xml = etree.SubElement(line_items_xml, 'lineitem')
            item_xml.attrib.update(item)

    # populate info
    root_xml.attrib.update(request_data)

    # pesapal_request_data
    pesapal_request_data = escape(etree.tostring(root_xml).decode("utf-8"))
    # print etree.tostring(root_xml)
    default_params = {
        'oauth_callback': '',
        # 'oauth_consumer_key': '',
        # 'oauth_nonce': '',
        # 'oauth_signature': '',
        # 'oauth_signature_method': '',
        # 'oauth_timestamp': '',
        # 'oauth_version': '1.0',
        'pesapal_request_data': pesapal_request_data
    }

    http_url = 'PostPesapalDirectOrderV4'
    return_url = createOauthRequest(http_url, params, default_params)
    print(return_url)
    return return_url


def queryPaymentStatus(params):
    """
    Use this to query the status of the transaction.
    When a transaction is posted to PesaPal, it may be in a PENDING, COMPLETED or FAILED state.
    If the transaction is PENDING, the payment may complete or fail at a later stage.
     Both the unique order id generated by your system and the pesapal tracking id are required as input parameters.
    """
    http_url = 'QueryPaymentStatus'

    default_params = {
        'pesapal_merchant_reference': '',
        'pesapal_transaction_tracking_id': ''
    }

    return createOauthRequest(http_url, params, default_params)


def queryPaymentStatusByMerchantRef(params):
    """
    Same as QueryPaymentStatus, but only the unique order id generated
    by your system is required as the input parameter.
    """

    http_url = 'QueryPaymentStatusByMerchantRef'

    default_params = {
        'pesapal_merchant_reference': ''
    }

    return createOauthRequest(http_url, params, default_params)


def queryPaymentDetails(params):
    """
    Same as QueryPaymentStatus, but additional information is returned.
    """

    http_url = 'QueryPaymentDetails'

    default_params = {
        'pesapal_merchant_reference': '',
        'pesapal_transaction_tracking_id': ''
    }

    return createOauthRequest(http_url, params, default_params)
