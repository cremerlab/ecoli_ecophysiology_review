#%% Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import seaborn as sns
from scipy.optimize import curve_fit

#%% Define functions

def arrhenius(T,A):
    # Calculates the growth rate based on Arrhenius' law given an input temperature T and factor A (fitted)
    E_activation = 13 # kcal/mol, Knapp et al. review 
    kB = 1.987e-3 # kcal/mol/K, blotzmann constant
    Kelvin_offset = 273.15 # 0 Celsius in Kelvin
    return A*np.exp(-E_activation/(kB*(T+Kelvin_offset))) # growth rate

#%% Define variables

# variable names
vars = ['Temperature','pH','Osmolarity']

# variable units for x axis label
x_label_dict={'Temperature':'Celsius',\
            'pH':'pH',\
            'Osmolarity':'mOsm/kg'}

# Ileocecal ranges
range_var_dict={'Temperature':[35.6,37.3],\
                'pH':[5.8,7.6],\
                'Osmolarity':[287,353]}

# Subplot letters
plot_letter_dict={'Temperature':'A',\
                  'pH':'B',\
                  'Osmolarity':'C'}


# Set up matplotlib params
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial'] + plt.rcParams['font.serif']

# from MoMAColors on Github, Warhol palette
colors=["#d1aac2", "#a5506d", "#db7003", "#fba600", "#f8c1a6", "#A30000","#ff3200", "#011a51", "#97d1d9",  "#916c37"]
# Color dictionary from figure 1
colors_dict = {'upper':'#d4d4d4','stomach':'#b3b3b3','SI':'#eea82d','ileum':'#cf5d3c','cecum':'#8d332a','LI':'#c49f91'}
marker_style=["o", "P", "*", "X", "d", "|", "_"]
palette=[['#d53130','#e35e52','#ef8375','#f8a69a','#fec9c0'],['#ffe401', '#ffec76', '#fff5bc'],['#7d6eeb', '#a496ea', '#c4bfe8']]

#%%

# Plot
plt.figure(figsize=(12,3))
i=1
for var in vars:

    # Import data
    df = pd.read_csv(glob(f'{var}/*processed.csv')[0])

    # Relabel study with spaces
    df['study']=[study.split('_')[0]+' '+study.split('_')[1] for study in df.study.values]

    plt.subplot(1,3,i)
    if var=='Temperature':
        label_range='Ileocecal range'

        # Add Arrhenius growth curve
        x_vals=np.linspace(10,45,100)
        df_arr=df[(df.Celsius>=20)&(df.Celsius<=37)]
        p,cov=curve_fit(arrhenius,df_arr['Celsius'].values,df_arr['growth_rate_hr_norm'].values,p0=1e9)
        plt.plot(x_vals,arrhenius(x_vals,p[0]),'k',zorder=1,label='Arrhenius growth')
        
        # Plot Ileocecal range
        plt.fill_betweenx(y=[-1,2],x1=range_var_dict[var][0],x2=range_var_dict[var][1],color=colors_dict['cecum'],alpha=0.2,label=label_range)
        
        # Plot data from studies
        sns.scatterplot(df,x=x_label_dict[var],y='growth_rate_hr_norm',hue='study',style='study',palette=palette[i-1],edgecolor='k',s=70,markers=marker_style,zorder=0)
        
        plt.ylabel('Rescaled growth rate')
        legend=plt.legend(bbox_to_anchor=(0.5,-0.2),loc='upper center',ncol=2)
    else:
        label_range='_nolegend_'

        # Plot Ileocecal range
        plt.fill_betweenx(y=[-1,2],x1=range_var_dict[var][0],x2=range_var_dict[var][1],color=colors_dict['cecum'],alpha=0.2,label=label_range)
        
        # Plot data from studies
        sns.scatterplot(df,x=x_label_dict[var],y='growth_rate_hr_norm',hue='study',style='study',palette=palette[i-1],edgecolor='k',s=70,markers=marker_style)
        
        plt.ylabel('')
        legend=plt.legend(bbox_to_anchor=(0.5,-0.2),loc='upper center')
    
    # Loop through the auto-generated handles and apply the edge color
    for handle in legend.legend_handles:
        try:
            handle.set_edgecolor('black')
            handle.set_linewidth(0.5)
        except:
            continue
    
    plt.text(-0.13,1.07,plot_letter_dict[var],fontsize=14,transform=plt.gca().transAxes,fontweight="bold",va="bottom",ha="right")
    plt.title(var)
    plt.ylim([-0.05,1.1]) 
    i+=1

# Save figure
plt.savefig('Ecoligy-figure-3.pdf',dpi=1000,bbox_inches="tight")
# %%
