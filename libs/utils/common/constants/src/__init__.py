from datetime import date
from pathlib import Path

from libs.utils.config.src.fastapi import FRONTEND_APP_URL

CHILD_SUPPORT_PAYER_WALLET_NAME = "Child Support Wallet - Payer"
CHILD_SUPPORT_RECIPIENT_WALLET_NAME = "Child Support Wallet - Recipient"
FUZZY_SEARCH_TOP_N = 10

FRONTEND_SIGNUP_URL = f"{FRONTEND_APP_URL}/signup/user"
FRONTEND_FORGET_PASSWORD_URL = f"{FRONTEND_APP_URL}/forgot-password"

FRONTEND_FORGET_PASSWORD_TEMPLATE = Path("templates/forget_password.html")
FRONTEND_INVITE_EXTERNAL_USER_TEMPLATE = Path("templates/invite_external_user.html")
FRONTEND_FUND_INVITE_TEMPLATE = Path("templates/fund_invite.html")
FRONTEND_FUND_DISBURSEMENT_TEMPLATE = Path("templates/fund_disbursement.html")
FRONTEND_FUND_STATUS_UPDATE_TEMPLATE = Path("templates/fund_status_update.html")
LOGO_URL = f"{FRONTEND_APP_URL}/logo/002-B.png"

RULE_DEFINITIONS = [
    {
        "name": "Grocery",
        "description": "Default grocery spending rule.",
        "mccs": [5411, 5499, 5422, 5451, 5441, 5462],
    },
    {
        "name": "Restaurants & Food",
        "description": "Default restaurant and food spending rule.",
        "mccs": [5812, 5814, 5811],
    },
    {
        "name": "Gas & Fuel",
        "description": "Default gas and fuel spending rule.",
        "mccs": [5541, 5542, 5983],
    },
    {
        "name": "Pharmacy & Medical",
        "description": "Default pharmacy and medical spending rule.",
        "mccs": [5912, 8011, 8021, 8041, 8042, 8043, 8049, 8062, 8099, 8071],
    },
    {
        "name": "Travel",
        "description": "Default travel spending rule.",
        "mccs": [
            4511,
            4582,
            7011,
            7012,
            4411,
            4722,
            7512,
            7519,
            4111,
            4121,
            4131,
            4112,
        ],
    },
    {
        "name": "Shopping / Retail",
        "description": "Default shopping and retail spending rule.",
        "mccs": [5311, 5310, 5331, 5399, 5300, 5999],
    },
]

DEFAULT_DATE_OF_BIRTH = date(1970, 1, 1)
DEFAULT_COUNTRY_CODE = "+1"
DEFAULT_PHONE_NUMBER = "0000000000"
DEFAULT_ADDRESS = "USA"
DEFAULT_POSTAL_CODE = "00000"

CHILD_SUPPORT_RULE_NAME = "Child Support Rule"
CHILD_SUPPORT_RULE_DESCRIPTION = (
    "Rule to block the child support wallets in unauthorized sites."
)
CHILD_SUPPORT_MCCS = [4215, 5813, 5993, 7273, 7801, 7932, 7995]
