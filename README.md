# IUCN ModLib
IUCN Modelling Library

## Name
iucn_modlib

## Description
A Python library to facilitate the development of Habitat Models with data from IUCN.

This library allows the user to create `Taxon` objects from the IUCN Red List API and and use them to extract information necessary to develop Habitat Models (HM) or Area of Habitat (AOH) models.

A series of helpers are included, such as factories to automatically create and clean data from IUCN, habitat filters to define desired habitat parameters, and translators to convert species-habitat associations (IUCN Red List habitat codes) into the equivalent values used in land-cover rasters.

## Installation

### From GitLab
```pip install git+https://gitlab.com/daniele.baisero/iucn-modlib```

### From PIP
```pip install iucn_modlib```

## Requirements
For some functionalities you will need an IUCN Red List API token, obtainable
from [https://apiv3.iucnredlist.org/](https://apiv3.iucnredlist.org/).

## Usage
```
import iucn_modlib

token = 'your IUCN Red List API token here'

# Create a taxon object using a species' scientific name or its taxon id.
taxon = iucn_modlib.TaxonFactoryRedListAPI('Ursus maritimus', token)
taxon = iucn_modlib.TaxonFactoryRedListAPI(22823, token)

# By default the taxon factories apply elevation and habitat fixes. You can request the taxon object to be constructed without applying fixes.
taxon = iucn_modlib.TaxonFactoryRedListAPI('Ursus maritimus', token, fixElevation=False, fixHabitats=False)


# The taxon object can be used to obtain the species' parameters
taxon
taxon.kingdom
taxon.phylum
taxon.class_
taxon.order
taxon.family
taxon.genus
taxon.scientific_name
taxon.category

# Parameters useful for model development include elevation, depth, habitat systems.
taxon.elevation_lower
taxon.elevation_upper
taxon.depth_upper
taxon.depth_lower
taxon.marine_system
taxon.freshwater_system
taxon.terrestrial_system


# The taxon object can also be used to obtain lists of the species' habitats and their iucn habitat codes.
taxon.habitatNames()
taxon.habitatCodes()

# These can be filtered using Habitat Filter objects, for example if you are only interested in a species' breeding or non-breeding habitats.
# Create a custom Habitat Filter or use a template.
HF = iucn_modlib.HabitatFilters(
    season = ('Resident', 'Breeding Season', 'Non-Breeding Season', 'Seasonal Occurrence Unknown'),
    suitability = ('Suitable', 'Unknown'),
    majorImportance = ('Yes', 'No')
    )
HF_br = iucn_modlib.HabitatFiltersFactory(template='kba_breeding')
HF_nb = iucn_modlib.HabitatFiltersFactory(template='kba_nonbreeding')

# You can then use the habitat filter to filter a taxon's habitat names and codes
taxon.habitatNames(habitatFilters=HF_br)
taxon.habitatNames(habitatFilters=HF_nb)
taxon.habitatCodes(habitatFilters=HF_br)
taxon.habitatCodes(habitatFilters=HF_nb)


# The translators can be used to convert habitat codes (filtered or un-filtered) into the corresponding pixel values in select land-cover maps.
polar_bear_breeding_codes = taxon.habitatCodes(habitatFilters=HF_br)
iucn_modlib.translator.toJung(polar_bear_breeding_codes)
iucn_modlib.translator.toESACCI(polar_bear_breeding_codes)
```

## Support
For support please use the issue tracker at [https://gitlab.com/daniele.baisero/iucn-modlib](https://gitlab.com/daniele.baisero/iucn-modlib).

## Contributing
The project is open to contributions. Please contact Daniele Baisero.

## Authors and acknowledgment
This library was ideated, designed and coded by Daniele Baisero. Michael Dales provided invaluable feedback and improvements.

## License
ISC license. Please read the LICENSE file.

## Project status
This library is under active development.