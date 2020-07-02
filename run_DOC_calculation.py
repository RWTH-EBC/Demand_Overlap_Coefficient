# -*- coding: utf-8 -*-
"""Examplary calculation of Demand Overlap Coefficients.

This module demonstrates the calculation of different (single, building energy systems
and network) Demand Overlap Coefficient (DOC) as presented in:

M. Wirtz, L. Kivilip, P. Remmen, D. Müller:
Quantifying Demand Balancing in Bidirectional Low Temperature Networks,
Energy and Buildings, 224, 110245, 2020.

DOI: 10.1016/j.enbuild.2020.110245

Example
-------

For an examplary use of different DOCs please look at __main__ of this module, where all
three DOCs are calculated for synthetic time series for one year in hourly resolution.

"""

import numpy as np
import matplotlib.pyplot as plt


def calc_DOC(heat_dem, cool_dem):
    """Function to calculate DOC for time series.

    This function calculates the DOC for heating and cooling time series. It returns the
    DOC according to Eq. (2). The calculated DOC can be used to determine:

      - District DOC                   in Eq. (6)
      - BES DOC for single building    in Eq. (10)

    Input parameters heat_dem and cool_dem need to have the same dimensions.

    Parameters
    ----------
    heat_dem : array_like
        Numpy array with heating demand time series in same resolution as cool_dem.
    cool_dem : array_like
        Numpy array with cooling demand time series in same resolution as cool_dem.

    Returns
    -------
    float
        DOC for given time series.
    """

    t_steps = range(len(heat_dem))  # Number of time steps

    counter = sum((2 * np.min([heat_dem[k], cool_dem[k]])) for k in t_steps)
    denominator = sum((heat_dem[k] + cool_dem[k]) for k in t_steps)

    return counter / denominator


def calc_mean_BES_DOC(heat_dem_list, cool_dem_list):
    """Function to calculate DOC for an arbitrary number of buildings.

    This function calculates the mean DOC for a number of buildingsas defined in Eq.
    (11). Input parameters heat_dem_list and cool_dem_list need to have the same
    dimensions. In addition, the containing time series need to have the same
    dimensions.

    Parameters
    ----------
    heat_dem_list : list
        List with array_like demand time series for heating.
    cool_dem_list : list
        List with array_like demand time series for cooling.

    Returns
    -------
    float
        mean DOC for given time series as defined in Eq. (11).
    """

    t_steps = range(len(heat_dem_list[0]))  # Number of time steps
    bldgs = range(len(heat_dem_list))       # Number of buildings

    counter = 2 * sum(
        sum(np.min([heat_dem_list[b][t], cool_dem_list[b][t]], 0) for b in bldgs)
        for t in t_steps
    )

    denominator = sum(
        sum(heat_dem_list[b][t] for b in bldgs)
        + sum(cool_dem_list[b][t] for b in bldgs)
        for t in t_steps
    )

    return counter / denominator


def calc_Network_DOC(heat_dem_list, cool_dem_list):
    """Function to calculate DOC for thermal network.

    This function calculates the network DOC for a number of connected buildings as
    defined in Eq. (15). Input parameters heat_dem_list and cool_dem_list need to have
    the same dimensions. In addition, the containing time series need to have the same
    dimensions.

    Parameters
    ----------
    heat_dem_list : list
        List with array_like demand time series for heating.
    cool_dem_list : list
        List with array_like demand time series for cooling.

    Returns
    -------
    float
        Network DOC for given time series as defined in Eq. (15).
    """

    t_steps = range(len(heat_dem_list[0]))  # Number of time steps
    bldgs = range(len(heat_dem_list))       # Number of buildings

    counter = 2 * sum(np.min([sum(heat_dem_list[b][t] for b in bldgs),
                              sum(cool_dem_list[b][t] for b in bldgs)], 0) 
                  for t in t_steps)

    denominator = sum(sum(heat_dem_list[b][t] for b in bldgs)
                    + sum(cool_dem_list[b][t] for b in bldgs) for t in t_steps)

    return counter / denominator



if __name__ == "__main__":

    # CREATE EXEMPLARY DEMAND TIME SERIES

    # Time steps
    time = np.linspace(0, 8759, 8760)

    # Building 1: heat/cold demand (sine curve)
    heat_demand_bldg_1 = 1 * (np.sin(time / 8760 * 2 * np.pi + np.pi / 2) + 1)
    cold_demand_bldg_1 = 1 * (np.sin(time / 8760 * 2 * np.pi - np.pi / 2) + 1)

    # Building 2: heat/cold demand (constand demand)
    heat_demand_bldg_2 = 1 * np.ones(8760)
    cold_demand_bldg_2 = 2 * np.ones(8760)


    # DISTRICT DOC

    # For calculating the District DOC, sum time series of all buildings
    sum_heat_demand = heat_demand_bldg_1 + heat_demand_bldg_2
    sum_cool_demand = cold_demand_bldg_1 + cold_demand_bldg_2

    # Calculate DOC
    DOC_district = calc_DOC(sum_heat_demand, sum_cool_demand)       # Eq. (6)
    print("District DOC is " + str(round(DOC_district, 3)) + ".")


    # BUILDING ENERGY SYSTEM DOC (DOC for individual buildings)

    # Assume COPs for heat pumps and chillers
    COP_HP = 4
    COP_CC = 5

    # Building 1
    heat_demand_BES_1 = heat_demand_bldg_1 * (1 - 1 / COP_HP)       # Eq. (7)
    cold_demand_BES_1 = cold_demand_bldg_1 * (1 + 1 / COP_CC)       # Eq. (8)
    DOC_BES_1 = calc_DOC(heat_demand_BES_1, cold_demand_BES_1)      # Eq. (10)
    print("DOC BES of building 1 is " + str(round(DOC_BES_1, 3)) + ".")

    # Building 2
    heat_demand_BES_2 = heat_demand_bldg_2 * (1 - 1 / COP_HP)       # Eq. (7)
    cold_demand_BES_2 = cold_demand_bldg_2 * (1 + 1 / COP_CC)       # Eq. (8)
    DOC_BES_2 = calc_DOC(heat_demand_BES_2, cold_demand_BES_2)      # Eq. (10)
    print("DOC BES of building 2 is " + str(round(DOC_BES_2, 3)) + ".")

    # Mean BES DOC
    # Collect time series of all buildings in list
    heat_dem_list = [heat_demand_BES_1, heat_demand_BES_2]
    cool_dem_list = [cold_demand_BES_1, cold_demand_BES_2]

    # Calculate Network DOC
    mean_BES_DOC = calc_mean_BES_DOC(heat_dem_list, cool_dem_list)  # Eq. (11)
    print("Mean BES DOC is " + str(round(mean_BES_DOC, 3)) + ".")


    # NETWORK DOC (indicates balancing potential between buildings)

    # Calculate net heat/cold demand
    # Building 1
    bal_1 = np.min([heat_demand_BES_1, cold_demand_BES_1], 0)       # Eq. (9)
    heat_net_demand_1 = heat_demand_BES_1 - bal_1                   # Eq. (13)
    cold_net_demand_1 = cold_demand_BES_1 - bal_1                   # Eq. (14)

    # Building 2
    bal_2 = np.min([heat_demand_BES_2, cold_demand_BES_2], 0)       # Eq. (9)
    heat_net_demand_2 = heat_demand_BES_2 - bal_2                   # Eq. (13)
    cold_net_demand_2 = cold_demand_BES_2 - bal_2                   # Eq. (14)

    # Collect time series of all buildings in list
    heat_dem_list = [heat_net_demand_1, heat_net_demand_2]
    cool_dem_list = [cold_net_demand_1, cold_net_demand_2]

    # Calculate Network DOC
    Network_DOC = calc_Network_DOC(heat_dem_list, cool_dem_list)    # Eq. (15)
    print("Network DOC is " + str(round(Network_DOC, 3)) + ".")


    # VISUALIZE OVERLAP OF DEMANDS

    # Create new figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, ylabel="Thermal demand (MW)", xlabel="Time (hours)")

    # Plot demand profiles
    ax.plot(sum_heat_demand, color=("#c00000"), label="Heat demand (buildings 1 and 2)")
    ax.plot(sum_cool_demand, color=("#4472c4"), label="Cold demand (buildings 1 and 2)")

    # Color areas under profiles
    ax.fill_between(time, 0, sum_heat_demand, color=("#ffc5b8"), label="Heat demand")
    ax.fill_between(time, 0, sum_cool_demand, color=("#c2d1ed"), label="Cold demand")

    # Calculate balanced demands (overlapping area)
    balanced_demands = np.min(np.array([sum_heat_demand, sum_cool_demand]), 0)

    # Color overlapping area
    ax.fill_between(time, 0, balanced_demands, color=("#e1d1e2"), label="Overlap of demands")

    # Set axis
    ax.set_ylim(bottom=0, top=ax.get_ylim()[1] * 1.1)
    ax.set_xlim(left=0, right=8760)

    # Set legend and DOC label
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.3), ncol=2)
    ax.text(200, 0.2, "District DOC = " + str(round(DOC_district, 3)))

    # Save figure
    fig.savefig(
        fname="DOC_visualization.png",
        dpi=200,
        format="png",
        bbox_inches="tight",
        pad_inches=0.1,
    )
