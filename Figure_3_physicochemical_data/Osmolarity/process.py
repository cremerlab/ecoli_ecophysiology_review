#%% 

# Import modules
import pandas as pd
import numpy as np

# Import raw data
df=pd.read_csv('Growth_rate_vs_Osm.csv')

# Offset values for each media

# LB offset: Pilizota_2014, DOI: 10.1016/j.bpj.2014.08.025
# M9 glycerol offset: based on M9 recipe +0.01 for 0.1% glycerol
Osm_offset_dict = {'LB':0.44,'M9_glycerol' :0.26} 

# Add osmolarity offset for each media type
for media in ['LB','M9_glycerol']:
    df.loc[df.media==media,'Osm/kg']= df[df.media==media]['Osm/kg']+Osm_offset_dict[media]

# Rescale growth rate values by the maximum growth rate observed in each study
df['growth_rate_hr_norm']=np.nan
for g,d in df.groupby('study'):
    df.loc[df.study==g,'growth_rate_hr_norm']=d['growth_rate_hr']/d['growth_rate_hr'].max()

# Calculate millisomolar
df['mOsm/kg']=1e3*df['Osm/kg']

# Save processed data
df.to_csv('Growth_rate_vs_Osm_processed.csv')
#%%