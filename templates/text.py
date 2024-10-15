class BaseTextTemplate:

    @staticmethod
    def load(template: str):
        f = open(
            file=template,
            mode="r",
            encoding='unicode_escape'
        )

        return f.read()
