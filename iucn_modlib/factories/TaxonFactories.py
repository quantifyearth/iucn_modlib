#!/usr/bin/python3

from ..classes.Taxon import Taxon
from .. import redlist_api
import json
import pandas
import numpy
import os


def unwrap(val, key):
    try:
        return val[key].values[0]
    except (KeyError, IndexError):
        return ""


def TaxonFactoryRedListAPI(
        sp, token,
        fixElevation = True, fixHabitats = True
        ):
    """A Factory for Taxon objects from the Red List API

    Given a species numeric ID or scientific binomial,
    pulls data from the IUCN Red List API and constructs a Taxon object.
    """

    # Get species assessment and habitats
    if type(sp) == int:
        tax_ass = redlist_api.v3.id_to_assessment(sp, token)
        tax_hab = redlist_api.v3.id_to_habitats(sp, token)
    elif type(sp) == str:
        if len(sp.split()) != 2:
            raise ValueError("Species names must be binomial 'Genus species'.")
        tax_ass = redlist_api.v3.name_to_assessment(sp, token)
        tax_hab = redlist_api.v3.name_to_habitats(sp, token)
    else:
        raise TypeError('sp must be a string or integer')
    
    # Validate api call results
    if 'message' in tax_ass:
        raise ValueError(tax_ass['message'])
    if 'message' in tax_hab:
        raise ValueError(tax_hab['message'])
    if 'result' not in tax_ass:
        raise ValueError('assessment api call did not return a result.')
    elif len(tax_ass['result']) == 0:
        raise ValueError('assessment api call returned an empty result.')
    if 'result' not in tax_hab:
        raise ValueError('habitats api call did not return a result.')
    elif len(tax_hab['result']) == 0:
        raise ValueError('habitats api call returned an empty result.')

    # Compile Taxon Object
    tax = Taxon(
        taxonid            = tax_ass['result'][0]['taxonid'],
        scientific_name    = tax_ass['result'][0]['scientific_name'],
        kingdom            = tax_ass['result'][0]['kingdom'],
        phylum             = tax_ass['result'][0]['phylum'],
        class_             = tax_ass['result'][0]['class'],
        order              = tax_ass['result'][0]['order'],
        family             = tax_ass['result'][0]['family'],
        genus              = tax_ass['result'][0]['genus'],
        main_common_name   = tax_ass['result'][0]['main_common_name'],
        authority          = tax_ass['result'][0]['authority'],
        published_year     = tax_ass['result'][0]['published_year'],
        assessment_date    = tax_ass['result'][0]['assessment_date'],
        category           = tax_ass['result'][0]['category'],
        criteria           = tax_ass['result'][0]['criteria'],
        population_trend   = tax_ass['result'][0]['population_trend'],
        marine_system      = tax_ass['result'][0]['marine_system'],
        freshwater_system  = tax_ass['result'][0]['freshwater_system'],
        terrestrial_system = tax_ass['result'][0]['terrestrial_system'],
        assessor           = tax_ass['result'][0]['assessor'],
        reviewer           = tax_ass['result'][0]['reviewer'],
        aoo_km2            = tax_ass['result'][0]['aoo_km2'],
        eoo_km2            = tax_ass['result'][0]['eoo_km2'],
        elevation_upper    = tax_ass['result'][0]['elevation_upper'],
        elevation_lower    = tax_ass['result'][0]['elevation_lower'],
        depth_upper        = tax_ass['result'][0]['depth_upper'],
        depth_lower        = tax_ass['result'][0]['depth_lower'],
        errata_flag        = tax_ass['result'][0]['errata_flag'],
        errata_reason      = tax_ass['result'][0]['errata_reason'],
        amended_flag       = tax_ass['result'][0]['amended_flag'],
        amended_reason     = tax_ass['result'][0]['amended_reason'],
        habitats           = tax_hab['result']
    )
    
    # fix
    if fixElevation:
        tax.fix(fixType = 'elevation')
    if fixHabitats:
        tax.fix(fixType = 'habitats')

    # return
    return tax


def TaxonFactoryRedListAPIJsons(
        assessmentJSON, habitatsJSON,
        fixElevation = True, fixHabitats = True
        ):
    """A Factory for Taxon objects from Red List API JSON responses

    Given the paths to JSON files with Red List API results
    (assessment and habitat), constructs a Taxon object.
    """

    # load saved API results
    with open(assessmentJSON) as f:
        tax_ass = json.load(f)
    with open(habitatsJSON) as f:
        tax_hab = json.load(f)

    # Validate api call results (from saved jsons)
    if 'message' in tax_ass:
        raise ValueError(tax_ass['message'])
    if 'message' in tax_hab:
        raise ValueError(tax_hab['message'])
    if 'result' not in tax_ass:
        raise ValueError('assessment api call did not return a result.')
    elif len(tax_ass['result']) == 0:
        raise ValueError('assessment api call returned an empty result.')
    if 'result' not in tax_hab:
        raise ValueError('habitats api call did not return a result.')
    elif len(tax_hab['result']) == 0:
        raise ValueError('habitats api call returned an empty result.')

    # Compile Taxon Object
    tax = Taxon(
        taxonid            = tax_ass['result'][0]['taxonid'],
        scientific_name    = tax_ass['result'][0]['scientific_name'],
        kingdom            = tax_ass['result'][0]['kingdom'],
        phylum             = tax_ass['result'][0]['phylum'],
        class_             = tax_ass['result'][0]['class'],
        order              = tax_ass['result'][0]['order'],
        family             = tax_ass['result'][0]['family'],
        genus              = tax_ass['result'][0]['genus'],
        main_common_name   = tax_ass['result'][0]['main_common_name'],
        authority          = tax_ass['result'][0]['authority'],
        published_year     = tax_ass['result'][0]['published_year'],
        assessment_date    = tax_ass['result'][0]['assessment_date'],
        category           = tax_ass['result'][0]['category'],
        criteria           = tax_ass['result'][0]['criteria'],
        population_trend   = tax_ass['result'][0]['population_trend'],
        marine_system      = tax_ass['result'][0]['marine_system'],
        freshwater_system  = tax_ass['result'][0]['freshwater_system'],
        terrestrial_system = tax_ass['result'][0]['terrestrial_system'],
        assessor           = tax_ass['result'][0]['assessor'],
        reviewer           = tax_ass['result'][0]['reviewer'],
        aoo_km2            = tax_ass['result'][0]['aoo_km2'],
        eoo_km2            = tax_ass['result'][0]['eoo_km2'],
        elevation_upper    = tax_ass['result'][0]['elevation_upper'],
        elevation_lower    = tax_ass['result'][0]['elevation_lower'],
        depth_upper        = tax_ass['result'][0]['depth_upper'],
        depth_lower        = tax_ass['result'][0]['depth_lower'],
        errata_flag        = tax_ass['result'][0]['errata_flag'],
        errata_reason      = tax_ass['result'][0]['errata_reason'],
        amended_flag       = tax_ass['result'][0]['amended_flag'],
        amended_reason     = tax_ass['result'][0]['amended_reason'],
        habitats           = tax_hab['result']
    )
    
    # fix
    if fixElevation:
        tax.fix(fixType = 'elevation')
    if fixHabitats:
        tax.fix(fixType = 'habitats')

    # return
    return tax


def loadBatchSource(path):
    '''Helper function for TaxonFactoryRedListBatch
    '''

    # load assessment table
    assessments = pandas.read_csv(os.path.join(path,'assessments.csv'), low_memory = False)
    # load taxonomy table
    taxonomy = pandas.read_csv(os.path.join(path,'taxonomy.csv'), low_memory = False)
    
    # load and fix habitats table
    # the batch downwlod files are not as clean as API data, so ad-hoc fixes are needed
    habitats = pandas.read_csv(os.path.join(path,'habitats.csv'), low_memory = False)
    habitats.loc[habitats.season == 'passage', 'season'] = 'Passage'
    habitats.loc[habitats.season == 'resident', 'season'] = 'Resident'
    habitats.loc[habitats.season == 'breeding', 'season'] = 'Breeding Season'
    habitats.loc[habitats.season == 'non-breeding', 'season'] = 'Non-Breeding Season'
    habitats.loc[habitats.season == 'unknown', 'season'] = 'Seasonal Occurrence Unknown'
    habitats.rename(columns={
        'assessmentId': 'assid',
        'internalTaxonId': 'taxonid',
        'scientificName': 'scientific_name',
        'code': 'code',
        'name': 'habitat',
        'majorImportance': 'majorimportance',
        'season': 'season',
        'suitability': 'suitability'},
        inplace=True
        )

    # load all_other_fields table
    all_other_fields = pandas.read_csv(os.path.join(path,'all_other_fields.csv'), low_memory = False)

    # load common_names table
    common_names = pandas.read_csv(os.path.join(path,'common_names.csv'), low_memory = False)
    
    # Return
    return {
        'assessments': assessments,
        'taxonomy': taxonomy,
        'habitats': habitats,
        'all_other_fields': all_other_fields,
        'common_names': common_names
        }


def TaxonFactoryRedListBatch(species, source, fixElevation = True, fixHabitats = True):
    """A Factory for Taxon objects

    Given a species numeric ID or scientific binomial,
    pulls data from a Red List batch download folder.
    """
    # determine source type
    if type(source) != dict:
        source = loadBatchSource(source)
    # defind ids
    try:
        taxid = int(species)
    except:
        taxid = source['assessments'].loc[source['assessments'].scientificName == species, 'internalTaxonId'].values[0]
    # filter tables
    assessments = source['assessments'].loc[source['assessments'].internalTaxonId == taxid]
    taxonomy = source['taxonomy'].loc[source['taxonomy'].internalTaxonId == taxid]
    habitats = source['habitats'].loc[source['habitats'].taxonid == taxid]
    all_other_fields = source['all_other_fields'].loc[source['all_other_fields'].internalTaxonId == taxid]
    common_names = source['common_names'].loc[source['common_names'].internalTaxonId == taxid].loc[source['common_names'].main == True]
    # create taxon object
    tax = Taxon(
        taxonid            = assessments['internalTaxonId'].values[0],
        scientific_name    = assessments['scientificName'].values[0],
        kingdom            = unwrap(taxonomy,'kingdomName'),
        phylum             = unwrap(taxonomy, 'phylumName'),
        class_             = unwrap(taxonomy,'className'),
        order              = unwrap(taxonomy, 'orderName'),
        family             = unwrap(taxonomy,'familyName'),
        genus              = unwrap(taxonomy,'genusName'),
        main_common_name   = unwrap(common_names,'name'),
        authority          = unwrap(taxonomy,'authority'),
        published_year     = unwrap(assessments, 'yearPublished'),
        assessment_date    = unwrap(assessments,'assessmentDate'),
        category           = unwrap(assessments,'redlistCategory'),
        criteria           = unwrap(assessments,'redlistCriteria'),
        population_trend   = unwrap(assessments,'populationTrend'),
        marine_system      = unwrap(assessments,'systems').find('Marine') != -1,
        freshwater_system  = unwrap(assessments,'systems').find('Freshwater') != -1,
        terrestrial_system = unwrap(assessments,'systems').find('Terrestrial') != -1,
        assessor           = 'AOH modeller: not available in batch',
        reviewer           = 'AOH modeller: not available in batch',
        aoo_km2            = unwrap(all_other_fields, 'AOO.range'),
        eoo_km2            = unwrap(all_other_fields,'EOO.range'),
        elevation_upper    = int(all_other_fields['ElevationUpper.limit'].values[0]) \
            if not numpy.isnan(all_other_fields['ElevationUpper.limit'].values[0]) else None,
        elevation_lower    = int(all_other_fields['ElevationLower.limit'].values[0]) \
            if not numpy.isnan(all_other_fields['ElevationLower.limit'].values[0]) else None,
        depth_upper        = int(all_other_fields['DepthUpper.limit'].values[0]) \
            if not numpy.isnan(all_other_fields['DepthUpper.limit'].values[0]) else None,
        depth_lower        = int(all_other_fields['DepthLower.limit'].values[0]) \
            if not numpy.isnan(all_other_fields['DepthLower.limit'].values[0]) else None,
        errata_flag        = 'AOH modeller: not available in batch',
        errata_reason      = 'AOH modeller: not available in batch',
        amended_flag       = 'AOH modeller: not available in batch',
        amended_reason     = 'AOH modeller: not available in batch',
        habitats           = habitats.to_dict('records')
    )
    
    # fix
    if fixElevation:
        tax.fix(fixType = 'elevation')
    if fixHabitats:
        tax.fix(fixType = 'habitats')
    
    #return
    return tax


def TaxonFactoryKBADB(species, con, fixElevation = True, fixHabitats = True):
    """A Factory for Taxon objects

    Given a species numeric ID or scientific binomial,
    pulls data from the KBA database.
    """

    # define id
    try:
        id = int(species)
    except:
        with con.cursor() as cur:
            cur.execute(f"SELECT taxonid from iucn_species where scientific_name = '{species}'")
            id = cur.fetchone()[0]
    
    # collate species record
    import psycopg2.extras
    with con.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f'SELECT * from iucn_species where taxonid = {id}')
        assessment = cur.fetchall()
        cur.execute(f'SELECT * from iucn_habitats where taxonid = {id}')
        habitats = cur.fetchall()
    
    # create taxon object
    tax = Taxon(
        taxonid            = assessment[0]['taxonid'],
        scientific_name    = assessment[0]['scientific_name'],
        kingdom            = assessment[0]['kingdom'],
        phylum             = assessment[0]['phylum'],
        class_             = assessment[0]['class'],
        order              = assessment[0]['order'],
        family             = assessment[0]['family'],
        genus              = assessment[0]['genus'],
        main_common_name   = assessment[0]['main_common_name'],
        authority          = assessment[0]['authority'],
        published_year     = assessment[0]['published_year'],
        assessment_date    = assessment[0]['assessment_date'],
        category           = assessment[0]['category'],
        criteria           = assessment[0]['criteria'],
        population_trend   = assessment[0]['population_trend'],
        marine_system      = assessment[0]['marine_system'],
        freshwater_system  = assessment[0]['freshwater_system'],
        terrestrial_system = assessment[0]['terrestrial_system'],
        assessor           = assessment[0]['assessor'],
        reviewer           = assessment[0]['reviewer'],
        aoo_km2            = assessment[0]['aoo_km2'],
        eoo_km2            = assessment[0]['eoo_km2'],
        elevation_upper    = assessment[0]['elevation_upper'],
        elevation_lower    = assessment[0]['elevation_lower'],
        depth_upper        = assessment[0]['depth_upper'],
        depth_lower        = assessment[0]['depth_lower'],
        errata_flag        = assessment[0]['errata_flag'],
        errata_reason      = assessment[0]['errata_reason'],
        amended_flag       = assessment[0]['amended_flag'],
        amended_reason     = assessment[0]['amended_reason'],
        habitats           = [dict(h) for h in habitats]
    )
    
    # apply fixes
    if fixElevation:
        tax.fix(fixType = 'elevation')
    if fixHabitats:
        tax.fix(fixType = 'habitats')
    
    #return
    return tax


# HIC SVNT DRACONES