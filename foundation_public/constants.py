from django.utils.translation import ugettext_lazy as _

HOW_DISCOVERED_OPTIONS = (
    ("Google search", _("Google search")),
    ("SMEgurus.com", _("SMEgurus.com")),
    ("Social media", _("Social media")),
    ("Other", _("Other")),
)

HOW_MANY_SERVED_OPTIONS = (
    (1, _('1-10')),
    (2, _('11-50')),
    (3, _('50+')),
)

QUESTION_CATEGORY_OPTIONS = (
    (1, _('Pre-Intake Registration')),
    (2, _('Intake Registration')),
    #(3, _('All-or-None')),
)

QUESTION_TYPE_OPTIONS = (
    (1, _('Open Question')),
    (2, _('Open Closed Question - Value')),
    (2, _('Open Closed Question - Radio')),
    (2, _('Open Closed Question - Checkbox')),
    (2, _('Closed Question - Value')),
    (2, _('Closed Question - Radio')),
    (2, _('Closed Question - Checkbox')),
)

# Constants assign identification to groups.
ENTREPRENEUR_GROUP_ID = 1
MENTOR_GROUP_ID = 2
ADVISOR_GROUP_ID = 3
ORGANIZATION_MANAGER_GROUP_ID = 4
ORGANIZATION_ADMIN_GROUP_ID = 5
CLIENT_MANAGER_GROUP_ID = 6
SYSTEM_ADMIN_GROUP_ID = 7

ENTREPRENEUR_GROUP = _("Entrepreneur")
MENTOR_GROUP = _("Mentor")
ADVISOR_GROUP = _("Advisor")
ORGANIZATION_MANAGER_GROUP = _("Organization Manager")
ORGANIZATION_ADMIN_GROUP = _("Organization Administrator")
CLIENT_MANAGER_GROUP = _("Client Manager")
SYSTEM_ADMIN_GROUP = _("System Administrator")

# Constant lists all the roles belonging to the employee system of the
# application.
EMPLOYEE_GROUPS = [
    ADVISOR_GROUP,
    ORGANIZATION_MANAGER_GROUP,
    ORGANIZATION_ADMIN_GROUP,
    CLIENT_MANAGER_GROUP,
    SYSTEM_ADMIN_GROUP
]

EMPLOYEE_GROUP_IDS = [
    ADVISOR_GROUP_ID,
    ORGANIZATION_MANAGER_GROUP_ID,
    ORGANIZATION_ADMIN_GROUP_ID,
    CLIENT_MANAGER_GROUP_ID,
    SYSTEM_ADMIN_GROUP_ID
]

MANAGEMENT_EMPLOYEE_GROUP_IDS = [
    ORGANIZATION_MANAGER_GROUP_ID,
    ORGANIZATION_ADMIN_GROUP_ID,
    CLIENT_MANAGER_GROUP_ID,
    SYSTEM_ADMIN_GROUP_ID
]

TRADITIONAL_LEARNING_PREFERENCE = 1
BLENDED_LEARNING_PREFERENCE = 2
LEARNING_PREFERENCE_OPTIONS = (
    (TRADITIONAL_LEARNING_PREFERENCE, _('Traditional Learning Preference')),
    (BLENDED_LEARNING_PREFERENCE, _('Blended Learning Preference')),
)


TRADITIONAL_CHALLENGE = 1
REAL_WORLD_CHALLENGE = 2
CHALLENGE_OPTIONS = (
    (TRADITIONAL_CHALLENGE, _('Traditional Challenge')),
    (REAL_WORLD_CHALLENGE, _('Real World Challenge')),
)


CA_ADDRESS_REGIONS = [
    _('Ontario'),
    _('Quebec'),
    _('British Columbia'),
    _('Alberta'),
    _('Manitoba'),
    _('Saskatchewan'),
    _('Nova Scotia'),
    _('New Brunswick'),
    _('Newfoundland and Labrador'),
    _('Prince Edward Island'),
    _('Northwest Territories'),
    _('Yukon'),
    _('Nunavut'),
]

US_ADDRESS_REGIONS = [
    _('Alabama'),
    _('Alaska'),
    _('Arizona'),
    _('Arkansas'),
    _('California'),
    _('Colorado'),
    _('Connecticut'),
    _('Delaware'),
    _('Florida'),
    _('Georgia'),
    _('Hawaii'),
    _('Idaho'),
    _('Illinois Indiana'),
    _('Iowa'),
    _('Kansas'),
    _('Kentucky'),
    _('Louisiana'),
    _('Maine'),
    _('Maryland'),
    _('Massachusetts'),
    _('Michigan'),
    _('Minnesota'),
    _('Mississippi'),
    _('Missouri'),
    _('Montana Nebraska'),
    _('Nevada'),
    _('New Hampshire'),
    _('New Jersey'),
    _('New Mexico'),
    _('New York'),
    _('North Carolina'),
    _('North Dakota'),
    _('Ohio'),
    _('Oklahoma'),
    _('Oregon'),
    _('Pennsylvania Rhode Island'),
    _('South Carolina'),
    _('South Dakota'),
    _('Tennessee'),
    _('Texas'),
    _('Utah'),
    _('Vermont'),
    _('Virginia'),
    _('Washington'),
    _('West Virginia'),
    _('Wisconsin'),
    _('Wyoming'),
]


MX_ADDRESS_REGIONS = [
    _('Mexico City'),
    _('Chihuahua'),
    _('Sonora'),
    _('Coahuila'),
    _('Durango'),
    _('Oaxaca'),
    _('Tamaulipas'),
    _('Jalisco'),
    _('Zacatecas'),
    _('Baja California Sur'),
    _('Chiapas'),
    _('Veracruz'),
    _('Baja California'),
    _('Nuevo León'),
    _('Guerrero'),
    _('San Luis Potosí'),
    _('Michoacán'),
    _('Campeche'),
    _('Sinaloa'),
    _('Quintana Roo'),
    _('Yucatán'),
    _('Puebla'),
    _('Guanajuato'),
    _('Nayarit'),
    _('Tabasco'),
    _('México'),
    _('Hidalgo'),
    _('Querétaro'),
    _('Colima'),
    _('Aguascalientes'),
    _('Morelos'),
    _('Tlaxcala')
]

CN_ADDRESS_REGIONS = [
    _('Alabama'),
    _('Anhui'),
    _('Fujian'),
    _('Gansu'),
    _('Guangdong'),
    _('Guizhou'),
    _('Hainan'),
    _('Hebei'),
    _('Heilongjiang'),
    _('Henan'),
    _('Hubei'),
    _('Hunan'),
    _('Jiangsu'),
    _('Jiangxi'),
    _('Jilin'),
    _('Liaoning'),
    _('Qinghai'),
    _('Shaanxi'),
    _('Shandong'),
    _('Shanxi'),
    _('Sichuan'),
    _('Yunnan'),
    _('Zhejiang'),
    _('Guangxi Zhuang'),
    _('Inner Mongolia'),
    _('Ningxia Hui'),
    _('Xinjiang Uighur'),
    _('Tibet'),
    _('Hong Kong'),
    _('Macau'),
    _('Wolong'),
]

BR_ADDRESS_REGIONS = [
    _('Acre'),
    _('Alagoas'),
    _('Amapá'),
    _('Amazonas'),
    _('Bahia'),
    _('Ceará'),
    _('Distrito Federal'),
    _('Espírito Santo'),
    _('Goiás'),
    _('Maranhão'),
    _('MatoGrosso'),
    _('MatoGrosso do Sul'),
    _('Minas Gerais'),
    _('Pará'),
    _('Paraíba'),
    _('Paraná'),
    _('Pernambuco'),
    _('Piauí'),
    _('Rio de Janeiro'),
    _('Rio Grande do Norte'),
    _('Rio Grande do Sul'),
    _('Rondônia'),
    _('Roraima'),
    _('Santa Catarina'),
    _('São Paulo'),
    _('Sergipe'),
    _('Tocantins'),
]
