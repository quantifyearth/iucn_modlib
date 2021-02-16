#!/usr/bin/python3

from dataclasses import dataclass
from typing import Tuple


@dataclass
class HabitatFilters:
    """A dataclass to store habitat filters.
    
    The intended use is as a parameter to Taxon.habitatCodes and
    Taxon.habitatNames. The habitat codes and names will be returned only for
    habitat elements where seasonality, suitability and majorImportance values
    match those included in the HabitatFiltes object.
    Filters are applied AND-wise, not OR-wise.

    season: tuple: Season values to be returned.
        Defaults to ('Resident', 'Breeding Season', 'Non-Breeding Season', 'Seasonal Occurrence Unknown').
    suitability: tuple: Suitability values to be returned.
        Defaults to ('Suitable', 'Unknown').
    majorImportance: tuple: Habitats major improtance values to be returned.
        Defaults to ('Yes', 'No')
    """

    season: Tuple = None
    suitability: Tuple = None
    majorImportance: Tuple = None

    if season is None:
        season = ('Resident', 'Breeding Season', 'Non-Breeding Season', 'Seasonal Occurrence Unknown')
    if suitability is None:
        suitability = ('Suitable', 'Unknown')
    if majorImportance is None:
        majorImportance = ('Yes', 'No')

# HIC SVNT DRACONES