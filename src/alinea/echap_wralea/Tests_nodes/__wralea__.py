
# This file has been generated at Mon Jul 15 16:17:12 2013

from openalea.core import *


__name__ = 'Alinea.Echap.Tests_nodes'

__editable__ = True
__description__ = ''
__license__ = 'CeCILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__alias__ = []
__version__ = '0.8.0'
__authors__ = ''
__institutes__ = ''
__icon__ = ''


__all__ = ['tests_nodes_plot_DU', 'tests_nodes_sum_temp_global', 'tests_nodes_plot_lesions', 'tests_nodes_update_no_doses', 'tests_nodes_compounds_from_csv', 'tests_nodes_products_from_csv', 'tests_nodes_set_initial_properties_g', 'tests_nodes_plot_pesticide', 'tests_nodes_generate_scene', 'tests_nodes_wheat_mtg']



tests_nodes_plot_DU = Factory(name='plot_DU',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='plot_DU',
                inputs=[{'interface': None, 'name': 'g', 'value': None, 'desc': ''}],
                outputs=[],
                widgetmodule=None,
                widgetclass=None,
               )




tests_nodes_sum_temp_global = Factory(name='sum_temp_global',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='sum_temp_global',
                inputs=[{'interface': None, 'name': 'g', 'value': None, 'desc': ''}, {'interface': None, 'name': 'globalclimate', 'value': None, 'desc': 'Pandas dataframe with global climate for the time step'}],
                outputs=[{'interface': None, 'name': 'g', 'desc': 'MTG with the sum of temperature at the plant scale'}],
                widgetmodule=None,
                widgetclass=None,
               )




tests_nodes_plot_lesions = Factory(name='plot_lesions',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='plot_lesions',
                inputs=[{'interface': None, 'name': 'g', 'value': None, 'desc': ''}],
                outputs=[],
                widgetmodule=None,
                widgetclass=None,
               )




tests_nodes_update_no_doses = Factory(name='update_no_doses',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='update_no_doses',
                inputs=[{'interface': None, 'name': 'g', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'label', 'value': 'LeafElement', 'desc': ''}],
                outputs=[{'interface': None, 'name': 'g', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




tests_nodes_compounds_from_csv = Factory(name='compounds_from_csv',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='compounds_from_csv',
                inputs=[{'interface': IData, 'name': 'csvname', 'value': None, 'desc': ''}],
                outputs=[{'interface': IDict, 'name': 'compound_dict', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




tests_nodes_products_from_csv = Factory(name='products_from_csv',
                authors=' (wralea authors)',
                description='Read a products names csv file and convert it to a dict',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='products_from_csv',
                inputs=[{'interface': IData, 'name': 'csvname', 'value': None, 'desc': ''}],
                outputs=[{'interface': IDict, 'name': 'product_dict', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




tests_nodes_set_initial_properties_g = Factory(name='set_initial_properties_g',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='set_initial_properties_g',
                inputs=[{'interface': None, 'name': 'g', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'surface_leaf_element', 'value': 5., 'desc': ''}, {'interface': None, 'name': 'position_senescence', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'label', 'value': 'LeafElement', 'desc': ''}],
                outputs=[{'interface': None, 'name': 'g', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




tests_nodes_plot_pesticide = Factory(name='plot_pesticide',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='plot_pesticide',
                inputs=[{'interface': None, 'name': 'g', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




tests_nodes_generate_scene = Factory(name='generate_scene',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='generate_scene',
                inputs=[{'interface': None, 'name': 'g', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'g', 'desc': ''}, {'interface': None, 'name': 'scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




tests_nodes_wheat_mtg = Factory(name='Adel_mtg2',
                authors=' (wralea authors)',
                description='Create a less simple mtg',
                category='Unclassified',
                nodemodule='alinea.echap.tests_nodes',
                nodeclass='wheat_mtg',
                inputs=[{'interface': IInt, 'name': 'nb_sect', 'value': 1, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'g', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




