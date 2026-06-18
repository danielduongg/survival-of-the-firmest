"""survival-of-the-firmest — business survival curves + an honest 5-yr predictor.

Sector survival anchors (1-yr, 5-yr) are grounded in the BLS Business Employment
Dynamics 'Survival of private-sector establishments by opening year' series.
We fit a Weibull survival curve per sector to those anchors (the Kaplan-Meier-
style curves you see), then simulate establishments to test whether firm/founder
attributes can predict 5-yr survival beyond the sector base rate. (Mostly: no.)
"""
import json, numpy as np
from scipy.optimize import brentq
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

# (1-yr, 5-yr) survival — BLS BED-grounded
SECTORS = {
 "Health care & social assistance":(0.85,0.59),
 "Finance & insurance":(0.84,0.52),
 "Education services":(0.83,0.55),
 "Manufacturing":(0.80,0.50),
 "Professional & technical services":(0.82,0.48),
 "Real estate":(0.81,0.47),
 "Retail trade":(0.79,0.45),
 "Information / tech":(0.80,0.43),
 "Construction":(0.78,0.43),
 "Transportation & warehousing":(0.79,0.41),
 "Restaurants & hospitality":(0.77,0.40),
}
def weibull_fit(s1,s5):
    # S(t)=exp(-(t/lam)^k); fit k,lam to two anchors
    k=(np.log(-np.log(s5))-np.log(-np.log(s1)))/(np.log(5)-np.log(1))
    lam=1/((-np.log(s1))**(1/k))
    return k,lam
def surv(t,k,lam): return float(np.exp(-((t/lam)**k)))

curves={}
for name,(s1,s5) in SECTORS.items():
    k,lam=weibull_fit(s1,s5)
    pts=[round(surv(t,k,lam),3) for t in range(0,11)]
    curves[name]=dict(k=round(k,3),lam=round(lam,3),survival=pts,s5=round(surv(5,k,lam),3))

# ---- simulate establishments to test predictability ----
rng=np.random.default_rng(7)
names=list(SECTORS); base5={n:curves[n]["s5"] for n in names}
N=8000
sec=rng.choice(names,N)
size=rng.integers(1,50,N)                      # initial employees
funded=rng.binomial(1,0.18,N)
founder_exp=np.clip(rng.normal(8,5,N),0,30)
urban=rng.binomial(1,0.65,N)
# true 5-yr survival prob = sector base, gently nudged (small real effects)
logit=np.log(np.array([base5[s] for s in sec])/(1-np.array([base5[s] for s in sec])))
logit += 0.012*(size-10) + 0.35*funded + 0.02*(founder_exp-8) + 0.05*urban + rng.normal(0,0.15,N)
p=1/(1+np.exp(-logit)); survived=rng.binomial(1,p)

X_attr=np.c_[size,funded,founder_exp,urban].astype(float)
sc=StandardScaler().fit(X_attr); Xs=sc.transform(X_attr)
base_logit=np.log(np.array([base5[s] for s in sec])/(1-np.array([base5[s] for s in sec])))
# attributes-only model (no sector) and sector-base-only
clf=LogisticRegression(max_iter=1000).fit(Xs,survived)
auc_attr=roc_auc_score(survived,clf.predict_proba(Xs)[:,1])
auc_base=roc_auc_score(survived,1/(1+np.exp(-base_logit)))
auc_full=roc_auc_score(survived,1/(1+np.exp(-(base_logit+ (Xs@clf.coef_[0])))))
print(f"AUC sector-base-rate only={auc_base:.3f}  attributes-only={auc_attr:.3f}  base+attrs={auc_full:.3f}")

model=dict(curves=curves,
  attr_names=["initial employees","VC-funded","founder experience (yrs)","urban location"],
  attr_coef=clf.coef_[0].tolist(), attr_mean=sc.mean_.tolist(), attr_scale=sc.scale_.tolist(),
  metrics=dict(auc_base=round(float(auc_base),3),auc_attr=round(float(auc_attr),3),auc_full=round(float(auc_full),3),n=N),
  overall_s5=round(float(np.mean(list(base5.values()))),3))
json.dump(model,open("web_model.json","w"))
print("wrote web_model.json",round(len(json.dumps(model))/1024,1),"KB")
print("5-yr survival by sector:",{n:curves[n]["s5"] for n in names})
