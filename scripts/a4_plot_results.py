from pathlib import Path
import argparse,collections,csv,json,statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

parser=argparse.ArgumentParser(description='Reproduce the five report figures from the recorded run and assessment matrices.')
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
parser.add_argument('--out',type=Path)
args=parser.parse_args();root=args.repo.resolve()
def read(p):
    with (root/p).open(newline='') as f:return list(csv.DictReader(f))
runs=read('data/processed/a4-analysis/a4_sample_results_45.csv')
assessment=read('assessment/a4_review_consensus.csv')
controls=read('data/processed/a4-calibration-20261030T103600927206Z/calibration_outcomes.csv')
out=args.out or root/'evidence/a4';out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'serif','font.serif':['Times New Roman','Nimbus Roman'],'font.size':12,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
langs=['python','java','javascript'];labels=['Python','Java','JavaScript'];domains=['database','files','authentication'];colors=['#285F72','#62958E','#BDCFCA']
def save(fig,name):fig.tight_layout(pad=1.1);fig.savefig(out/name);plt.close(fig)
fig,ax=plt.subplots(figsize=(7.2,3.2));bottom=np.zeros(3)
for d,c in zip(domains,colors):
    values=np.array([sum(r['language']==l and r['domain']==d for r in runs) for l in langs])
    ax.bar(labels,values,bottom=bottom,color=c,label=d.capitalize())
    for i,n in enumerate(values):ax.text(i,bottom[i]+n/2,str(n),ha='center',va='center',color='white' if d!='authentication' else '#182E35')
    bottom+=values
ax.set(ylabel='Generated programs',ylim=(0,17),yticks=[0,5,10,15]);ax.legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.5,1.24));save(fig,'figure_01_corpus.png')
values=[[int(r['physical_lines']) for r in runs if r['language']==l] for l in langs]
fig,ax=plt.subplots(figsize=(7.2,3.1));bp=ax.boxplot(values,tick_labels=labels,patch_artist=True,showfliers=True)
for p,c in zip(bp['boxes'],colors):p.set_facecolor(c)
for p in bp['medians']:p.set_color('#182E35')
ax.set_ylabel('Physical source lines');save(fig,'figure_02_source_length.png')
cwes=['CWE-89','CWE-22','CWE-256','CWE-798'];x=np.arange(len(cwes))
neg=[sum(r['cwe']==c and r['verdict']=='0' for r in assessment) for c in cwes]
na=[sum(r['cwe']==c and r['verdict']=='n/a' for r in assessment) for c in cwes]
fig,ax=plt.subplots(figsize=(7.2,3.3));ax.bar(x,neg,color=colors[0],label='Applicable; target not identified');ax.bar(x,na,bottom=neg,color='#DAE3E6',label='Not applicable')
for i in x:ax.text(i,neg[i]/2,str(neg[i]),ha='center',va='center',color='white');ax.text(i,neg[i]+na[i]/2,str(na[i]),ha='center',va='center')
ax.set(xticks=x,xticklabels=cwes,ylabel='Program-category decisions',ylim=(0,49),yticks=[0,15,30,45]);ax.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.01));save(fig,'figure_03_assessment_scope.png')
codes=['PY','JAVA','JS']
m=np.array([[int(next(r['candidate_classification']=='TP' for r in controls if r['target_cwe']==c and r['language']==l and r['expected_positive']=='1')) for l in codes] for c in cwes])
fig,ax=plt.subplots(figsize=(7.2,3.2));ax.imshow(m,cmap=ListedColormap(['#EBD5CB','#C3DCD4']),vmin=0,vmax=1,aspect='auto')
for y in range(4):
    for k in range(3):ax.text(k,y,'Detected' if m[y,k] else 'Missed',ha='center',va='center',color='#182E35')
ax.set(xticks=range(3),xticklabels=labels,yticks=range(4),yticklabels=cwes);ax.tick_params(length=0,pad=8);ax.spines[['left','bottom']].set_visible(False);save(fig,'figure_04_control_coverage.png')
conf=collections.Counter(r['candidate_classification'] for r in controls)
fig,ax=plt.subplots(figsize=(7.2,3.1));ax.barh([1],[conf['TP']],color=colors[0],label='Detected positive');ax.barh([1],[conf['FN']],left=[conf['TP']],color='#C48161',label='Missed positive');ax.barh([0],[conf['TN']],color='#A7C3BA',label='Negative with no target alert')
ax.text(conf['TP']/2,1,str(conf['TP']),ha='center',va='center',color='white');ax.text(conf['TP']+conf['FN']/2,1,str(conf['FN']),ha='center',va='center');ax.text(conf['TN']/2,0,str(conf['TN']),ha='center',va='center')
ax.set(yticks=[0,1],yticklabels=['Negative controls','Positive controls'],xlabel='Control source files',xlim=(0,13),xticks=[0,3,6,9,12]);ax.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.02));save(fig,'figure_05_control_counts.png')
data={'program_counts':{l:{d:sum(r['language']==l and r['domain']==d for r in runs) for d in domains} for l in langs},'source_line_summary':{l:{'n':len(v),'minimum':min(v),'maximum':max(v),'median':statistics.median(v),'sum':sum(v)} for l,v in zip(langs,values)},'positive_control_detected_matrix':m.tolist(),'matrix_rows':cwes,'matrix_columns':codes,'control_confusion':{k:conf[k] for k in ['TP','FN','TN','FP']},'assessment_counts_per_cwe':{c:{'applicable_negative':n,'not_applicable':a,'technical_positive':sum(r['cwe']==c and r['verdict']=='1' for r in assessment)} for c,n,a in zip(cwes,neg,na)}}
(root/'data/processed/a4-analysis/figure_data.json').write_text(json.dumps(data,indent=2)+'\n')
print('Five figures reproduced from the recorded matrices.')
