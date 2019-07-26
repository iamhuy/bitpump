from django.db import models


class PositiveBigIntegerField(models.BigIntegerField):
    empty_strings_allowed = False

    def db_type(self, connection):
        return "BIGINT UNSIGNED"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': models.BigIntegerField.MAX_BIGINT * 2 + 1}
        defaults.update(kwargs)
        return super(PositiveBigIntegerField, self).formfield(**defaults)
