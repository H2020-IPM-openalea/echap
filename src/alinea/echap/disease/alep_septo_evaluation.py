# -*- coding: latin1 -*- 

""" Get simulation outputs of Alep septoria as pandas DataFrames complying with the format generated 
    by readers in 'septo_data_reader' and define comparison methods """

import pandas as pd
import numpy as np
import random as rd
from alinea.alep.disease_outputs import *
from alinea.alep.simulation_tools.simulation_tools import get_data_sim
from alinea.alep.simulation_tools.simulation_tools import plot_by_leaf as plot_by_leaf_sim
#from alinea.alep.simulation_tools.septo_decomposed import run_reps_septo
from alinea.echap.disease.septo_data_reader import *
from alinea.echap.disease.septo_data_treatment import *
from alinea.echap.disease.septo_data_treatment import *
    
# Run simulations ###########################################################################
# TODO strategy for multiprocessing if focus on one variety

def get_year_sowing_date(variety='Tremie12'):
    if variety in ['Mercia', 'Rht3']:
        year = 2011
        sowing_date = '10-15'
    elif variety=='Tremie12':
        year = 2012
        sowing_date = '10-21'
    elif variety=='Tremie13':
        year = 2013
        sowing_date = '10-29'
    return year, sowing_date
    
def run_simu(variety = 'Tremie12', nplants = 15, 
             sporulating_fraction=5e-3, nreps=5, 
             nsect = 7, layer_thickness = 0.01, **kwds):
    year, sowing_date = get_year_sowing_date(variety=variety)
    run_reps_septo(year=year, variety=variety,
                   sowing_date=sowing_date,
                   nplants=nplants, nsect=nsect,
                   sporulating_fraction=sporulating_fraction,
                   layer_thickness=layer_thickness, 
                   nreps=nreps, **kwds)
    
def organize_fnl(df_sim):
    """ Trick to give same plant number to plants with same fnl """
    df_sim['num_plant'] *= 10**(df_sim['rep'])
    fnls = {}
    df = df_sim[df_sim['rep']==0]
    for pl in set(df['num_plant']):
        fnls[pl] = np.unique(df[df['num_plant']==pl]['fnl'])[0]
    for rep in set(df_sim['rep']):
        if rep>0:
            fnls_tmp = {}
            df = df_sim[df_sim['rep']==rep]
            for pl in set(df['num_plant']):
                fnls_tmp[pl] = np.unique(df[df['num_plant']==pl]['fnl'])[0]
            
            for k, v in fnls.iteritems():
                new_num = None
                it = fnls_tmp.iteritems()
                while new_num is None:
                    kk, vv = next(it)
                    if vv == v:
                        new_num = k
                        fnls_tmp.pop(kk)
                        df_sim.loc[df_sim['num_plant']==kk, 'num_plant'] = new_num
    return df_sim
    
def get_mean_data_sim(df_sim):
    df_sim = organize_fnl(df_sim)
    df = df_sim.reset_index()
    df = df.groupby(['date', 'num_plant', 'num_leaf_bottom']).mean()
    df = df.reset_index()
    df['variety'] = np.unique(df_sim['variety'])[0]
    df['axis'] = 'MS'
    df['severity'] *= 100
    df['severity_on_green'] *= 100
    df = df.set_index('date')
    return df

def get_aggregated_data_sim(variety = 'Tremie12', nplants = 15, 
                            sporulating_fraction=5e-3, 
                            num_leaf = 'num_leaf_top', suffix=None, 
                            forced_year=None):
    if forced_year is None:
        year, sowing_date = get_year_sowing_date(variety=variety)
    else:
        year = forced_year
    data_sim = get_data_sim(fungus='septoria', year=year,
                            variety=variety, nplants=nplants,
                            inoc=sporulating_fraction, suffix=suffix)
    data_sim = get_data_without_death(data_sim, num_leaf=num_leaf)
    data_sim['severity'] *= 100
    data_sim['severity_on_green'] *= 100
    return data_sim

# Data manipulation on results of simulation #######################################################
def get_mean_one_leaf_sim(df, variable = 'severity', xaxis = 'degree_days',
                          num_leaf = 1, from_top = True):
    """ Get average of input variable on input leaf over all plants in simulated canopy """
    if from_top == True:
        df = df[df['num_leaf_top'] == num_leaf]
    else:
        df = df[df['num_leaf_bottom'] == num_leaf]
    if xaxis in ['date', 'degree_days']:
        return df.groupby(xaxis).mean()[variable]
    elif xaxis in ['age_leaf', 'age_leaf_lig', 'age_leaf_vs_flag_lig']:
        df_mean = df.groupby('degree_days').mean()[variable]
        df_dates = get_df_dates_xaxis(df, xaxis)
        df_mean.index -= df_dates.loc[num_leaf, xaxis]
        return df_mean

def get_df_mean_sim(data_sim, variable = 'severity', xaxis = 'degree_days', leaves = range(1,14)):
    """ Get average for given variable over xaxis for all given leaves """
    dfs = []
    for lf in leaves:
        df_mean_lf = get_mean_one_leaf_sim(data_sim, variable = variable, 
                                            xaxis = xaxis, num_leaf = lf, from_top = True)
        df_mean_lf = df_mean_lf.to_frame()
        df_mean_lf.columns = [lf]
        dfs.append(df_mean_lf)
    return pd.concat(dfs, axis = 1)
    
def get_mean_rmse(df_mean_obs, df_mean_sim, num_leaf):
    """ Get mean RMSE between observation data and simulation results """
    notnull_obs = df_mean_obs[num_leaf][df_mean_obs[num_leaf].notnull()]
    nearest_sim = [df_mean_sim[num_leaf].iloc[np.abs(np.array(df_mean_sim.index) - ind).argmin()] 
                    for ind in notnull_obs.index]
    return numpy.sqrt(((nearest_sim - notnull_obs) ** 2).mean())
    
# Compare observations and simulations #############################################################
def plot_one_leaf_sim(data_sim, variable = 'severity', xaxis = 'degree_days',
                      num_leaf = 1, from_top = True, ax = None, return_df_mean = True,
                      color = 'r', linestyle = '-', marker = ''):
    """ Plot input variable versus input axis """
    if ax is None:
        fig, ax = plt.subplots(1)
    df_mean_sim = get_mean_one_leaf_sim(df = data_sim, variable = variable, xaxis = xaxis,
                                        num_leaf = num_leaf, from_top = from_top)
    ax.plot(df_mean_sim.index, df_mean_sim, 
            color = color, linestyle = linestyle, marker = marker)
    if return_df_mean == True:
        return df_mean_sim

def plot_mean_by_leaf_sim(data_sim, variable = 'severity', leaves = range(1,14), 
                          xaxis = 'degree_days', ax = None, xlims = None,
                          ylims = None, ylabel = 'Severity', xlabel = 'Degree Days',
                          fig_size = (8,6), grid = True):
    """ Plot average of given variable on given separate leaves for all plants """    
    df_mean = get_df_mean_sim(data_sim, variable = variable, xaxis = xaxis, leaves = leaves)
    if ax == None:
        fig, ax = plt.subplots(1, figsize = fig_size)
    for leaf in df_mean.columns:
        x_data = df_mean.index[~np.isnan(df_mean.ix[:,leaf])]
        ax.plot(x_data, df_mean.loc[:, leaf][~np.isnan(df_mean.ix[:,leaf])])
    
    # Customize plot
    if ylims is not None:
        ax.set_ylim(ylims)
    if xlims is not None:
        ax.set_xlim(xlims)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize = 18)
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize = 18)
    if grid == True:
        ax.grid()
    ax.legend(leaves, title = 'Leaf\nnumber', loc='center left', bbox_to_anchor=(1, 0.5))
    
def plot_comparison_confidence_and_boxplot_sim_obs(data_obs, data_sim,
                                                    weather, variable='severity', 
                                                    xaxis = 'degree_days', 
                                                    leaves = range(1,7), 
                                                    xlims = [1100, 2500], 
                                                    display_rmse = False):
    df_mean_obs, df_low, df_high, fig, axs = plot_confidence_and_boxplot(data_obs, weather, leaves = leaves,
                                                                         variable = variable, xaxis = xaxis,
                                                                         xlims = xlims, return_fig = True)
    if variable == 'septo_green':
        variable = 'severity_on_green'
    df_mean_sim = get_mean(data_sim, column = variable, xaxis = xaxis)
    for i, ax in enumerate(axs.flat):
        leaf = i+1
        if leaf in leaves:
            x_data = df_mean_sim.index[~np.isnan(df_mean_sim.ix[:,leaf])]
            ax.plot(x_data, df_mean_sim.loc[:, leaf][~np.isnan(df_mean_sim.ix[:,leaf])], 'r')
            if display_rmse == True:
                ax.annotate('RMSE : %.2f' %get_mean_rmse(df_mean_obs, df_mean_sim, num_leaf = leaf), xy=(0.05, 0.75),
                            xycoords='axes fraction', fontsize=14)
                            
def plot_one_sim(data_sim, variable, xaxis, axs, leaves, color, xlims=None,
                 linestyle='-', linewidth=1):
    df_mean_sim = get_mean(data_sim, column = variable, xaxis = xaxis)
    for i, ax in enumerate(axs.flat):
        if i < len(leaves):
            leaf = leaves[i]
            x_data = df_mean_sim.index[~np.isnan(df_mean_sim.ix[:,leaf])]
            ax.plot(x_data, df_mean_sim.loc[:, leaf][~np.isnan(df_mean_sim.ix[:,leaf])], 
                    color=color, linestyle=linestyle, linewidth=linewidth)
            if xlims is not None:
                ax.set_xlim(xlims)