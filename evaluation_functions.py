# <evaluation_functions.py>
#
#  @Author: Lucas Pascotti Valem <lucas.valem@unesp.br>
#
#-------------------------------------------------------------------------------
#
# This file is part of Unsupervised Selective Rank Fusion Framework (USRF).
#
# USRF is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# USRF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with USRF.  If not, see <http://www.gnu.org/licenses/>.
#


import rank_dictionaries
from scipy.stats import pearsonr as compute_pearson


def compute_pearson_for_scores(parameters, selection_scores, map_scores):
    x = []
    y = []
    print("\n Computing Pearson cor. between",
          parameters["supervised_effectiveness"].upper(),
          "and selection scores...")
    for combination in selection_scores:
        x.append(selection_scores[combination])
        y.append(map_scores[combination])
    pearson = compute_pearson(x, y)[0]
    print(" Pearson:", pearson)
    return pearson


def compute_average_case(map_list):
    map_list = sorted(map_list, reverse=True)
    avg_case = []
    while len(map_list) != 0:
        element = map_list.pop(int(len(map_list)/2))
        avg_case.append(element)
    return avg_case


def compute_virtual_baselines(map_scores):
    print("\n Computing virtual baselines...")
    map_list = [[map_scores[combination], combination]
                for combination in map_scores]
    best_case = sorted(map_list, reverse=True)
    avg_case = compute_average_case(map_list)
    worst_case = sorted(map_list, reverse=False)
    print(" Done!")
    return best_case, avg_case, worst_case


def compute_selection_case(selection_scores, map_scores):
    print("\n Computing selection case...")
    selection_list = rank_dictionaries.\
        rank_pairs_by_selection(selection_scores)
    selection_case = [[map_scores[combination[0]], combination[0]]
                      for combination in selection_list]
    print(" Done!")
    return selection_case


def compute_avg_topk_list(input_case):
    values_only = [x[0] for x in input_case]
    avg_topk = []
    current_value = 0
    for i, value in enumerate(values_only):
        current_value += value
        avg_topk.append(current_value/(i+1))
    return avg_topk
