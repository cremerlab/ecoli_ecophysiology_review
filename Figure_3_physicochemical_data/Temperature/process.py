# %%

# Import modules
import pandas as pd
import numpy as np

# Import data
df = pd.read_csv('Growth_rate_vs_Temp.csv')

# Convert temperature to Celsius
df.loc[df.study=='Farewell_1998','Celsius']=1/(df.loc[df.study=='Farewell_1998','temp_inverse_K']) - 273

# Rescale growth rate values by the maximum growth rate observed in each study
df['growth_rate_hr_norm']=np.nan
for g,d in df.groupby('study'):
    df.loc[df.study==g,'growth_rate_hr_norm']=d['growth_rate_hr']/d['growth_rate_hr'].max()

# Save processed data
df.to_csv('Growth_rate_vs_Temp_processed.csv')
# %%
