import iucn_modlib


def test_import_json():
    tax = iucn_modlib.TaxonFactoryRedListAPIJsons(
        assessmentJSON = 'tests/data/red_list_api_json_dummy/equus_unicornis_assessment.json',
        habitatsJSON   = 'tests/data/red_list_api_json_dummy/equus_unicornis_habitats.json'
        )
    assert tax.scientific_name == 'Equus unicornis'


def test_import_batch():
    tribble = iucn_modlib.TaxonFactoryRedListBatch(
        species=2345, 
        source='tests/data/red_list_batch_dummy/'
        )
    assert tribble.taxonid == 2345
    assert tribble.scientific_name == "Polygeminus grex"
    assert tribble.main_common_name == "Tribble"
    assert tribble.habitatCodes() == [1.4]
    assert tribble.habitatNames() == ['Silo - grain']
