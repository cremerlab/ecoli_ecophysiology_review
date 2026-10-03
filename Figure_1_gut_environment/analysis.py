#%%

# Import modules

import numpy as np
import pandas as pd

#%%

# Import raw data
df=pd.read_csv('flow_abundance_data.csv')

# Calculate total flow rate through compartments (L/day) as the cummulation sum of flow changes along the digestive tract
df['flow_rate_L_day']=[df['flow_rate_change_L_day'][:i].sum() for i in range(len(df))]

# Calculate coliform densities
L_to_mL_conversion=1e3
df['coliform_passage_log_CFU_day']=np.log10(L_to_mL_conversion*df['flow_rate_L_day']*10**(df['coliform_density_log_CFU_mL']))

# Save analysis
df.to_csv('flow_abundance_data_analyzed.csv')

# Create subset of data for density increase analysis
positions=['Ileum','Cecum','Feces']
df_subset=df[df.gut_location.isin(positions)].reset_index()

# Calculate changes coliform densities between compartments
df_subset['coliform_density_increase_log2']=np.log2(np.append([np.nan],[10**df_subset['coliform_density_log_CFU_mL'][i+1]/10**df_subset['coliform_density_log_CFU_mL'][i] for i in range(len(df_subset)-1)]))

# Calculate increase in density due to microbial growth
df_subset['coliform_density_increase_from_growth_log2']=np.log2(np.append([np.nan],[10**df_subset['coliform_passage_log_CFU_day'][i+1]/10**df_subset['coliform_passage_log_CFU_day'][i] for i in range(len(df_subset)-1)]))

# Infer increase in density due to water reuptake
df_subset['coliform_density_increase_from_water_reuptake_log2']=df_subset['coliform_density_increase_log2']-df_subset['coliform_density_increase_from_growth_log2']

# Save analysis
df_subset.to_csv('flow_abundance_data_subset_analyzed.csv')
# %%
