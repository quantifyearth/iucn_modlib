"""Module to facilitate the extraction of model parameters and data for the
development of habitat suitability models."""


__title__ = 'iucn-modlib'
__version__ = '0.1'
__author__ = 'Daniele Baisero'
__license__ = """ISC License

Copyright 2022 Daniele Baisero <daniele.baisero@gmail.com>

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE."""
__copyright__ = 'Copyright 2022 Daniele Baisero <daniele.baisero@gmail.com>'


from .classes.Taxon import Taxon
from .classes.HabitatFilters import HabitatFilters
from .factories.TaxonFactories import TaxonFactoryRedListAPI, TaxonFactoryRedListAPIJsons, TaxonFactoryRedListBatch
from .factories.HabitatFiltersFactories import HabitatFiltersFactory
from .classes.IUCNHabitatCodes import IUCNHabitatCodes_v3_1
from . import translator

