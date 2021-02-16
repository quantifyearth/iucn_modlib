#!/usr/bin/python3


import requests


# api calls

def id_to_assessment(id, token):
    url = 'http://apiv3.iucnredlist.org/api/v3/species/id/{}'.format(str(id))
    payload = {'token':token}
    r = requests.get(url, params=payload)
    return r.json()


def name_to_assessment(name, token):
    url = 'http://apiv3.iucnredlist.org/api/v3/species/{}'.format(str(name))
    payload = {'token':token}
    r = requests.get(url, params=payload)
    return r.json()


def id_to_habitats(id, token):
    url = 'http://apiv3.iucnredlist.org/api/v3/habitats/species/id/{}'.format(str(id))
    payload = {'token':token}
    r = requests.get(url, params=payload)
    return r.json()


def name_to_habitats(name, token):
    url = 'http://apiv3.iucnredlist.org/api/v3/habitats/species/name/{}'.format(str(name))
    payload = {'token':token}
    r = requests.get(url, params=payload)
    return r.json()


def name_to_weblink(name):
    url = 'https://apiv3.iucnredlist.org/api/v3/weblink/{}'.format(str(name))
    r = requests.get(url)
    return r.json()


# custom call manipulations

def id_to_name(id, token):
    j = id_to_assessment(id, token)
    name = j['result'][0]['scientific_name']
    return name


def name_to_assessmentID(name):
    j = name_to_weblink(name)
    weblink = j['rlurl']
    aID = weblink.rsplit('/', 1)[-1]
    return aID


def id_to_assessmentID(id, token):
    name = id_to_name(id, token)
    aID = name_to_assessmentID(name)
    return aID

