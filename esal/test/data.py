# Common test data
#
# Copyright (c) 2015 Aubrey Barnard.  This is free software.  See
# LICENSE for details.

import itertools as itools

from .. import events


# Raw tuples for binary events in "data order"
binary_event_tuples = (
    # Sequence 0 length 0

    # Single event
    (1, 0, 'a'),

    # Same event, same time
    (2, 0, 'a'), # 1
    (2, 0, 'a'),

    # Same event, different times
    (3, 0, 'a'), # 3
    (3, 1, 'a'),

    # Different events, same time
    (4, 0, 'a'), # 5
    (4, 0, 'b'),

    # Different events, different times
    (5, 0, 'a'), # 7
    (5, 1, 'b'),

    # Full unique sequence
    (6, 0, 'a'), # 9
    (6, 1, 'b'),
    (6, 2, 'c'),
    (6, 3, 'd'),
    (6, 4, 'e'),
    (6, 5, 'f'),

    # Multiple events every time
    (7, 0, 'a'), # 15
    (7, 0, 'b'),
    (7, 0, 'c'),
    (7, 1, 'a'),
    (7, 1, 'b'),
    (7, 1, 'c'),
    (7, 1, 'd'),
    (7, 2, 'a'),
    (7, 2, 'b'),
    (7, 3, 'a'),
    (7, 3, 'b'),
    (7, 3, 'c'),
    (7, 3, 'd'),
    (7, 3, 'e'),

    # Unsorted
    (8, 0, 'a'), # 29
    (8, 4, 'd'),
    (8, 4, 'a'),
    (8, 3, 'e'),
    (8, 0, 'b'),
    (8, 9, 'f'),
    (8, 0, 'b'),
    (8, 1, 'a'),
    (8, 4, 'e'),
    (8, 2, 'f'),
    (8, 3, 'e'),

    # Sorted version of above
    (9, 0, 'a'), # 40
    (9, 0, 'b'),
    (9, 0, 'b'),
    (9, 1, 'a'),
    (9, 2, 'f'),
    (9, 3, 'e'),
    (9, 3, 'e'),
    (9, 4, 'a'),
    (9, 4, 'd'),
    (9, 4, 'e'),
    (9, 9, 'f'),

    # Random 1, length 8
    # {1:(e,f), 4:(d,f,f), 5:(b,a), 9:f}
    (6741, 1, 'e'), # 51
    (6741, 1, 'f'),
    (6741, 4, 'd'),
    (6741, 4, 'f'),
    (6741, 4, 'f'),
    (6741, 5, 'b'),
    (6741, 5, 'a'),
    (6741, 9, 'f'),

    # Random 2, length 15
    # {0:c, 1:d, 2:c, 4:f, 5:(c,b,d,c), 6:(a,e), 8:(c,b,a), 9:(b,a)}
    (4594, 0, 'c'), # 59
    (4594, 1, 'd'),
    (4594, 2, 'c'),
    (4594, 4, 'f'),
    (4594, 5, 'c'),
    (4594, 5, 'b'),
    (4594, 5, 'd'),
    (4594, 5, 'c'),
    (4594, 6, 'a'),
    (4594, 6, 'e'),
    (4594, 8, 'c'),
    (4594, 8, 'b'),
    (4594, 8, 'a'),
    (4594, 9, 'b'),
    (4594, 9, 'a'),

    # Random, unsorted events for selection, length 20
    # >>> (random.randrange(10), random.randrange(10), random.choice('abcdef'))
    (5, 0, 'b'), # 74
    (1, 3, 'a'),
    (4, 3, 'a'),
    (5, 1, 'd'),
    (6, 7, 'e'),
    (6, 1, 'f'),
    (5, 4, 'a'),
    (0, 1, 'a'),
    (0, 8, 'e'),
    (1, 0, 'a'),
    (7, 6, 'b'),
    (1, 0, 'e'),
    (6, 3, 'e'),
    (1, 8, 'd'),
    (3, 3, 'f'),
    (3, 3, 'e'),
    (1, 3, 'c'),
    (6, 8, 'e'),
    (4, 1, 'e'),
    (9, 7, 'd'),
) # 94

# Event tuples for binary events
binary_events = tuple(
    map(lambda tup: events.Event(seq=tup[0], time=tup[1], ev=tup[2]),
        binary_event_tuples))

# Specific event sequences to be used in preference to indexing events
seq_len1 = binary_events[0:1]
seq_abcdef = binary_events[9:15]
seq_concurrent_events = binary_events[15:29]
seq_unsorted = binary_events[29:40]
seq_sorted = binary_events[40:51]
seq_rand1_08 = binary_events[51:59]
seq_rand2_15 = binary_events[59:74]
evs_for_selection = binary_events[74:94]

# Drug and condition events for example medical data
drugs = (
    'd_ace_inhibitor',
    'd_amphotericin_b',
    'd_antibiotic',
    'd_antiepileptic',
    'd_benzodiazepine',
    'd_beta_blocker',
    'd_bisphosphonate',
    'd_rofecoxib',
    'd_tricyclic_antidepressant',
    'd_typical_antipsychotic',
    'd_warfarin',
)
conds = (
    'c_angioedema',
    'c_aplastic_anemia',
    'c_acute_liver_failure',
    'c_acute_renal_failure',
    'c_bleeding',
    'c_hip_fracture',
    'c_mi',
    'c_death_after_mi',
    'c_thrombosis',
    'c_upper_gi_ulcer',
)

# Example medical events data (patient-id, datetime, duration, event,
# state).  State would normally always be true for observations of
# binary-valued events, but I've added variety.  The states can be
# interpreted as observed to be true, observed to be false (absent), and
# unobserved (None).
#
# >>> [(random.randrange(10), random.uniform(2004.0, 2010.0), random.randrange(360), random.choice(drugs + conds), random.choice((True, True, True, False, None))) for i in range(100)]
med_event_tuples = (
    (5, 2005.3332745463497, 336, 'c_mi', True),
    (7, 2009.4113006002851, 254, 'd_amphotericin_b', True),
    (0, 2009.6693668064265, 171, 'c_aplastic_anemia', True),
    (4, 2009.6566494692959, 236, 'c_acute_liver_failure', None),
    (8, 2007.5532928951857, 197, 'c_bleeding', None),
    (6, 2007.5112378468978,  89, 'c_hip_fracture', None),
    (0, 2004.1344775666760, 234, 'c_upper_gi_ulcer', False),
    (4, 2008.3805326283791, 212, 'd_benzodiazepine', True),
    (0, 2007.3088140421100, 243, 'd_antiepileptic', True),
    (3, 2009.6675945975064, 191, 'c_angioedema', None),
    (9, 2009.4179744938078, 281, 'd_benzodiazepine', True),
    (1, 2009.4820034980016, 356, 'c_acute_renal_failure', True),
    (3, 2006.5025913849706, 246, 'c_hip_fracture', True),
    (3, 2004.4252999731070,  70, 'd_ace_inhibitor', False),
    (4, 2008.8598874955567,  49, 'c_bleeding', False),
    (6, 2005.6059077185855, 106, 'd_typical_antipsychotic', False),
    (9, 2009.3085019898756,  49, 'd_beta_blocker', True),
    (6, 2007.2051182932805,  29, 'c_angioedema', True),
    (3, 2004.6538474460613, 243, 'c_death_after_mi', True),
    (6, 2009.0460491635836, 357, 'd_ace_inhibitor', True),
    (1, 2005.9831341939494, 302, 'd_ace_inhibitor', False),
    (0, 2005.7490747246877, 178, 'd_beta_blocker', False),
    (3, 2006.0348299735340,  98, 'c_thrombosis', None),
    (0, 2004.2930682152503, 306, 'c_mi', False),
    (3, 2009.6534688666572, 114, 'd_tricyclic_antidepressant', True),
    (7, 2008.4087370118657, 303, 'c_bleeding', None),
    (0, 2004.8438259854040, 175, 'd_bisphosphonate', True),
    (6, 2005.3031178066450, 345, 'c_death_after_mi', True),
    (4, 2004.8116324195530, 171, 'd_benzodiazepine', True),
    (6, 2006.6086582446580, 100, 'd_antibiotic', True),
    (6, 2008.9020193708247, 272, 'd_beta_blocker', True),
    (6, 2006.1802628640899, 208, 'd_bisphosphonate', None),
    (8, 2004.4641903073273, 293, 'c_bleeding', True),
    (7, 2009.2583315827196, 300, 'c_death_after_mi', False),
    (5, 2006.1315252946108, 137, 'c_upper_gi_ulcer', False),
    (7, 2008.3969462511034, 179, 'c_death_after_mi', True),
    (5, 2007.1295801931808, 124, 'd_beta_blocker', False),
    (1, 2005.8250680259634, 173, 'd_amphotericin_b', True),
    (8, 2007.7476076474540, 181, 'c_mi', True),
    (6, 2007.0484706552230, 223, 'c_upper_gi_ulcer', True),
    (2, 2007.7834788406813, 103, 'c_acute_renal_failure', False),
    (4, 2004.2650298112253, 198, 'd_antibiotic', False),
    (2, 2009.6754954140822,  96, 'd_typical_antipsychotic', True),
    (0, 2009.8129931224557, 163, 'd_rofecoxib', True),
    (1, 2007.0589671799020, 344, 'd_rofecoxib', True),
    (8, 2009.8719591211996, 269, 'c_hip_fracture', True),
    (6, 2007.4955568157418, 257, 'd_ace_inhibitor', False),
    (4, 2005.1199312650213, 142, 'd_beta_blocker', None),
    (7, 2008.1137872447428, 240, 'd_antiepileptic', True),
    (0, 2004.9610834879416, 318, 'c_mi', True),
    (3, 2006.3341818104423, 211, 'c_bleeding', None),
    (9, 2005.5952095414964, 275, 'd_antibiotic', None),
    (4, 2008.0033894769124, 133, 'c_acute_liver_failure', True),
    (6, 2009.1604219576610, 232, 'd_typical_antipsychotic', True),
    (9, 2008.3046196668852, 229, 'd_rofecoxib', False),
    (4, 2009.1303507822130, 135, 'c_hip_fracture', True),
    (0, 2007.0803917293170, 218, 'c_acute_liver_failure', True),
    (5, 2007.4950038347326, 355, 'c_aplastic_anemia', True),
    (1, 2007.2699297048710,  37, 'd_typical_antipsychotic', False),
    (8, 2005.6347186759415, 359, 'd_typical_antipsychotic', False),
    (3, 2007.7967146349251, 219, 'd_rofecoxib', None),
    (1, 2006.0581851728723, 334, 'd_rofecoxib', True),
    (4, 2009.2829977644194,  66, 'c_aplastic_anemia', False),
    (6, 2004.4083938080412,  85, 'c_thrombosis', True),
    (0, 2006.9933632256200, 218, 'c_thrombosis', True),
    (1, 2007.3359932473843, 275, 'd_ace_inhibitor', False),
    (7, 2009.1823316856378, 131, 'd_antibiotic', True),
    (7, 2005.8146689101081, 274, 'd_benzodiazepine', True),
    (9, 2005.6885677282460, 223, 'd_rofecoxib', True),
    (8, 2006.7905425356084, 291, 'd_antiepileptic', True),
    (0, 2004.1823066924650, 199, 'c_death_after_mi', True),
    (1, 2006.8433625103664, 228, 'd_antiepileptic', None),
    (7, 2005.4767294386797, 197, 'c_hip_fracture', False),
    (2, 2008.1695651899206, 352, 'd_warfarin', True),
    (8, 2008.0477694365666, 137, 'd_antiepileptic', True),
    (3, 2009.1518974465762, 196, 'd_warfarin', True),
    (9, 2006.9016401006740, 211, 'c_acute_liver_failure', False),
    (3, 2009.5107557891602, 282, 'c_upper_gi_ulcer', True),
    (4, 2005.0803410918760, 107, 'd_amphotericin_b', True),
    (9, 2009.9497198552497, 337, 'd_antibiotic', False),
    (1, 2006.0332193337065,  49, 'd_ace_inhibitor', False),
    (9, 2009.9133471629430, 235, 'c_upper_gi_ulcer', True),
    (7, 2004.5460017954450, 189, 'd_rofecoxib', False),
    (0, 2006.8806369589706, 307, 'c_thrombosis', True),
    (6, 2005.9682710420348, 163, 'c_acute_liver_failure', True),
    (7, 2005.2254370184628,  60, 'd_ace_inhibitor', None),
    (6, 2007.2142245652628, 240, 'c_acute_liver_failure', None),
    (0, 2004.0022596528395, 271, 'c_upper_gi_ulcer', False),
    (8, 2007.3561708632415, 273, 'c_hip_fracture', False),
    (7, 2006.2915087944675, 198, 'd_ace_inhibitor', True),
    (5, 2007.0676303628993, 270, 'd_beta_blocker', False),
    (5, 2004.2195192654463, 258, 'c_thrombosis', False),
    (8, 2007.0133637769313,  27, 'c_acute_liver_failure', True),
    (7, 2009.8034295926834, 294, 'c_upper_gi_ulcer', True),
    (0, 2004.6174141502584, 345, 'd_tricyclic_antidepressant', True),
    (2, 2005.7923497956665, 280, 'd_tricyclic_antidepressant', None),
    (8, 2008.2963937793882,  92, 'd_amphotericin_b', None),
    (6, 2006.4040261221346, 158, 'c_death_after_mi', True),
    (7, 2007.9416342372140,  47, 'd_benzodiazepine', True),
    (6, 2005.2507518364293,  92, 'c_angioedema', None),
)
med_events = tuple(map(lambda t: events.Event(*t), med_event_tuples))
