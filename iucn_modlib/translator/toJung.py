#!/usr/bin/python3

from ..classes.IUCNHabitatCodes import IUCNHabitatCodes_v3_1

def toJung(codes):
    '''Translate IUCN habitat codes to Jung habitat codes

    In jung maps, even at level-2, some habitats are coded at level-1 (1100),
    level-2 (1101), or both (1100, 1101) depending on local data precision.
    Therefore the translator allows both to be present and is valid for both
    level-1 and level-2 translation.

        Args:
            codes (str): An IUCN habitat code (str or str- castable), or
                a list or tuple of IUCN habitat codes.
        
        Returns:
            list(int): A list of integers corresponding to Jung level 1 and 2
            codes

        Examples:
            toJung('11')     -> [1100, 1101, 1102, 1103, 1104, 1105, 1106]
            toJung('11.1')   -> [1100, 1101]
            toJung('11.1.1') -> [1100, 1101]
    '''

    # setup IUCNHabitatCodes
    HC = IUCNHabitatCodes_v3_1()
    # define unmappable jung codes
    unmappable = (
        '7', '7.1', '7.2',
        '9.8.1', '9.8.2', '9.8.3', '9.8.4', '9.8.5', '9.8.6',
        '11.1.1', '11.1.2',
        '13', '13.1', '13.2', '13.3', '13.4', '13.5',
        '15', '15.1', '15.2', '15.3', '15.4', '15.5', '15.6', '15.7', '15.8', '15.9', '15.10', '15.11', '15.12', '15.13',
        '16',
        '18'
        )

    # setup empty set
    jungCodes = set()
    # get all codes at level 1
    # this involves casting all species codes at levels 1-3 to level 1
    jungCodes = jungCodes | set([
        int(code.replace('.', '')) * 100
        for code in HC.toLevel(codes, 1)
        ])
    # add all codes at level 2
    # this involves casting all species codes at levels 1-3 to level 2, but some
    # level codes, like '6', cannot be cast to 2 and were already picked up by
    # the previous operation. They also raise an error as they cannot be split
    # by '.', so they are excluded.
    jungCodes = jungCodes | set([
        int(code.split('.')[0]) * 100 + int(code.split('.')[1])
        for code in HC.toLevel(codes, 2) if '.' in code
        ])

    # remove level 1 unmappable codes
    jungCodes = jungCodes - set([
        int(code.replace('.', '')) * 100
        for code in unmappable if '.' not in code
        ])
    # remove level 2 unmappable codes
    # the `code.count('.') == 1` filter matches only level 2 codes
    jungCodes = jungCodes - set([
        int(code.split('.')[0]) * 100 + int(code.split('.')[1])
        for code in unmappable if code.count('.') == 1
        ])
    # no need to remove level 3 unmappable codes as these were never inserted

    # return
    return list(jungCodes)


# HIC SVNT DRACONES