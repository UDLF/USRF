# <show_messages.py>
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


from pprint import pprint


def show_usraf_header():
    print(" Welcome to USRAF!\n")


def show_settings(parameters, dataset):
    print("---------------------------------")
    print(" General parameters:")
    print("\tSelection Mode:", parameters["selection_mode"])
    print("\tEffectiveness Estimation Measure:",
          parameters["effectiveness_estimation_measure"])
    print("\tCorrelation Measure:", parameters["correlation_measure"])
    print("\tBeta (cor. coef.):", parameters["beta"])
    print("\tTop K:", parameters["top_k"])
    print("\tEffectiveness Measure:", parameters["supervised_effectiveness"])
    print("\tTop Tuples to Fuse:", parameters["top_tuples_fusion"])
    print("\tTop Tuples for Intersection:",
          parameters["top_tuples_intersection"])
    print("\tMax Tuple Size:", parameters["max_tuple_size"])
    print("\tPerform Fusion:", parameters["perform_fusion"])
    print("\tPerform Evaluation:", parameters["perform_evaluation"])
    print("\tMultithreading Pools:", parameters["multithreading_pools"])
    print(" Dataset info:")
    print("\tDataset name:", dataset["name"])
    print("\tDataset size:", dataset["size"])
    print("\tRanked lists path:", dataset["path_ranked_lists"])
    print("\tLists file path:", dataset["path_lists_file"])
    print("\tClasses file path:", dataset["path_classes_file"])
    print("---------------------------------")


def show_available_descriptors(descriptors):
    print("\n Available descriptors:")
    print("\t(", len(descriptors), "descriptors in total )")
    print(end="\t")
    pprint(descriptors, indent=8)


def show_computed_pairs(pairs):
    print("\n Possible combinations (pairs):")
    print("\t(", len(pairs), "pairs in total )")
    pprint(pairs, indent=8)


def show_computed_combinations(combinations):
    print("\n Possible combinations:")
    print("\t(", len(combinations), "combinations in total )")
    pprint(combinations, indent=8)


def show_effectiveness_results(effectiveness):
    print("\n Effectiveness estimation results:")
    pprint(effectiveness, indent=8)


def show_correlation_results(correlations):
    print("\n Correlation for each pair:")
    pprint(correlations, indent=8)


def show_pairs_selection_results(selection_pairs):
    print("\n Selection score for each pair:")
    pprint(selection_pairs, indent=8)


def show_tuples_selection_results(selection_tuples):
    print("\n Selection score for each tuple:")
    pprint(selection_tuples, indent=8)


def show_pairs_map_results(parameters, pairs_map):
    print("\n", parameters["supervised_effectiveness"].upper(),
          "results for each pair after CPRR fusion:")
    pprint(pairs_map, indent=8)


def show_descriptors_map_results(parameters, descriptors_map):
    print("\n", parameters["supervised_effectiveness"].upper(),
          "results for each descriptor:")
    pprint(descriptors_map, indent=8)


def show_avg_topk_lists(parameters,
                        selection_avg_topk,
                        best_avg_topk,
                        average_avg_topk,
                        worst_avg_topk):
    class prettyfloat(float):
        def __repr__(self):
            return "%0.4f" % self

    n_values_to_show = 10
    print("\n Accumulated average",
          parameters["supervised_effectiveness"].upper(),
          "until top-" + str(n_values_to_show) + ":")
    print(" USRAF =",
          list(map(prettyfloat, selection_avg_topk))[:n_values_to_show])
    print(" Best =",
          list(map(prettyfloat, best_avg_topk))[:n_values_to_show])
    print(" Avg =",
          list(map(prettyfloat, average_avg_topk))[:n_values_to_show])
    print(" Worst =",
          list(map(prettyfloat, worst_avg_topk))[:n_values_to_show])
