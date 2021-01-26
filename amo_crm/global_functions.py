def validate_lead_data(access_token, name=None, price=None, status_id=None, pipeline_id=None,
                       created_by=None, updated_by=None, created_at=None, updated_at=None, closed_at=None,
                       loss_reason_id=None, responsible_user_id=None,
                       custom_fields=None, tags=None, contacts=None, companies=None):
    if not isinstance(access_token, str): raise TypeError('Error "access_token" must be <str>')
    if name and not isinstance(name, str): raise TypeError('TypeError "name" must be <str>')
    if price and not isinstance(price, int): raise TypeError('TypeError "price" must be <int>')
    if status_id and not isinstance(status_id, int): raise TypeError('TypeError "status_id" must be <int>')
    if pipeline_id and not isinstance(pipeline_id, int): raise TypeError('TypeError "pipeline_id" must be <int>')
    if created_by and not isinstance(created_by, int): raise TypeError('TypeError "created_by" must be <int>')
    if updated_by and not isinstance(updated_by, int): raise TypeError('TypeError "updated_by" must be <int>')

    if created_at and not isinstance(created_at, int): raise TypeError('TypeError "created_at" must be <int>')
    if updated_at and not isinstance(updated_at, int): raise TypeError('TypeError "updated_at" must be <int>')
    if closed_at and not isinstance(closed_at, int): raise TypeError('TypeError "closed_at" must be <int>')
    if loss_reason_id and not isinstance(loss_reason_id, int):
        raise TypeError('TypeError "loss_reason_id" must be <int>')
    if responsible_user_id and not isinstance(responsible_user_id, int):
        raise TypeError('TypeError "responsible_user_id" must be <int>')
    if custom_fields and not isinstance(custom_fields, list):
        raise TypeError('TypeError "custom_fields" must be <list>')
    if tags and not isinstance(tags, list):
        raise TypeError('TypeError "tags" must be <list>')
    if contacts and not isinstance(contacts, list):
        raise TypeError('TypeError "contacts" must be <list>')
    if companies and not isinstance(companies, list):
        raise TypeError('TypeError "custom_fields" must be <list>')


def format_custom_field(custom_fields):
    """
    Приводим данные к формату для AmoCRM
    """
    data = []
    for custom_field in custom_fields:
        field_id = custom_field.get('field_id', None)
        value = custom_field.get('value', None)
        # Валидируем словари
        if not field_id or not value:
            return KeyError('KeyError invalid data in custom fields.\n'
                            'Example {"field_id": 1, "value": "test value"}')
        elif isinstance(field_id, int):
            raise TypeError('TypeError "field_id" must be <int>')
        else:
            data.append({"field_id": field_id, "values": [{"value": str(value)}]})
    return data


def format_tags(tags):
    data = []
    for tag in tags:
        data.append({'name': str(tag)})

    return data


def format_to_key(values):
    """
    contacts и companies имеют одингковый формат.
    """
    data = []
    for value in values:
        data.append({'id': int(value)})

    return data


def validate_lead_note_params(text=None, uniq=None, duration=None, source=None, link=None, phone=None, service=None,
                              status=None, icon_url=None, params=None, address=None, longitude=None, latitude=None):
    if text and not isinstance(text, str):
        raise KeyError('duration must be <str>')
    elif uniq and not isinstance(uniq, str):
        raise KeyError('uniq must be <str>')
    elif duration and not isinstance(duration, int):
        raise KeyError('duration must be <int>')
    elif source and not isinstance(source, str):
        raise KeyError('source must be <str>')
    elif link and not isinstance(link, str):
        raise KeyError('link must be <str>')
    elif phone and not isinstance(phone, str):
        raise KeyError('phone must be <str>')
    elif service and not isinstance(service, str):
        raise KeyError('service must be <str>')
    elif status and not isinstance(status, str):
        raise KeyError('status must be <str>')
    elif icon_url and not isinstance(icon_url, str):
        raise KeyError('icon_url must be <str>')
    elif params and not isinstance(params, str):
        raise KeyError('params must be <str>')
    elif address and not isinstance(address, str):
        raise KeyError('address must be <str>')
    elif longitude and not isinstance(longitude, str):
        raise KeyError('longitude must be <str>')
    elif latitude and not isinstance(latitude, str):
        raise KeyError('latitude must be <str>')


def validate_lead_note(note_type, params):
    data = {'note_type': note_type}
    if note_type == 'common':
        text = params.get('text', None)
        if not text: raise KeyError('Type "common" must have params text')
        validate_lead_note_params(text=text)

        data.update({'params': {'text': text}})
    elif note_type in ('call_in', 'call_out'):
        uniq = params.get('uniq', None)
        duration = params.get('duration', None)
        source = params.get('source', None)
        link = params.get('link', None)
        phone = params.get('phone', None)
        if not uniq or not duration or not source or not link or not phone:
            raise KeyError('Type "{}" must have params: uniq, duration, source, link and phone'.format(note_type))
        validate_lead_note_params(uniq=uniq, duration=duration, source=source, link=link, phone=phone)

        data.update({'params': {'uniq': uniq, 'duration': duration, 'source': source, 'link': link, 'phone': phone}})
    elif note_type in ('service_message', 'extended_service_message'):
        service = params.get('service', None)
        text = params.get('text', None)
        if not service or not text:
            raise KeyError('Type "{}" must have params: service and text'.format(note_type))
        validate_lead_note_params(service=service, text=text)

        data.update({'params': {'service': service, 'text': text}})
    elif note_type == 'message_cashier':
        status = params.get('status', None)
        text = params.get('text', None)
        if not status or not text:
            raise KeyError('Type "message_cashier" must have params: status and text')
        elif status not in ('created', 'shown', 'canceled'):
            raise ValueError('Type message_cashier must have status one of the created, shown or canceled')
        validate_lead_note_params(status=status, text=text)

        data.update({'params': {'status': status, 'text': text}})
    elif note_type == 'invoice_paid':
        icon_url = params.get('icon_url', None)
        service = params.get('service', None)
        text = params.get('text', None)
        if not icon_url or not service or not text:
            raise KeyError('Type "invoice_paid" must have params: icon_url, service and text')
        validate_lead_note_params(icon_url=icon_url, service=service, text=text)

        data.update({'params': {'icon_url': icon_url, 'service': service, 'text': text}})
    elif note_type == 'geolocation':
        text = params.get('text', None)
        address = params.get('text', None)
        longitude = params.get('text', None)
        latitude = params.get('text', None)
        if not text or not address or not longitude or not latitude:
            raise KeyError('Type "geolocation" must have params: text, address, longitude, latitude')
        validate_lead_note_params(text=text, address=address, longitude=longitude, latitude=latitude)

        data.update({'params': {'text': text, 'address': address, 'longitude': longitude, 'latitude': latitude}})
    elif note_type in ('sms_in', 'sms_out'):
        text = params.get('text', None)
        phone = params.get('phone', None)
        if not text or not phone:
            raise KeyError('Type "{}" must have params: text and phone'.format(note_type))
        validate_lead_note_params(text=text, phone=phone)

        data.update({'params': {'text': text, 'phone': phone}})
    else:
        raise ValueError('Invalid note type')

    return data
