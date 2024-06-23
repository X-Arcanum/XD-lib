import requests

def parse_buttons(buttons):
    try:
        if isinstance(buttons[0], list):
            btns = buttons
        else:
            btns = [buttons]
    except IndexError:
        return None

    button_type = buttons[0][0].get('_')
    if button_type in ('inline_keyboard', 'keyboard'):
        return {button_type: btns}
    else:
        return None

def parse_url(url):
    parsed_url = requests.utils.urlparse(url)
    query_params = dict(param.split('=') for param in parsed_url.query.split('&'))
    return query_params
