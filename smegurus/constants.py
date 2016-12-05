from django.utils.translation import ugettext_lazy as _
from smegurus.settings import env_var


# The domain of our application.
SMEGURUS_APP_HTTP_PROTOCOL = env_var('SMEGURUS_APP_HTTP_PROTOCOL')
SMEGURUS_APP_HTTP_DOMAIN = env_var('SMEGURUS_APP_HTTP_DOMAIN')


# Constants assign identification to groups.
ENTREPRENEUR_GROUP_ID = 1
MENTOR_GROUP_ID = 2
ADVISOR_GROUP_ID = 3
ORGANIZATION_MANAGER_GROUP_ID = 4
ORGANIZATION_ADMIN_GROUP_ID = 5
CLIENT_MANAGER_GROUP_ID = 6
SYSTEM_ADMIN_GROUP_ID = 7


# The official name of our specific group membership.
ENTREPRENEUR_GROUP = _("Entrepreneur")
MENTOR_GROUP = _("Mentor")
ADVISOR_GROUP = _("Advisor")
ORGANIZATION_MANAGER_GROUP = _("Organization Manager")
ORGANIZATION_ADMIN_GROUP = _("Organization Administrator")
CLIENT_MANAGER_GROUP = _("Client Manager")
SYSTEM_ADMIN_GROUP = _("System Administrator")


#==============================================================================#
#                             USER PROFILE CONSTANTS                           #
#==============================================================================#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                                  STAGE NUMBER                                *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
ME_MIN_STAGE_NUM = 0
ME_MAX_STAGE_NUM = 7
ME_ONBOARDING_STAGE_NUM = 1

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                                      GENDER                                  *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
ME_MALE_GENDER_ID = 1
ME_FEMALE_GENDER_ID = 2
ME_ANOTHER_GENDER_ID = 3
ME_OTHER_GENDER_ID = 4
ME_GENDER_OPTIONS = (
    (ME_MALE_GENDER_ID, _("Male")),
    (ME_FEMALE_GENDER_ID, _("Female")),
    (ME_ANOTHER_GENDER_ID, _("Another")),
    (ME_OTHER_GENDER_ID, _("Other")),
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                            HIGHEST LEVEL OF EDUCATION                        *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
HIGHEST_LEVEL_OF_EDUCATION_OPTIONS = (
    (1, _('Some High School')),
    (2, _('High School diploma')),
    (3, _('Some Post-Secondary')),
    (4, _('Post-Secondary diploma')),
    (5, _('Graduate degree')),
    (6, _('Professional degree')),
    (7, _('Other')),
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                                  PLACE OF BIRTH                              *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
ME_PLACE_OF_BIRTH_OPTIONS = (
    ("Canada",_("Canada")),
("United States",_ ("United States")),
("Mexico",_("Mexico")),
("Afghanistan",_("Afghanistan")),
("Aland Islands",_("Aland Islands")),
("Albania",_("Albania")),
("Algeria",_("Algeria")),
("American Samoa",_("American Samoa")),
("Andorra",_("Andorra")),
("Angola",_("Angola")),
("Anguilla",_("Anguilla")),
("Antarctica",_("Antarctica")),
("Antigua and Barbuda",_("Antigua and Barbuda")),
("Argentina",_("Argentina")),
("Armenia",_("Armenia")),
("Aruba",_("Aruba")),
("Australia",_("Australia")),
("Austria",_("Austria")),
("Azerbaijan",_("Azerbaijan")),
("Bahamas",_("Bahamas")),
("Bahrain",_("Bahrain")),
("Bangladesh",_("Bangladesh")),
("Barbados",_("Barbados")),
("Belarus",_("Belarus")),
("Belgium",_("Belgium")),
("Belize",_("Belize")),
("Benin",_("Benin")),
("Bermuda",_("Bermuda")),
("Bhutan",_("Bhutan")),
("Bolivia",_("Bolivia")),
("Bosnia and Herzegovina",_("Bosnia and Herzegovina")),
("Botswana",_("Botswana")),
("Bouvet Island",_("Bouvet Island")),
("Brazil",_("Brazil")),
("British Indian Ocean Territory",_("British Indian Ocean Territory")),
("Brunei Darussalam",_("Brunei Darussalam")),
("Bulgaria",_("Bulgaria")),
("Burkina Faso",_("Burkina Faso")),
("Burundi",_("Burundi")),
("Cambodia",_("Cambodia")),
("Cameroon",_("Cameroon")),
("Cape Verde",_("Cape Verde")),
("Cayman Islands",_("Cayman Islands")),
("Central African Republic",_("Central African Republic")),
("Chad",_("Chad")),
("Chile",_("Chile")),
("China",_("China")),
("Christmas Island",_("Christmas Island")),
("Cocos (Keeling) Islands",_("Cocos (Keeling) Islands")),
("Colombia",_("Colombia")),
("Comoros",_("Comoros")),
("Congo",_("Congo")),
("Cook Islands",_("Cook Islands")),
("Costa Rica",_("Costa Rica")),
("Cote D'Ivoire",_("Cote D'Ivoire")),
("Croatia",_("Croatia")),
("Cuba",_("Cuba")),
("Cyprus",_("Cyprus")),
("Czech Republic",_("Czech Republic")),
("Democratic Republic of the Congo",_("Democratic Republic of the Congo")),
("Denmark",_("Denmark")),
("Djibouti", _("Djibouti")),
("Dominica",_("Dominica")),
("Dominican Republic",_("Dominican Republic")),
("Ecuador",_("Ecuador")),
("Egypt",_("Egypt")),
("El Salvador",_("El Salvador")),
("Equatorial Guinea",_("Equatorial Guinea")),
("Eritrea",_("Eritrea")),
("Estonia",_("Estonia")),
("Ethiopia",_("Ethiopia")),
("Falkland Islands (Malvinas)",_("Falkland Islands (Malvinas)")),
("Faroe Islands",_("Faroe Islands")),
("Fiji",_("Fiji")),
("Finland",_("Finland")),
("France",_("France")),
("French Guiana",_("French Guiana")),
("French Polynesia",_("French Polynesia")),
("French Southern Territories",_("French Southern Territories")),
("Gabon",_("Gabon")),
("Gambia",_("Gambia")),
("Georgia",_("Georgia")),
("Germany",_("Germany")),
("Ghana",_("Ghana")),
("Gibraltar",_("Gibraltar")),
("Greece",_("Greece")),
("Greenland",_("Greenland")),
("Grenada",_("Grenada")),
("Guadeloupe",_("Guadeloupe")),
("Guam",_("Guam")),
("Guatemala",_("Guatemala")),
("Guernsey",_("Guernsey")),
("Guinea",_("Guinea")),
("Guinea-Bissau",_("Guinea-Bissau")),
("Guyana",_("Guyana")),
("Haiti",_("Haiti")),
("Heard Island and Mcdonald Islands",_("Heard Island and Mcdonald Islands")),
("Holy See (Vatican City State)",_("Holy See (Vatican City State)")),
("Honduras",_("Honduras")),
("Hong Kong",_("Hong Kong")),
("Hungary",_("Hungary")),
("Iceland",_("Iceland")),
("India",_("India")),
("Indonesia",_("Indonesia")),
("Iran",_("Iran")),
("Iraq",_("Iraq")),
("Ireland",_("Ireland")),
("Isle of Man",_("Isle of Man")),
("Israel",_("Israel")),
("Italy",_("Italy")),
("Jamaica",_("Jamaica")),
("Japan",_("Japan")),
("Jersey",_("Jersey")),
("Jordan",_("Jordan")),
("Kazakhstan",_("Kazakhstan")),
("Kenya",_("Kenya")),
("Kiribati",_("Kiribati")),
("Korea",_("Korea")),
("Korea DPR",_("Korea DPR")),
("Kuwait",_("Kuwait")),
("Kyrgyzstan",_("Kyrgyzstan")),
("Laos",_("Laos")),
("Latvia",_("Latvia")),
("Lebanon",_("Lebanon")),
("Lesotho",_("Lesotho")),
("Liberia",_("Liberia")),
("Libya",_("Libya")),
("Liechtenstein",_("Liechtenstein")),
("Lithuania",_("Lithuania")),
("Luxembourg",_("Luxembourg")),
("Macao",_("Macao")),
("Macedonia",_("Macedonia")),
("Madagascar",_("Madagascar")),
("Malawi",_("Malawi")),
("Malaysia",_("Malaysia")),
("Maldives",_("Maldives")),
("Mali",_("Mali")),
("Malta",_("Malta")),
("Marshall Islands",_("Marshall Islands")),
("Martinique",_("Martinique")),
("Mauritania",_("Mauritania")),
("Mauritius",_("Mauritius")),
("Mayotte",_("Mayotte")),
("Micronesia",_("Micronesia")),
("Moldova",_("Moldova")),
("Monaco",_("Monaco")),
("Mongolia",_("Mongolia")),
("Montenegro",_("Montenegro")),
("Montserrat",_("Montserrat")),
("Morocco",_("Morocco")),
("Mozambique",_("Mozambique")),
("Myanmar",_("Myanmar")),
("Namibia",_("Namibia")),
("Nauru",_("Nauru")),
("Nepal",_("Nepal")),
("Netherlands",_("Netherlands")),
("Netherlands Antilles",_("Netherlands Antilles")),
("New Caledonia",_("New Caledonia")),
("New Zealand",_("New Zealand")),
("Nicaragua",_("Nicaragua")),
("Niger",_("Niger")),
("Nigeria",_("Nigeria")),
("Niue",_("Niue")),
("Norfolk Island",_("Norfolk Island")),
("Northern Mariana Islands",_("Northern Mariana Islands")),
("Norway",_("Norway")),
("Oman",_("Oman")),
("Pakistan",_("Pakistan")),
("Palau",_("Palau")),
("Palestinian Territories",_("Palestinian Territories")),
("Panama",_("Panama")),
("Papua New Guinea",_("Papua New Guinea")),
("Paraguay",_("Paraguay")),
("Peru",_("Peru")),
("Philippines",_("Philippines")),
("Pitcairn",_("Pitcairn")),
("Poland",_("Poland")),
("Portugal",_("Portugal")),
("Puerto Rico",_("Puerto Rico")),
("Qatar",_("Qatar")),
("Reunion",_("Reunion")),
("Romania",_("Romania")),
("Russia",_("Russia")),
("Rwanda",_("Rwanda")),
("Saint Helena",_("Saint Helena")),
("Saint Kitts & Nevis",_("Saint Kitts & Nevis")),
("Saint Lucia",_("Saint Lucia")),
("Saint Pierre & Miquelon",_("Saint Pierre & Miquelon")),
("Saint Vincent & the Grenadines",_("Saint Vincent & the Grenadines")),
("Samoa",_("Samoa")),
("San Marino",_("San Marino")),
("Sao Tome and Principe",_("Sao Tome and Principe")),
("Saudi Arabia",_("Saudi Arabia")),
("Senegal",_("Senegal")),
("Serbia",_("Serbia")),
("Seychelles",_("Seychelles")),
("Sierra Leone",_("Sierra Leone")),
("Singapore",_("Singapore")),
("Slovakia",_("Slovakia")),
("Slovenia",_("Slovenia")),
("Solomon Islands",_("Solomon Islands")),
("Somalia",_("Somalia")),
("South Africa",_("South Africa")),
("South Georgia & the South Sandwich Islands",
("South Georgia & the South Sandwich Islands")),
("Spain",_("Spain")),
("Sri Lanka",_("Sri Lanka")),
("Sudan",_("Sudan")),
("Suriname",_("Suriname")),
("Svalbard & Jan Mayen",_("Svalbard & Jan Mayen")),
("Swaziland",_("Swaziland")),
("Sweden",_("Sweden")),
("Switzerland",_("Switzerland")),
("Syria",_("Syria")),
("Taiwan",_("Taiwan")),
("Tajikistan",_("Tajikistan")),
("Tanzania",_("Tanzania")),
("Thailand",_("Thailand")),
("Timor-Leste",_("Timor-Leste")),
("Togo",_("Togo")),
("Tokelau",_("Tokelau")),
("Tonga",_("Tonga")),
("Trinidad & Tobago",_("Trinidad & Tobago")),
("Tunisia",_("Tunisia")),
("Turkey",_("Turkey")),
("Turkmenistan",_("Turkmenistan")),
("Turks & Caicos Islands",_("Turks & Caicos Islands")),
("Tuvalu",_("Tuvalu")),
("Uganda",_("Uganda")),
("Ukraine",_("Ukraine")),
("United Arab Emirates", _("United Arab Emirates")),
("United Kingdom",_("United Kingdom")),
("United States Minor Outlying Islands",_("United States Minor Outlying Islands")),
("Uruguay",_("Uruguay")),
("Uzbekistan",_("Uzbekistan")),
("Vanuatu",_("Vanuatu")),
("Venezuela",_("Venezuela")),
("Vietnam",_("Vietnam")),
("Virgin Islands, British",_("Virgin Islands, British")),
("Virgin Islands, U.S.",_("Virgin Islands, U.S.")),
("Wallis & Futuna",_("Wallis & Futuna")),
("Western Sahara",_("Western Sahara")),
("Yemen",_("Yemen")),
("Zambia",_("Zambia")),
("Zimbabwe",_("Zimbabwe"))
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                               EMPLOYMENT STATUS                              *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
ME_EMPLOYMENT_STATUS_OPTIONS = (
    (1, _("employed full time")),
    (2, _("employed part time")),
    (3, _("underemployed")),
    (4, _("unemployed")),
    (5, _("receiving disability benefits")),
    (6, _("retired")),
    (7, _("Other")),
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                  ENROLLED IN EDUCATION OR TRAINING STATUS                    *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
ME_IN_EDUCATION_OR_TRAINING_STATUS_OPTIONS = (
    (1, _("Highschool")),
    (2, _("Post-Secondary")),
    (3, _("Private career training")),
    (4, _("Specialized employment program")),
    (5, _("Other")),
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                              WHY BE AN ENTREPRENEUR                          *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
ME_WHY_BE_ENTREPRENEUR_OPTIONS = (
    (1, _("I want to work for myself")),
    (2, _("I want to control my own schedule")),
    (3, _("I want to make more money")),
    (4, _("I want better work-life balance")),
    (5, _("I have a business idea that I want to try out")),
    (6, _("Other")),
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                    CHALLENGES IN BECOMING AN ENTREPRENEUR                    #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
ME_CHALLENGES_BECOMING_ENTREPRENEUR_OPTIONS = (
    (1, _("My health")),
    (2, _("Childcare")),
    (3, _("Transportation")),
    (4, _("Lack of Family support")),
    (5, _("Language skills")),
    (6, _("Other")),
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                            ANNUAL INCOME BRACKET                             #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
ME_ANNUAL_INCOME_BRACKET_OPTIONS = (
    (1, _("$0-$24,999")),
    (2, _("$25,000-$49,999")),
    (3, _("$50,000-$74,999")),
    (4, _("$75,000-$99,999")),
    (5, _("$100,000+")),
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
#                            ANNUAL INCOME BRACKET                             #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
ME_HAS_OWNED_BUSINESS_OPTIONS = (
    (1, _("Yes")),
    (2, _("No")),
    (3, _("Other")),
)

#==============================================================================#
#                              EMPLOYEE CONSTANTS                              #
#==============================================================================#
# Constant lists all the roles belonging to the employee system of the
# application.
EMPLOYEE_GROUPS = [
    ADVISOR_GROUP,
    ORGANIZATION_MANAGER_GROUP,
    ORGANIZATION_ADMIN_GROUP,
    CLIENT_MANAGER_GROUP,
    SYSTEM_ADMIN_GROUP
]

# This array of ID's is used for grouping all "employee" staff for our app.
EMPLOYEE_GROUP_IDS = [
    ADVISOR_GROUP_ID,
    ORGANIZATION_MANAGER_GROUP_ID,
    ORGANIZATION_ADMIN_GROUP_ID,
    CLIENT_MANAGER_GROUP_ID,
    SYSTEM_ADMIN_GROUP_ID
]

# This array of ID's is used for grouping all "management" staff for our app.
MANAGEMENT_EMPLOYEE_GROUP_IDS = [
    ORGANIZATION_MANAGER_GROUP_ID,
    ORGANIZATION_ADMIN_GROUP_ID,
    CLIENT_MANAGER_GROUP_ID,
    SYSTEM_ADMIN_GROUP_ID
]

# This array of ID's is used for grouping all "management" staff for our app.
ORG_ADMIN_GROUP_IDS = [
    ORGANIZATION_ADMIN_GROUP_ID,
    CLIENT_MANAGER_GROUP_ID,
    SYSTEM_ADMIN_GROUP_ID
]


# These constants are used for Employee-Customer reviewing process.
CREATED_STATUS = 1
PENDING_REVIEW_STATUS = 2
IN_REVIEW_STATUS = 3
REJECTED_STATUS = 4
APPROVED_STATUS = 5
SUSPENDED_STATUS = 6
EXPIRED_STATUS = 7
STATUS_OPTIONS = (
    (CREATED_STATUS, _('Created')),
    (PENDING_REVIEW_STATUS, _('Pending')),
    (IN_REVIEW_STATUS, _('In Review')),
    (REJECTED_STATUS, _('Rejected')),
    (APPROVED_STATUS, _('Approved')),
    (SUSPENDED_STATUS, _('Suspended')),
    (EXPIRED_STATUS, _('Expired')),
)


# Constants control the level of detail email notification the User will
# receive when interacted by the platform.
NO_EMAIL_FREQUENCY_STATUS = 0
ESSENTIAL_EMAIL_FREQUENCY_STATUS = 1
EXCESSIVE_EMAIL_FREQUENCY_STATUS = 3


# These constants are used for Task model.
OPEN_TASK_STATUS = 1
CLOSED_TASK_STATUS = 2
TASK_STATUS_OPTIONS = (
    (OPEN_TASK_STATUS, _('Open')),
    (CLOSED_TASK_STATUS, _('Completed')),
)


# Constants used for Tasks.
TASK_BY_CUSTOM_TYPE = 1
TASK_BY_TAG_TYPE = 2
TASK_TYPE_OPTIONS = (
    (TASK_BY_CUSTOM_TYPE, _('Task by Custom')),
    (TASK_BY_TAG_TYPE, _('Task by Tag')),
)


# Constants used for Calendar Events.
CALENDAR_EVENT_BY_CUSTOM_TYPE = 1
CALENDAR_EVENT_BY_TAG_TYPE = 2
CALENDAR_EVENT_TYPE_OPTIONS = (
    (CALENDAR_EVENT_BY_CUSTOM_TYPE, _('Calendar Event by Custom')),
    (CALENDAR_EVENT_BY_TAG_TYPE, _('Calendar Event by Tag')),
)


# Constants used for Informational Resources.
INFO_RESOURCE_CATEGORY_VIDEO_ID = 1
INFO_RESOURCE_CATEGORY_template_id = 2
INFO_RESOURCE_CATEGORY_FORM_ID = 3
INFO_RESOURCE_CATEGORY_ARTICLE_ID = 4
INFO_RESOURCE_CATEGORY_WEBLINK_ID = 5
INFO_RESOURCE_CATEGORY_LEARNING_ID = 6


INFO_RESOURCE_INTERAL_URL_TYPE = 1
INFO_RESOURCE_EXTERNAL_URL_TYPE = 2
INFO_RESOURCE_EMBEDDED_YOUTUBE_VIDEO_TYPE = 3
INFO_RESOURCE_INTERNAL_VIDEO_TYPE = 4
INFO_RESOURCE_INTERNAL_FILE_TYPE = 5
INFO_RESOURCE_TYPE_OPTIONS = (
    (INFO_RESOURCE_INTERAL_URL_TYPE, _('Internal URL')),
    (INFO_RESOURCE_EXTERNAL_URL_TYPE, _('External URL')),
    (INFO_RESOURCE_EMBEDDED_YOUTUBE_VIDEO_TYPE, _('Embedded YouTube Video')),
    (INFO_RESOURCE_INTERNAL_VIDEO_TYPE, _('Internal Video')),
    (INFO_RESOURCE_INTERNAL_FILE_TYPE, _('Internal File')),
)


# Postal Code addresses.
POSTALADDRESS_SUFFIX_OPTIONS = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    ('H', 'H'),
    ('I', 'I'),
    ('J', 'J'),
    ('K', 'K'),
    ('L', 'L'),
    ('M', 'M'),
    ('N', 'N'),
    ('O', 'O'),
    ('P', 'P'),
    ('Q', 'Q'),
    ('R', 'R'),
    ('S', 'S'),
    ('T', 'T'),
    ('U', 'U'),
    ('V', 'V'),
    ('W', 'W'),
    ('X', 'X'),
    ('Y', 'Y'),
    ('Z', 'Z'),
    ('¼', '¼'),
    ('½', '½'),
    ('¾', '¾'),
)

POSTALADDRESS_STREET_TYPE_OPTIONS = (
    ('ABBEY', _('Abbey')),
    ('ACRES', _('Acres')),
    ('ALLEE', _('Allée')),
    ('ALLEY', _('Alley')),
    ('AUT', _('Autoroute')),
    ('AVE', _('Avenue (E)')),
    ('AV', _('avenue (F)')),
    ('BAY', _('Bay')),
    ('BEACH', _('Beach')),
    ('BEND', _('Bend')),
    ('BLVD', _('Boulevard (E)')),
    ('BOUL', _('Boulevard (F)')),
    ('BR', _('Branch')),
    ('BYPASS', _('By-pass')),
    ('CAMPUS', _('Campus')),
    ('CAPE', _('Cape')),
    ('CAR', _('Carré')),
    ('CARREF', _('Carrefour')),
    ('CTR', _('Centre (E)')),
    ('C', _('Centre (F)')),
    ('CERCLE', _('Cercle')),
    ('CHASE', _('Chase')),
    ('CH', _('Chemin')),
    ('CIR', _('Circle')),
    ('CIRCT', _('Circuit')),
    ('CLOSE', _('Close')),
    ('COMMON', _('Common')),
    ('CONC', _('Concession')),
    ('CRNRS', _('Corners')),
    ('COTE', _('Côte')),
    ('COUR', _('Cour')),
    ('COURS', _('Cours')),
    ('CRT', _('Court')),
    ('COVE', _('Cove')),
    ('CRES', _('Crescent')),
    ('CREST', _('Crest')),
    ('CROIS', _('Croissant')),
    ('CROSS', _('Crossing')),
    ('CDS', _('Cul-de-sac')),
    ('DALE', _('Dale')),
    ('DELL', _('Dell')),
    ('DIVERS', _('Diversion')),
    ('DOWNS', _('Downs')),
    ('DR', _('Drive')),
    ('END', _('End')),
    ('ESPL', _('Esplanade')),
    ('ESTATE', _('Estates')),
    ('EXPY', _('Expressway')),
    ('EXTEN', _('Extension')),
    ('FIELD', _('Field')),
    ('FOREST', _('Forest')),
    ('FWY', _('Freeway')),
    ('GDNS', _('Gardens')),
    ('GATE', _('Gate')),
    ('GLADE', _('Glade')),
    ('GLEN', _('Glen')),
    ('GREEN', _('Green')),
    ('GRNDS', _('Grounds')),
    ('GROVE', _('Grove')),
    ('HARBR', _('Harbour')),
    ('HEATH', _('Heath')),
    ('HEIGHT', _('Height')),
    ('HTS', _('Heights')),
    ('HGHLDS', _('Highlands')),
    ('HWY', _('Highway')),
    ('HILL', _('Hill')),
    ('HOLLOW', _('Hollow')),
    ('ILE', _('Île')),
    ('IMP', _('Impasse')),
    ('INLET', _('Inlet')),
    ('ISLAND', _('Island')),
    ('KEY', _('Key')),
    ('KNOLL', _('Knoll')),
    ('LANDNG', _('Landing')),
    ('LANE', _('Lane')),
    ('LMTS', _('Limits')),
    ('LINE', _('Line')),
    ('LINK', _('Link')),
    ('LKOUT', _('Lookout')),
    ('LOOP', _('Loop')),
    ('MALL', _('Mall')),
    ('MANOR', _('Manor')),
    ('MAZE', _('Maze')),
    ('MEADOW', _('Meadow')),
    ('MEWS', _('Mews')),
    ('MONTEE', _('Montéé')),
    ('MOUNT', _('Mount')),
    ('MTN', _('Mountain')),
    ('PARADE', _('Parade')),
    ('PARC', _('Parc')),
    ('PK', _('Park')),
    ('PKY', _('Parkway')),
    ('PASS', _('Passage')),
    ('PATH', _('Path')),
    ('PTWAY', _('Pathway')),
    ('PINES', _('Pines')),
    ('PL', _('Place (E)')),
    ('PLACE', _('Place (F)')),
    ('PLAT', _('Plateau')),
    ('PLAZA', _('Plaza')),
    ('PT', _('Point')),
    ('POINTE', _('Pointe')),
    ('PORT', _('Port')),
    ('PVT', _('Private')),
    ('PROM', _('Promenade')),
    ('QUAI', _('Quai')),
    ('QUAY', _('Quay')),
    ('RAMP', _('Ramp')),
    ('RANG', _('Rang')),
    ('RIDGE', _('Ridge')),
    ('RISE', _('Rise')),
    ('RD', _('Road')),
    ('RTE', _('Route')),
    ('ROW', _('Row')),
    ('RUE', _('Rue')),
    ('RLE', _('Ruelle')),
    ('RUN', _('Run')),
    ('SENT', _('Sentier')),
    ('SQ', _('Square')),
    ('ST', _('Street')),
    ('SUBDIV', _('Subdivision')),
    ('TERR', _('Terrace')),
    ('TSSE', _('Terrasse')),
    ('TLINE', _('Townline')),
    ('TRAIL', _('Trail')),
    ('TRNABT', _('Turnabout')),
    ('VALE', _('Vale')),
    ('VIEW', _('View')),
    ('VILLGE', _('Village')),
    ('VILLAS', _('Villas')),
    ('VISTA', _('Vista')),
    ('VOIE', _('Voie')),
    ('WALK', _('Walk')),
    ('WAY', _('Way')),
    ('WHARF', _('Wharf')),
    ('WOOD', _('Wood')),
    ('WYND', _('Wynd')),
)


POSTALADDRESS_DIRECTION_OPTIONS = (
    ('E', 'E'),
    ('N', 'N'),
    ('NE', 'NE'),
    ('NO', 'NO'),
    ('NW', 'NW'),
    ('O', 'O'),
    ('S', 'S'),
    ('SE', 'SE'),
    ('SO', 'SO'),
    ('SW', 'SW'),
    ('W', 'W'),
)


# DOCUMENT STATUS TYPES ID
DOCUMENT_CREATED_STATUS = 1
DOCUMENT_PENDING_REVIEW_STATUS = 2
DOCUMENT_READY_STATUS = 3

# DOCUMENT STATUS TYPE TEXT
DOCUMENT_CREATED_STATUS_TEXT = _('Created Status')
DOCUMENT_PENDING_REVIEW_STATUS_TEXT = _('Pending Review Status')
DOCUMENT_READY_STATUS_TEXT  = _('Ready Status')

# DOCUMENT STATUS OPTIONS
DOCUMENT_STATUS_OPTIONS = (
    (DOCUMENT_CREATED_STATUS, DOCUMENT_CREATED_STATUS_TEXT),
    (DOCUMENT_PENDING_REVIEW_STATUS, DOCUMENT_PENDING_REVIEW_STATUS_TEXT),
    (DOCUMENT_READY_STATUS, DOCUMENT_READY_STATUS_TEXT)
)
