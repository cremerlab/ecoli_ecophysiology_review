#%%

# import modules
import pandas as pd
import numpy as np

# import data
df = pd.read_csv('Growth_rate_vs_pH.csv')

# Convert different growth rate units to hr^-1
df.loc[df.study=='Gale_1942','growth_rate_hr']=np.log(2)/(df.loc[df.study=='Gale_1942','dbl_time_min']/60)
df.loc[df.study=='Stancik_2002','growth_rate_hr']=df.loc[df.study=='Stancik_2002','generation_hr']*np.log(2)

# Rescale growth rate values by the maximum growth rate observed in each study
df['growth_rate_hr_norm']=np.nan
for g,d in df.groupby('study'):
    df.loc[df.study==g,'growth_rate_hr_norm']=d['growth_rate_hr']/d['growth_rate_hr'].max()

# Save processed data
df.to_csv('Growth_rate_vs_pH_processed.csv')
# %%
