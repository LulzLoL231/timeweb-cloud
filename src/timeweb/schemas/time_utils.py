# -*- coding: utf-8 -*-
'''Time utilites.'''
import datetime
from typing import Any, Callable, Generator, TYPE_CHECKING

import isodate
from isodate.duration import Duration
from isodate.isoduration import ISO8601_PERIOD_REGEX
from pydantic.validators import str_validator


__all__ = ['Period']
if TYPE_CHECKING:
    GeneratorCallableStr = Generator[Callable[[str], str | "Period"], None, None]


class Period(Duration, str):
    '''Period class for working with ISO 8601 durations.

    Examples:
        >>> period = Period('P1Y2M3W4D')
        >>> period.timedelta  # timedelta(days=450)

    References:
        >>> help(isodate.duration.Duration)
    '''
    def __init__(self, period: str):
        '''Initialize period from ISO 8601 duration string.

        Args:
            period (str): ISO 8601 duration string.
        '''
        self.raw = period
        self.period = isodate.parse_duration(period)
        super().__init__(days=getattr(self.period, 'days', 0),
                         seconds=getattr(self.period, 'seconds', 0),
                         microseconds=getattr(self.period, 'microseconds', 0),
                         milliseconds=getattr(self.period, 'milliseconds', 0),
                         minutes=getattr(self.period, 'minutes', 0),
                         hours=getattr(self.period, 'hours', 0),
                         weeks=getattr(self.period, 'weeks', 0),
                         months=getattr(self.period, 'months', 0),
                         years=getattr(self.period, 'years', 0))

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(
            type="string", format="period", example="P1Y2M3W4D"
        )

    @classmethod
    def __get_validators__(cls) -> "GeneratorCallableStr":
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: str) -> "Period":
        match = ISO8601_PERIOD_REGEX.match(value)
        if not match:
            raise ValueError(f'Invalid period string: {value!r}')

        return cls(value)

    @property
    def timedelta(self) -> datetime.timedelta:
        '''Alias for `self.totimedelta(datetime.now())`.

        Returns:
            datetime.timedelta: Timedelta.
        '''
        return self.totimedelta(datetime.datetime.now())

    def __str__(self) -> str:
        return self.raw

    def __repr__(self) -> str:
        return f'Period({self.raw!r})'
