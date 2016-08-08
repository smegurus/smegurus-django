from django.utils.translation import ugettext_lazy as _


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


# These constants are used for Employee-Customer reviewing process.
CREATED_STATUS = 1
PENDING_REVIEW_STATUS = 2
IN_REVIEW_STATUS = 3
REJECTED_STATUS = 4
APPROVED_STATUS = 5


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


RU_ADDRESS_REGIONS = [
    _('Tverskaya Oblast'),
    _('Smolenskaya Oblast'),
    _('Kirovskaya Oblast'),
    _('Arkhangelskaya Oblast'),
    _('Moskovskaya Oblast'),
    _('Perm Krai'),
    _('Krasnoyarskiy Kray'),
    _('Novgorodskaya Oblast'),
    _('Respublika Bashkortostan'),
    _('Khabarovskiy Kray'),
    _('Leningradskaya Oblast'),
    _('Pskovskaya Oblast'),
    _('Respublika Kareliya'),
    _('Sverdlovskaya Oblast'),
    _('Krasnodarskiy Kray'),
    _('Vologodskaya Oblast'),
    _('Respublika Sakha'),
    _('Yakutiya'),
    _('Respublika Dagestan'),
    _('Yaroslavskaya Oblast'),
    _('Novosibirskaya Oblast'),
    _('Rostovskaya Oblast'),
    _('Primorskiy Kray'),
    _('Kaluzhskaya Oblast'),
    _('Nizhegorodskaya Oblast'),
    _('Altayskiy Kray'),
    _('Kurganskaya Oblast'),
    _('Ivanovskaya Oblast'),
    _('Irkutskaya Oblast'),
    _('Bryanskaya Oblast'),
    _('Orlovskaya Oblast'),
    _('Kostromskaya Oblast'),
    _('Tulskaya Oblast'),
    _('Chelyabinskaya Oblast'),
    _('Volgogradskaya Oblast'),
    _('Sakhalinskaya Oblast'),
    _('Orenburgskaya Oblast'),
    _('Saratovskaya Oblast'),
    _('Kamtchatski Kray'),
    _('Omskaya Oblast'),
    _('Voronezhskaya Oblast'),
    _('Respublika Tatarstan'),
    _('Vladimirskaya Oblast'),
    _('Murmanskaya Oblast'),
    _('Ryazanskaya Oblast'),
    _('Kurskaya Oblast'),
    _('Amurskaya Oblast'),
    _('Kaliningradskaya Oblast'),
    _('Respublika Buryatiya'),
    _('Respublika Komi'),
    _('Tambovskaya Oblast'),
    _('Udmurtskaya Respublika'),
    _('Tomskaya Oblast'),
    _('Belgorodskaya Oblast'),
    _('Stavropolskiy Kray'),
    _('Magadanskaya Oblast'),
    _('Zabaikalski Kray'),
    _('Yamalo Nenetskiy Avtonomnyy Okrug'),
    _('Kemerovskaya Oblast'),
    _('Astrakhanskaya Oblast'),
    _('Lipetskaya Oblast'),
    _('Penzenskaya Oblast'),
    _('Chukotskiy Avtonomnyy Okrug'),
    _('Nenetskiy Avtonomnyy Okrug'),
    _('Chuvashskaya Respublika'),
    _('Respublika Mariy El'),
    _('Khanty-Mansiyskiy Avtonomnyy Okrug'),
    _('Samarskaya Oblast'),
    _('Tyumenskaya Oblast'),
    _('Respublika Mordoviya'),
    _('Respublika Altay'),
    _('Respublika Kalmykiya'),
    _('Ulyanovskaya Oblast'),
    _('Kabardino Balkarskaya Respublika'),
    _('Respublika Khakasiya'),
    _('Karachayevo Cherkesskaya Respublika'),
    _('Respublika Tyva'),
    _('Respublika Severnaya Osetiya Alaniya'),
    _('Respublika Adygeya'),
    _('Moskva'),
    _('Yevreyskaya Avtonomnaya Oblast'),
    _('Sankt Peterburg'),
    _('Respublika Ingushetiya'),
    _('Chechenskaya Respublika'),
]
