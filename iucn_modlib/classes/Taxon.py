#!/usr/bin/python3

from dataclasses import dataclass, field
from .IUCNHabitatCodes import IUCNHabitatCodes_v3_1
from typing import List


@dataclass
class Taxon:
    """A Taxon Parameter dataclass.
    
    Fields available from the IUCN Red List API.
    """
    taxonid: int
    scientific_name: str
    kingdom: str
    phylum: str
    class_: str
    order: str
    family: str
    genus: str
    main_common_name: str
    authority: str
    published_year: int
    assessment_date: str
    category: str
    criteria: str
    population_trend: str
    marine_system: bool
    freshwater_system: bool
    terrestrial_system: bool
    assessor: str
    reviewer: str
    aoo_km2: float
    eoo_km2: float
    elevation_upper: int
    elevation_lower: int
    depth_upper: int
    depth_lower: int
    errata_flag: str
    errata_reason: str
    amended_flag: str
    amended_reason: str
    habitats: List = field(default_factory=lambda: [])
    
    def habitatCodes(self, habitatFilters = None):
        """Return habitat codes

        If habitatFilters (habitat filters object) is provided, filters the codes.
        """
        # if habitats are empty, return empty list
        if len(self.habitats) == 0:
            return []
        if habitatFilters is None:
            return [ h['code'] for h in self.habitats ]
        else:
            habitats = self.habitats
            if habitatFilters.season is not None:
                habitats = [ h for h in habitats if h['season'] in habitatFilters.season ]
            if habitatFilters.suitability is not None:
                habitats = [ h for h in habitats if h['suitability'] in habitatFilters.suitability ]
            if habitatFilters.majorImportance is not None:
                habitats = [ h for h in habitats if h['majorimportance'] in habitatFilters.majorImportance ]
            return [ h['code'] for h in habitats ]
    
    def habitatNames(self, habitatFilters = None):
        """Return habitat names

        If habitatFilters (habitat filters object) is provided, filters the names.
        """
        # if habitats are empty, return empty list
        if len(self.habitats) == 0:
            return []
        if habitatFilters is None:
            return [ h['habitat'] for h in self.habitats ]
        else:
            habitats = self.habitats
            if habitatFilters.season is not None:
                habitats = [ h for h in habitats if h['season'] in habitatFilters.season ]
            if habitatFilters.suitability is not None:
                habitats = [ h for h in habitats if h['suitability'] in habitatFilters.suitability ]
            if habitatFilters.majorImportance is not None:
                habitats = [ h for h in habitats if h['majorimportance'] in habitatFilters.majorImportance ]
            return [ h['habitat'] for h in habitats ]
    
    def fix(self, fixType):
        """Fixes elements in the Taxon object

        These can be applied in any order

        Examples:
            Taxon.fix('elevation')
            Taxon.fix('habitats')

        """
        def elevation():
            """Fix elevation

            If elevation values are are inverted, its impossible to nkow which
            one is wrong.
                Inserts default values for both:
                    elevation_lower -> -500
                    elevation_upper -> 9000

            Sometimes one or both elevations are missing.
                Inserts default values for the missing one(s):
                    elevation_lower -> -500
                    elevation_upper -> 9000

            Sometimes elevaions may be unreasonable.
            E.g. below -500 or above 9000 (It's over 9000!)
                Inserts default values for the unreasonable one(s):
                    elevation_lower -> -500
                    elevation_upper -> 9000
            
            Sometimes the interval is too small to be useful for practical
            purposes.
            E.g. elevation range below 50m.
                Expand the elevation range to be 50m, adding half of what's
                missing below the lower elevation, and the other half above
                the upper elevation. THEN, if the lower or upper elevations
                are out of bounds (outside of the -500 - 9000 range), shift
                both ranges up or down accordingly.
            """
            # Warning, the order of the fixes is important
            #
            # When elevation values are inverted it is impossible to know which one is wrong.
            if self.elevation_lower is not None and self.elevation_upper is not None:
                if self.elevation_lower > self.elevation_upper:
                    self.elevation_lower = -500
                    self.elevation_upper = 9000
            # Sometimes elevation values are missing
            if self.elevation_lower is None:
                self.elevation_lower = -500
            if self.elevation_upper is None:
                self.elevation_upper = 9000
            # Sometimes the elevations may simply be unreasonable
            if self.elevation_lower < -500:
                self.elevation_lower = -500
            if self.elevation_upper > 9000:
                self.elevation_upper = 9000
            # If the elevation extent is too small, it makes no sense to make a model.
            if self.elevation_upper - self.elevation_lower < 50:
                # Find the difference to have at least 50m elevation range
                diff = 50 - (self.elevation_upper - self.elevation_lower)
                # Distribute it up and down
                self.elevation_lower = self.elevation_lower - (diff // 2)  # minus floor division
                self.elevation_upper = self.elevation_upper + -(-diff // 2) # plus ceiling division hack
                # Oh no! Now you may have elevations out of bounds! Fix it.
                # Either by moving everything up
                if self.elevation_lower < -500:
                    diff = -500 - self.elevation_lower
                    self.elevation_lower = self.elevation_lower + diff
                    self.elevation_upper = self.elevation_upper + diff
                # Or down
                if self.elevation_upper > 9000:
                    diff = self.elevation_upper - 9000
                    self.elevation_lower = self.elevation_lower - diff
                    self.elevation_upper = self.elevation_upper - diff

        def habitats():
            """Fix habitat parameters

            If values for seson, suitability and majorimportance are set to None,
            assume they are unknown and assign the default unknown value.
            """
            # if habitats are empty, exit
            if len(self.habitats) == 0:
                return
            for h in self.habitats:
                if h['season'] is None:
                    h['season'] = 'Seasonal Occurrence Unknown'
                if h['suitability'] is None:
                    h['suitability'] = 'Unknown'
                if h['majorimportance'] is None:
                    h['majorimportance'] = 'No'

        def habitats_unmappable(unmapList = 'jung'):
            '''Refer to translators to see which codes cannot be translated,
            or provide your own unmapList if you are not using a translator.
            (Right now I can't imagine why you may want to use your own translator)

            Deprecated. This functionality is now managed by the translators.
            Code left temporarily and will be deleted in future updates.
            '''
            # if habitats are empty, exit
            if len(self.habitats) == 0:
                return
            # IUCN habitat codes machine
            HC = IUCNHabitatCodes_v3_1()

            switcher={
                'jung':('7', '7.1', '7.2', '9.8.1', '9.8.2', '9.8.3', '9.8.4', '9.8.5', '9.8.6', '11.1.1', '11.1.2', '13', '13.1', '13.2', '13.3', '13.4', '13.5', '15', '15.1', '15.2', '15.3', '15.4', '15.5', '15.6', '15.7', '15.8', '15.9', '15.10', '15.11', '15.12', '15.13', '16', '18'),
                'esa_cci':('1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.1', '2.2', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15', '5.16', '5.17', '5.18', '7', '7.1', '7.2', '8.1', '8.2', '8.3', '9.1', '9.2', '9.3', '9.4', '9.5', '9.6', '9.7', '9.8', '9.8', '9.8', '9.8.3', '9.8.4', '9.8.5', '9.8.6', '9.9', '9.10', '10.1', '10.2', '10.3', '10.4', '11.1', '11.1.1', '11.1.2', '11.2', '11.3', '11.4', '11.5', '11.6', '12.1', '12.2', '12.3', '12.4', '12.5', '12.6', '12.7', '13.1', '13.2', '13.3', '13.4', '13.5', '14.1', '14.2', '14.3', '14.4', '14.5', '14.6', '15.1', '15.2', '15.3', '15.4', '15.5', '15.6', '15.7', '15.8', '15.9', '15.10', '15.11', '15.12', '15.13', '17', '18')
                }
            
            def unsupported():
                raise ValueError(f"Supported formats are {', '.join(switcher.keys())}. Or provide your own list or tuple.")

            if type(unmapList) in (tuple, list):
                pass
            else:
                unmapList = switcher.get(unmapList, unsupported)

            # for each unmappable habitat in self.habitats that is not level 1, update it with the higher set.
            # repeat until all unmappable habitats are at level 1.
            while not all([h['code'] not in unmapList or HC.codeLevel(h['code']) == 1 for h in self.habitats]):
                h = self.habitats.pop(0)
                if h['code'] not in unmapList or HC.codeLevel(h['code']) == 1:
                    self.habitats.append(h)
                else:
                    for code in HC.toLevel(h['code'], HC.codeLevel(h['code'])-1):
                        self.habitats.append({
                            'code': code,
                            'habitat': HC.codeName(code),
                            'suitability': h['suitability'],
                            'season': h['season'],
                            'majorimportance': h['majorimportance']
                            })

            # remove habitats that are truly unmappable
            self.habitats = [h for h in self.habitats if h['code'] not in unmapList]

        def habitats_seasonal():
            '''If the taxon object has no suitable habitats for each season,
            assume that all habitat types are suitable for that season.

            Deprecated. This functionality is now managed by the habitatFilters.
            Code left temporarily and will be deleted in future updates.
            '''
            # check if unseasonal habitat list is empty
            if len([h for h in self.habitats if h['season'] in ('Resident', 'Seasonal Occurrence Unknown', None)]) == 0:
                # check if seasonal habitat list is empty
                for season in ('Breeding Season', 'Non-Breeding Season'):
                    if len([h for h in self.habitats if h['season'] == season]) == 0:
                        HC = IUCNHabitatCodes_v3_1()
                        self.habitats.extend(
                            [
                                {
                                    'code': code,
                                    'habitat': HC.codeName(code),
                                    'suitability': 'Unknown',
                                    'season': season,
                                    'majorimportance': 'No'
                                }
                                for code in HC.codes
                            ]
                            )

        def unsupported():
            raise ValueError('Supported templates are: {}'.format(', '.join(switcher.keys())))

        switcher={
            'elevation':elevation,
            'habitats':habitats
            }

        fixer = switcher.get(fixType, unsupported)
        fixer()
        return


# HIC SVNT DRACONES