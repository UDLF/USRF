# <effectiveness_estimation_functions.py>
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


from multiprocessing import Pool


def get_effectiveness_func(effectiveness_estimation_measure):
    if effectiveness_estimation_measure == "authority":
        return compute_authority_score

    if effectiveness_estimation_measure == "reciprocal":
        return compute_reciprocal_score

    print("\n ERROR: Unknown effec. estim. measure:",
          effectiveness_estimation_measure)
    exit(1)


def compute_authority_score(ranked_lists, index, top_k):
    score = 0
    rk1 = ranked_lists[index][:top_k]
    for img1 in rk1:
        rk2 = ranked_lists[img1][:top_k]
        for img2 in rk2:
            for current_img in rk1:
                if img2 == current_img:
                    score += 1
                    break
    return (score/(top_k**2))


def compute_reciprocal_score(ranked_lists, index, top_k):
    score = 0
    rk1 = ranked_lists[index][:top_k]
    for img1 in rk1:
        rk2 = ranked_lists[img1][:top_k]
        for img2 in rk2:
            for k, current_img in enumerate(rk1):
                if img2 == current_img:
                    score += 1/(k+1)
                    break
    return (score/(top_k**2))


def compute_rk_effectiveness(effectiveness_function, ranked_lists, top_k):
    n = int(len(ranked_lists))
    total = 0
    for index in range(n):
        total += effectiveness_function(ranked_lists, index, top_k)
    return total/n


def compute_descriptors_effectiveness(parameters,
                                      effectiveness_function,
                                      ranked_lists,
                                      descriptors,
                                      top_k):
    effectiveness = {}
    print("\n Computing effectiveness estimations...")
    n_pools = parameters["multithreading_pools"]
    pool_params = [[effectiveness_function, ranked_lists[descriptor], top_k]
                   for descriptor in descriptors]
    with Pool(n_pools) as p:
        # Some print messages may not be reported while running pool map
        output_effectiveness = p.starmap(compute_rk_effectiveness, pool_params)
    for i, descriptor in enumerate(descriptors):
        effectiveness[descriptor] = output_effectiveness[i]
    print(" Done!")
    return effectiveness
