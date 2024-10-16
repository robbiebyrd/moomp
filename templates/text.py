from services.session import TextSession


class BaseTextTemplate:

    def __init__(self, session: TextSession):
        self._session = session

    @staticmethod
    def load(template: str):
        with open(template, 'r', encoding='unicode_escape') as tmpl_file:
            return tmpl_file.read()
