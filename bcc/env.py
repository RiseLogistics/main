STAGING = False

TOKEN = "1103835E74b52k904294772T197332AC343D33557ad8b5951"

LICENSE_NUMBER_FIELD = "x_license_number"

ALERT_ENDPOINT = STAGING and "https://bcc-api-service-staging.herokuapp.com/api/alert" \
                 or "https://bcc-api-service-prod.herokuapp.com/api/alert"

ODOO_URL_BASE = STAGING and "http://127.0.0.1" or "https://odoo"
