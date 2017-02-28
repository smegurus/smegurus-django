from django.contrib import admin
from foundation_tenant.models.base.fileupload import FileUpload
from foundation_tenant.models.base.imageupload import ImageUpload
from foundation_tenant.models.base.s3file import S3File
from foundation_tenant.models.base.governmentbenefitoption import GovernmentBenefitOption
from foundation_tenant.models.base.identifyoption import IdentifyOption
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.models.base.language import Language
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.openinghoursspecification import OpeningHoursSpecification
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.base.geocoordinate import GeoCoordinate
from foundation_tenant.models.base.country import Country
from foundation_tenant.models.base.brand import Brand
from foundation_tenant.models.base.place import Place
from foundation_tenant.models.base.abstract_person import AbstractPerson
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.businessidea import BusinessIdea
from foundation_tenant.models.base.tellusyourneed import TellUsYourNeed
from foundation_tenant.models.base.calendarevent import CalendarEvent, SortedCalendarEventByCreated
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.admission import Admission
from foundation_tenant.models.base.faqitem import FAQItem
from foundation_tenant.models.base.faqgroup import FAQGroup
from foundation_tenant.models.base.communitypost import CommunityPost
from foundation_tenant.models.base.communityadvertisement import CommunityAdvertisement
from foundation_tenant.models.base.message import Message
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.note import Note
from foundation_tenant.models.base.logevent import SortedLogEventByCreated
from foundation_tenant.models.base.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.base.task import Task
from foundation_tenant.models.base.visitor import Visitor
from foundation_tenant.models.base.visitor import SortedVisitorsByLatestCreation
from foundation_tenant.models.base.inforesourcecategory import InfoResourceCategory
from foundation_tenant.models.base.inforesource import InfoResource
from foundation_tenant.models.base.notification import Notification
from foundation_tenant.models.bizmula.documenttype import DocumentType
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer

admin.site.register(FileUpload)
admin.site.register(ImageUpload)
admin.site.register(S3File)
admin.site.register(GovernmentBenefitOption)
admin.site.register(IdentifyOption)
admin.site.register(CountryOption)
admin.site.register(ProvinceOption)
admin.site.register(CityOption)
admin.site.register(NAICSOption)
admin.site.register(Language)
admin.site.register(PostalAddress)
admin.site.register(OpeningHoursSpecification)
admin.site.register(ContactPoint)
admin.site.register(GeoCoordinate)
admin.site.register(Country)
admin.site.register(Brand)
admin.site.register(Tag)
admin.site.register(BusinessIdea)
admin.site.register(TellUsYourNeed)
admin.site.register(CalendarEvent)
admin.site.register(Intake)
admin.site.register(Admission)
admin.site.register(FAQItem)
admin.site.register(FAQGroup)
admin.site.register(CommunityPost)
admin.site.register(CommunityAdvertisement)
admin.site.register(Message)
admin.site.register(Me)
admin.site.register(Note)
admin.site.register(SortedLogEventByCreated)
admin.site.register(SortedCommentPostByCreated)
admin.site.register(Task)
admin.site.register(SortedVisitorsByLatestCreation)
admin.site.register(InfoResourceCategory)
admin.site.register(InfoResource)
admin.site.register(Notification)
admin.site.register(DocumentType)
admin.site.register(Question)
admin.site.register(Workspace)
admin.site.register(Document)
admin.site.register(Module)
admin.site.register(Slide)
admin.site.register(QuestionAnswer)
