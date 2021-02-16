#!/usr/bin/python3

from ..classes.HabitatFilters import HabitatFilters

def HabitatFiltersFactory(template = None):
    """A Factory for HabitatFilters objects

    Standard templates for common HabitatFilters.

    'kba_breeding':    standard filters for KBA breeding seasons
    'kba_nonbreeding': standard filters for KBA nonbreeding seasons
    
    """

    def kba_breeding():
        return HabitatFilters(
            season = ('Resident', 'Breeding Season', 'Seasonal Occurrence Unknown'),
            suitability = ('Suitable', 'Unknown'),
            majorImportance = ('Yes', 'No')
            )

    def kba_nonbreeding():
        return HabitatFilters(
            season = ('Resident', 'Non-Breeding Season', 'Seasonal Occurrence Unknown'),
            suitability = ('Suitable', 'Unknown'),
            majorImportance = ('Yes', 'No')
            )

    def unsupported():
        raise ValueError(f"""Supported templates are: '{"', '".join(switcher.keys())}'""")

    switcher={
        'kba_breeding':    kba_breeding,
        'kba_nonbreeding': kba_nonbreeding
        }

    # The template string is converted to a template function and run.
    # If the template is not in the switcher, unsupported() is defined and run,
    # raising an error and specifying which templates are available.
    template =  switcher.get(template, unsupported)
    return template()


# HIC SVNT DRACONES