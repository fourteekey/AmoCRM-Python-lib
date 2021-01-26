import util
from datetime import datetime

from global_functions import validate_lead_data, format_custom_field, format_tags, format_to_key, validate_lead_note


class AmoCRM:
    def __init__(self, subdomain):
        self.subdomain = subdomain

    def get_pipelines(self, access_token: str, pipeline_id: int = None):
        if not isinstance(access_token, str): raise TypeError('Error "access_token" must be <str>')

        return util.get_pipelines(self.subdomain, access_token, pipeline_id)

    def get_statuses(self, access_token: str, pipeline_id):
        if not isinstance(access_token, str): raise TypeError('Error "access_token" must be <str>')

        return util.get_statuses(self.subdomain, access_token, pipeline_id)

    def get_all_leads(self, access_token: str):
        if not isinstance(access_token, str): raise TypeError('Error "access_token" must be <str>')

        return util.get_lead(self.subdomain, access_token)

    def get_lead(self, access_token: str, lead_id):
        if not isinstance(access_token, str): raise TypeError('Error "access_token" must be <str>')

        return util.get_lead(self.subdomain, access_token, lead_id)

    def add_lead(self, access_token: str,
                 name: str = None, price: int = None, status_id: int = None, pipeline_id: int = None,
                 created_at: int = None, updated_at: int = None, closed_at: int = None,
                 loss_reason_id: int = None, responsible_user_id: int = None,
                 custom_fields: dict = None, tags: list = None, contacts: dict = None, companies=None):
        """
        Создание новой карточки в AmoСRM.
        """

        # Валидация входных данных.
        validate_lead_data(access_token=access_token, name=name, price=price, status_id=status_id,
                           pipeline_id=pipeline_id,
                           created_at=created_at, updated_at=updated_at, closed_at=closed_at,
                           loss_reason_id=loss_reason_id, responsible_user_id=responsible_user_id,
                           custom_fields=custom_fields, tags=tags, contacts=contacts, companies=companies)

        # Приводим данные к формату для AMO
        if custom_fields: custom_fields = format_custom_field(custom_fields)
        if tags: tags = format_tags(tags)
        if contacts: tags = format_to_key(contacts)
        if companies: companies = format_to_key(companies)

        return util.add_lead(self.subdomain, access_token=access_token,
                             name=name, price=price, status_id=status_id, pipeline_id=pipeline_id,
                             created_at=created_at, updated_at=updated_at, closed_at=closed_at,
                             loss_reason_id=loss_reason_id, responsible_user_id=responsible_user_id,
                             custom_fields=custom_fields, tags=tags, contacts=contacts, companies=companies)

    def update_lead(self, access_token: str, lead_id,
                    name: str = None, price: int = None, status_id: int = None, pipeline_id: int = None,
                    created_by: int = 0, updated_by: int = 0,
                    created_at: int = None, updated_at: int = None, closed_at: int = None,
                    loss_reason_id: int = None, responsible_user_id: int = None,
                    custom_fields: dict = None, tags: list = None):

        # Валидация входных данных.
        validate_lead_data(access_token=access_token, name=name, price=price, status_id=status_id,
                           pipeline_id=pipeline_id,
                           created_by=created_by, updated_by=updated_by,
                           created_at=created_at, updated_at=updated_at, closed_at=closed_at,
                           loss_reason_id=loss_reason_id, responsible_user_id=responsible_user_id,
                           custom_fields=custom_fields, tags=tags)

        # Приводим данные к формату для AMO
        if custom_fields: custom_fields = format_custom_field(custom_fields)
        if tags: tags = format_tags(tags)

        if not updated_at: updated_at = datetime.now().strftime('%s')

        return util.update_lead(self.subdomain, access_token=access_token, lead_id=lead_id,
                                name=name, price=price, status_id=status_id, pipeline_id=pipeline_id,
                                created_by=created_by, updated_by=updated_by, created_at=created_at,
                                updated_at=updated_at, closed_at=closed_at, loss_reason_id=loss_reason_id,
                                responsible_user_id=responsible_user_id, custom_fields=custom_fields, tags=tags, )

    def add_note(self, access_token, entity_type, entity_id: int, note_type: str, params: dict, created_by: int = 0,
                 request_id: int = None):
        """
        note_type: https://www.amocrm.ru/developers/content/crm_platform/events-and-notes#notes-types
        """

        # TODO: Возможно добавить другие типы
        if entity_type not in ('leads',):
            raise ValueError('Entity type must be leads')

        note_obj = validate_lead_note(note_type, params)
        note_obj.update({'created_by': created_by})
        if request_id:
            note_obj.update({'request_id': request_id})

        return util.add_note(self.subdomain, access_token=access_token, entity_type=entity_type, entity_id=entity_id,
                             note_obj=note_obj)
