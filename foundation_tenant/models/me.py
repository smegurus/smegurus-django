from foundation_tenant.models.abstract_person import AbstractPerson


class Me(AbstractPerson):
    """
    The object that represents the entreprenuer. 
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_mes'

    def __str__(self):
        return str(self.name)
