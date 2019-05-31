import re


ZIP_REGEX = re.compile(r"(\d{5})")
LICENSE_REGEX = re.compile(r"(\w{2,3}-\d{2}-\d{7}-TEMP|CDPH-T\d{8}|T[A,M]L1[1,8]-\d{7})")
EMAIL_REGEX = re.compile(r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3})")
WEBSITE_REGEX = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
PHONE_REGEX = re.compile(r"[\d\w]")
PHONE = lambda x: "".join(PHONE_REGEX.findall(x))


STATE_CA = "CA"
HAS_MEDICAL = lambda l_type: True if l_type == MEDICINAL_TYPE else False
MEDICINAL_TYPE = "Medical"
ADULT_USE_TYPE = "Recreational"
ADULT_USE_DISPLAY = "Adult Use"
MEDICINAL_DISPLAY = MEDICINAL_TYPE

LICENSE_TYPE_MAPPING = {
    "A12": (35, ADULT_USE_TYPE, ADULT_USE_DISPLAY,
            "Recreational Microbusiness (TEMP)",
            STATE_CA,
            HAS_MEDICAL(ADULT_USE_TYPE)),

    "M11": (29, MEDICINAL_TYPE, MEDICINAL_DISPLAY,
            "Distributor (TEMP)", STATE_CA,
            HAS_MEDICAL(MEDICINAL_TYPE)),

    "A10": (32, ADULT_USE_TYPE, ADULT_USE_DISPLAY,
            "Retailer (TEMP)", STATE_CA,
            HAS_MEDICAL(ADULT_USE_TYPE)),

    "A13": (32, ADULT_USE_TYPE, ADULT_USE_DISPLAY,
            "Retailer (TEMP)", STATE_CA,
            HAS_MEDICAL(ADULT_USE_TYPE)),

    "M13": (29, MEDICINAL_TYPE, MEDICINAL_DISPLAY,
            "Distributor (TEMP)", STATE_CA,
            HAS_MEDICAL(MEDICINAL_TYPE)),

    "A11": (31, ADULT_USE_TYPE, ADULT_USE_DISPLAY,
            "Distributor (TEMP)", STATE_CA,
            HAS_MEDICAL(ADULT_USE_TYPE)),

    "A9": (36, ADULT_USE_TYPE, ADULT_USE_DISPLAY,
           "Retailer Non-Storefront (TEMP)", STATE_CA,
           HAS_MEDICAL(ADULT_USE_TYPE)),

    "M10": (30, MEDICINAL_TYPE, MEDICINAL_DISPLAY,
            "Retailer (TEMP)", STATE_CA,
            HAS_MEDICAL(MEDICINAL_TYPE)),

    "M12": (33, MEDICINAL_TYPE, MEDICINAL_DISPLAY,
            "Microbusiness (TEMP)", STATE_CA,
            HAS_MEDICAL(MEDICINAL_TYPE)),

    "M9": (34, MEDICINAL_TYPE, MEDICINAL_DISPLAY,
           "Retailer Non-Storefront", STATE_CA,
           HAS_MEDICAL(MEDICINAL_TYPE)),
}


def license_number_object(number):
    number = number.replace(" ", "").split("-")

    if len(number) < 3:
        return None

    key = number[0]
    ln = LICENSE_TYPE_MAPPING.get(key, None)

    if not ln:
        return None

    ln_id, ln_type, display_type, classification, state, has_medicinal = ln

    return {"id": ln_id,
            "type": ln_type,
            "display_type": display_type,
            "classification": classification,
            "state": state,
            "has_medical_line_items": has_medicinal}


def get_license_type(license_numbers):
    if not license_numbers:
        return None

    numbers = LICENSE_REGEX.findall(license_numbers)
    main_number = {}

    for number in numbers:
        num = license_number_object(number)
        if not num:
            continue

        if not main_number:
            main_number = dict(type=num, number=number)
            continue

        if not num["has_medical_line_items"]:
            main_number = dict(type=num, number=number)

    return main_number
