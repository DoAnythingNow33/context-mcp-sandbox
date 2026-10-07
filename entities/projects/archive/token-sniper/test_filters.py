"""Offline checks: the v1 false positives must now be rejected by Layer 2."""
from filters.momentum_filter import MomentumFilter
from filters.spam_filter import SpamFilter

mf = MomentumFilter()

CASES = {
    # from the v2 plan's "why v1 fails" table
    "beanly":  dict(buys_m5=1890, sells_m5=32,  volume_m5_usd=90000, lp_size_usd=6000,
                    price_change_percent_2min=15, holder_count=18, has_twitter=False),
    "USMS":    dict(buys_m5=495,  sells_m5=6,   volume_m5_usd=40000, lp_size_usd=5000,
                    price_change_percent_2min=1.4, holder_count=12, has_twitter=False),
    "MRHATE":  dict(buys_m5=2612, sells_m5=885, volume_m5_usd=250000, lp_size_usd=5000,
                    price_change_percent_2min=42, holder_count=40, has_twitter=False),
    "Rabbit":  dict(buys_m5=1634, sells_m5=1086, volume_m5_usd=120000, lp_size_usd=8000,
                    price_change_percent_2min=-34, holder_count=55, has_twitter=True, has_website=True),
    # a synthetic "healthy" token: real 2-sided flow, sane vol/liq, real holders
    "GOODCOIN": dict(buys_m5=140, sells_m5=70, volume_m5_usd=45000, lp_size_usd=120000,
                     price_change_percent_2min=12, holder_count=220, has_twitter=True, has_website=True),
}

print("=== Layer 2 (momentum / wash) ===")
for name, d in CASES.items():
    d["token_symbol"] = name
    passed, score, det = mf.evaluate(d)
    print(f"{name:9} passed={passed!s:5} score={score:3}  {det['checks_failed'] or 'OK'}")

print("\n=== Layer 3 (ticker farm) ===")
sf = SpamFilter(symbol_farm_max_repeats=3)
rc_ok = {"score": 100, "score_normalised": 10, "risks": []}
for i in range(5):
    passed, det = sf.check("USMS", rc_ok, {"creator_holds": None}, now=1000 + i)
    print(f"USMS relaunch #{i+1}: passed={passed!s:5} {det['checks_failed'] or 'OK'}")

# rugcheck hard fail
p, det = sf.check("XYZ", {"score": 900, "score_normalised": 80, "risks": []}, {})
print(f"high-rugcheck: passed={p} {det['checks_failed']}")
