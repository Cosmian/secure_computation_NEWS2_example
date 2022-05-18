from national_early_warning_score import run

score = run({
    'breaths_per_minute': 13,
    'hypercapnic_respiratory_failure': "yes",
    'spo2': 84,
    'room_air_or_supplemental_o2': "room",
    'temperature': 38,
    'systolic_bp_mmhg': 80,
    'beats_by_minute': 45,
    'consciousness': "yes",
})


print(score)
