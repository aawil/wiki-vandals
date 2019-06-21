def title_to_link(title):
    title_underscore = title.translate(str.maketrans(' ', '_'))
    url = f'https://en.wikipedia.org/wiki/{title_underscore}'
    link = f'<a href="{url}" target="_blank">{title}</a>'
    return link