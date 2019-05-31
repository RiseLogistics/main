from ..client.exceptions import LeafLinkClientRequestError


############## Endpoints Single Imports ##############

# Activity Entries
from ..resources.activity_entries import ActivityEntries

# Images endpoints
from ..resources.images           import Images

# License Types endpoints
from ..resources.license_types    import LicenseTypes

# Orders endpoints
from ..resources.orders           import Orders

# Payment Terms endpoints
from ..resources.payment_terms    import PaymentTerms

# Service Zones endpoints
from ..resources.service_zones    import ServiceZones

# Territories endpoints
from ..resources.territories      import Territories


############## Endpoints Collection Imports ##############

# Company endpoints

from ..resources.company_contacts import CompanyContacts  as _CompanyContacts
from ..resources.company_staffs   import CompanyStaffs    as _CompanyStaffs


class Company(object):
    def __init__(self, company, api_key, base_url):
        self.Contacts = _CompanyContacts(company, api_key, base_url)
        self.Staff    = _CompanyStaffs(company, api_key, base_url)


# Customers endpoints

from ..resources.customer_contacts import CustomerContacts    as _CustomerContacts
from ..resources.customer_statuses import CustomerStatuses    as _CustomerStatuses
from ..resources.customer_tiers    import CustomerTiers       as _CustomerTiers
from ..resources.customers         import Customers           as _Customers


class Customers(_Customers):
    def __init__(self, company, api_key, base_url):
        _Customers.__init__(self, company, api_key, base_url)

        self.Contacts = _CustomerContacts(company, api_key, base_url)
        self.Statuses = _CustomerStatuses(company, api_key, base_url)
        self.Tiers    = _CustomerTiers(company, api_key, base_url)


# Discussions endpoints

from ..resources.discussion_messages  import DiscussionMessages   as _DiscussionMessages
from ..resources.discussions          import Discussions          as _Discussions


class Discussions(_Discussions):
    def __init__(self, company, api_key, base_url):
        _Discussions.__init__(self, company, api_key, base_url)
        self.Messages = _DiscussionMessages(company, api_key, base_url)


# Products endpoints

from ..resources.product_line       import ProductLine              as _ProductLines
from ..resources.product_templates  import ProductTemplates         as _ProductTemplates
from ..resources.products           import Products                 as _Products
from ..resources.products           import ProductImages            as _ProductImages
from ..resources.batches            import ProductBatches           as _ProductBatches
from ..resources.batches import AssociateBatches


class Products(_Products):
    def __init__(self, company, api_key, base_url):
        _Products.__init__(self, company, api_key, base_url)

        self.Lines          = _ProductLines(company, api_key, base_url)
        self.Templates      = _ProductTemplates(company, api_key, base_url)
        self.Images         = _ProductImages(company, api_key, base_url)
        self.Batches        = _ProductBatches(company, api_key, base_url)
        self.batch_assign   = AssociateBatches(company, api_key, base_url)
