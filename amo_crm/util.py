import json
import requests


def get_pipelines(subdomain, access_token, pipeline_id=None):
    url = 'https://{}.amocrm.ru/api/v4/leads/pipelines/'.format(subdomain)
    if pipeline_id: url += str(pipeline_id)
    return requests.get(url, headers={'Authorization': 'Bearer ' + str(access_token)})


def get_statuses(subdomain, access_token, pipeline_id):
    return requests.get('https://{}.amocrm.ru/api/v4/leads/pipelines/{}/statuses'.format(subdomain, pipeline_id),
                        headers={'Authorization': 'Bearer ' + str(access_token)})


def get_lead(subdomain, access_token, lead_id=None):
    url = 'https://{}.amocrm.ru/api/v4/leads/'.format(subdomain)
    if lead_id: url += str(lead_id)
    return requests.get(url, headers={'Authorization': 'Bearer ' + str(access_token)})


def add_lead(subdomain, access_token, name, price, status_id, pipeline_id, created_at, updated_at, closed_at,
             loss_reason_id, responsible_user_id, custom_fields, tags, contacts, companies):
    add_obj = {}
    # Формирование словаря сделки
    if name: add_obj.update({'name': name})
    if price: add_obj.update({'sale': price})
    if status_id: add_obj.update({'status_id': status_id})
    if pipeline_id: add_obj.update({'pipeline_id': pipeline_id})
    if created_at: add_obj.update({'created_at': created_at})
    if updated_at: add_obj.update({'updated_at': updated_at})
    if closed_at: add_obj.update({'closed_at': closed_at})
    if loss_reason_id: add_obj.update({'loss_reason_id': loss_reason_id})
    if responsible_user_id: add_obj.update({'responsible_user_id': responsible_user_id})

    if custom_fields: add_obj.update({"custom_fields_values": custom_fields})

    if tags: add_obj.update({"_embedded": {"tags": tags}})
    if contacts: add_obj.update({"_embedded": {"contacts": contacts}})
    if companies: add_obj.update({"_embedded": {"companies": companies}})

    return requests.post('https://{}.amocrm.ru/api/v4/leads'.format(subdomain),
                         headers={'Authorization': 'Bearer ' + str(access_token)},
                         data=json.dumps([add_obj]))


def update_lead(subdomain, access_token, lead_id, name, price, status_id, pipeline_id,
                created_by, updated_by, created_at, updated_at, closed_at,
                loss_reason_id, responsible_user_id, custom_fields, tags):
    update_obj = {}
    if name: update_obj.update({'name': name})
    if price: update_obj.update({'sale': price})
    if status_id: update_obj.update({'status_id': status_id})
    if pipeline_id: update_obj.update({'pipeline_id': pipeline_id})
    if created_by or created_by == 0: update_obj.update({'created_by': created_at})
    if updated_by or updated_by == 0: update_obj.update({'updated_by': created_at})
    if created_at: update_obj.update({'created_at': created_at})
    if updated_at: update_obj.update({'updated_at': updated_at})
    if closed_at: update_obj.update({'closed_at': closed_at})
    if loss_reason_id: update_obj.update({'loss_reason_id': loss_reason_id})
    if responsible_user_id: update_obj.update({'responsible_user_id': responsible_user_id})
    if custom_fields: update_obj.update({"custom_fields_values": custom_fields})

    if tags: update_obj.update({"_embedded": {"tags": tags}})

    return requests.patch('https://{}.amocrm.ru/api/v4/leads/{}'.format(subdomain, lead_id),
                          headers={'Authorization': 'Bearer ' + str(access_token)},
                          data=json.dumps([update_obj]))


def add_note(subdomain, access_token, entity_type, entity_id, note_obj):
    return requests.post('https://{}.amocrm.ru/api/v4/{}/{}/notes'.format(subdomain, entity_type, entity_id),
                         headers={'Authorization': 'Bearer ' + str(access_token)},
                         data=json.dumps(note_obj))
