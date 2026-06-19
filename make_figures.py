"""Figures: all-sector survival curves + AUC comparison."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
M=json.load(open("web_model.json")); C=M["curves"]
plt.rcParams.update({"figure.facecolor":"#070b11","axes.facecolor":"#0f1622","savefig.facecolor":"#070b11",
  "text.color":"#eaf1ff","axes.labelcolor":"#cdd9ef","xtick.color":"#8aa0bf","ytick.color":"#8aa0bf",
  "axes.edgecolor":"#1e2a3e","font.size":10,"axes.titlecolor":"#eaf1ff"})
plt.figure(figsize=(7.6,4.6)); cmap=plt.cm.viridis(np.linspace(0,1,len(C)))
for (name,c),col in zip(C.items(),cmap):
    plt.plot(range(11),c["survival"],color=col,lw=2,label=name.split(" (")[0][:22])
plt.ylim(0,1); plt.xlabel("years since founding"); plt.ylabel("survival probability")
plt.title("Business survival by industry (Weibull fit to BLS anchors)")
plt.legend(fontsize=7,loc="upper right",ncol=2,framealpha=.2); plt.tight_layout()
plt.savefig("fig_survival_curves.png",dpi=120); plt.close()

mm=M["metrics"]; vals=[mm["auc_base"],mm["auc_attr"],mm["auc_full"]]
plt.figure(figsize=(6.4,3.8)); b=plt.bar(["sector\nbase rate","founder/firm\ntraits","base +\ntraits"],vals,color=["#8aa0bf","#5b8cff","#27d08a"])
plt.ylim(0.5,0.7); plt.ylabel("ROC-AUC"); plt.title("Predicting an individual firm: barely above a coin flip")
for bar,v in zip(b,vals): plt.text(bar.get_x()+bar.get_width()/2,v+0.003,f"{v:.3f}",ha="center")
plt.tight_layout(); plt.savefig("fig_auc_comparison.png",dpi=120); plt.close()
print("wrote 2 figures")
