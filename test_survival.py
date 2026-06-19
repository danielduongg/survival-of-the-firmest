import json
M=json.load(open("web_model.json")); C=M["curves"]

def test_curves_monotonic_decreasing():
    for name,c in C.items():
        s=c["survival"]
        assert s[0]==1.0
        assert all(s[i]>=s[i+1] for i in range(len(s)-1))

def test_five_year_survival_realistic():
    for name,c in C.items():
        assert 0.35 <= c["s5"] <= 0.62      # BLS-grounded range

def test_ci_band_brackets_curve():
    for name,c in C.items():
        for lo,s,hi in zip(c["ci_lo"],c["survival"],c["ci_hi"]):
            assert lo-1e-9 <= s <= hi+1e-9

def test_base_rate_dominates_prediction():
    m=M["metrics"]
    assert m["auc_full"] < 0.65          # individual prediction is weak
    assert m["auc_full"] >= m["auc_base"]
