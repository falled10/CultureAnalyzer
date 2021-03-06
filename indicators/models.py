import re

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator

__all__ = ['CountryIndicator', 'IndicatorField', 'INDICATORS_ORDER']

MAX_FIELD_REPRESENTATION = 20
INDICATORS_ORDER = ('pdi', 'idv', 'mas', 'uai', 'lto', 'ivr')
_RE_ISO_CODE = re.compile(r'^[a-z]{3}$', re.IGNORECASE)


class IndicatorField(models.PositiveIntegerField):
    default_validators = [MinValueValidator(0), MaxValueValidator(100)]


class CountryIndicator(models.Model):
    iso_code = models.CharField(max_length=3, unique=True,
                                validators=[RegexValidator(_RE_ISO_CODE)])
    name = models.CharField(max_length=200, unique=True)
    pdi = IndicatorField(verbose_name='PDI')
    idv = IndicatorField(verbose_name='IDV')
    mas = IndicatorField(verbose_name='MAS')
    uai = IndicatorField(verbose_name='UAI')
    lto = IndicatorField(verbose_name='LTO')
    ivr = IndicatorField(verbose_name='IVR')

    class Meta:
        db_table = 'countries_indicators'
        ordering = ['iso_code', 'name']
        verbose_name_plural = 'countries\' indicators'

    def __str__(self):
        return f'{self.name[:MAX_FIELD_REPRESENTATION]} - {self.iso_code}'

    @property
    def get_indicators(self):
        """
        Return indicators values for single instance
        :return: dict{iso_code:[pdi, idv, mas, uai, lto, ivr]}.
        Where, key: iso_code which mean country identifier and value: list of
        indicators values
        """

        country_values = {
            self.iso_code: [getattr(self, ind) for ind in INDICATORS_ORDER]}
        return country_values
