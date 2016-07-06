from foundation_public.models.abstract_person import AbstractPlacePerson


class PublicMe(AbstractPlacePerson):
    """
    The object that represents the entreprenuer.
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'biz_mes'

    def __str__(self):
        return str(self.name)
