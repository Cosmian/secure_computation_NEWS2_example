"""national_early_warning_score module."""

from math import inf

def run(data):
    score = 0

    score += compute_one_value({
        (0 , 8  ): 3,
        (9 , 11 ): 1,
        (12, 20 ): 0,
        (21, 24 ): 2,
        (25, inf): 3,
    }, round(data['breaths_per_minute']))

    if data['hypercapnic_respiratory_failure'] == "yes" and data['room_air_or_supplemental_o2'] == "room":
        score += compute_one_value({
            (0 , 83 ): 3,
            (84, 85 ): 2,
            (86, 87 ): 1,
            (88, 100): 0,
        }, round(data['spo2']))
    elif data['hypercapnic_respiratory_failure'] == "yes" and data['room_air_or_supplemental_o2'] == "supplemental":
        score += compute_one_value({
            (0 , 83 ): 3,
            (84, 85 ): 2,
            (86, 87 ): 1,
            (88, 92 ): 0,
            (93, 94 ): 1,
            (95, 96 ): 2,
            (97, 100): 3,
        }, round(data['spo2']))
    elif data['hypercapnic_respiratory_failure'] == "no":
        score += compute_one_value({
            (0 , 91 ): 3,
            (92, 93 ): 2,
            (94, 95 ): 1,
            (96, 100): 0,
        }, round(data['spo2']))

    if data['room_air_or_supplemental_o2'] == "supplemental":
        score += 2
    
    score += compute_one_value({
        (0   , 35 ): 3,
        (35.1, 36 ): 1,
        (36.1, 38 ): 0,
        (38.1, 39 ): 1,
        (39.1, inf): 2,
    }, round(data['temperature'], 1))

    score += compute_one_value({
        (0  , 90 ): 3,
        (91 , 100): 2,
        (101, 110): 1,
        (111, 119): 0,
        (220, inf): 3,
    }, round(data['systolic_bp_mmhg']))

    score += compute_one_value({
        (0  , 40 ): 3,
        (41 , 50 ): 1,
        (51 , 90 ): 0,
        (91 , 110): 1,
        (111, 130): 2,
        (131, inf): 3,
    }, round(data['beats_by_minute']))

    if data['consciousness'] == "no":
        score += 3

    return score


def compute_one_value(ranges, value):
    for (min, max), v in ranges.items():
        if min <= value <= max:
            return v

    return 0