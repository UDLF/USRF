# <correlation_functions.py>
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


import math
import numpy as np
from nltk import agreement
from multiprocessing import Pool


def get_correlation_func(correlation_measure):
    if correlation_measure == "jaccard":
        return compute_jaccard

    if correlation_measure == "jaccard_k":
        return compute_jaccard_k

    if correlation_measure == "rbo":
        return compute_rbo

    if correlation_measure == "kendalltau":
        return compute_kendalltau

    if correlation_measure == "kendallw":
        return compute_kendallw

    if correlation_measure == "spearman":
        return compute_spearman

    if correlation_measure == "kappa":
        return compute_kappa

    if correlation_measure == "fleiss":
        return compute_fleiss

    if correlation_measure == "alpha":
        return compute_alpha

    if correlation_measure == "scotts":
        return compute_scotts

    if correlation_measure == "generalized_jaccard":
        return compute_jaccard

    print("\n ERROR: Unknown correlation measure:",
          correlation_measure)
    exit(1)


def get_correlation_func_tuples(correlation_measure):
    if correlation_measure == "kendallw":
        return kendall_w

    if correlation_measure == "kappa":
        return kappa

    if correlation_measure == "fleiss":
        return fleiss

    if correlation_measure == "alpha":
        return alpha

    if correlation_measure == "scotts":
        return scotts

    if correlation_measure == "generalized_jaccard":
        return generalized_jaccard

    print("\n ERROR: Unknown correlation measure:",
          correlation_measure)
    exit(1)


def compute_jaccard(x, y, top_k):
    return len(set(x) & set(y))/len(set(x) | set(y))


def compute_jaccard_k(x, y, top_k):
    score = 0

    for k in range(1, top_k+1):
        inter = len(set(x[:k]) & set(y[:k]))
        union = len(set(x[:k]) | set(y[:k]))
        score += (inter/union)

    score = score/top_k

    return score


def compute_rbo(x, y, top_k):
    p = 0.9
    score = 0

    for k in range(1, top_k+1):
        inter = len(set(x[:k]) & set(y[:k]))
        score += (p**(k-1))*(inter/k)

    score = (1-p)*score

    return score


def get_index(i, x):
    """
    Returns the position of the element 'i' in the ranked list 'x'
    """
    if i in x:
        return x.index(i)
    else:
        return len(x)


def check_sizes(x, y):
    """
    Verifies if the ranked lists 'x' and 'y' have the same size
    """
    if len(x) != len(y):
        return False
    return True


def compute_kendalltau(x, y, top_k):
    inter = []
    for elem in (set(x) | set(y)):
        inter.append((get_index(elem, x), get_index(elem, y)))

    ktau = 0
    n = len(inter)
    for i in range(0, n):
        for j in range(i+1, n):
            comp1 = int(inter[i][0] >= inter[j][0])
            comp2 = int(inter[i][1] >= inter[j][1])
            if (comp1 != comp2):
                ktau += 1

    ktau = ktau/((n*(n-1))/2)

    return (1-ktau)


def get_pos_list(rks):
    rks_pos = []
    for rk in rks:
        rk_pos = [get_index(i+1, rk)+1 for i, x in enumerate(rk)]
        rks_pos.append(rk_pos)
    return rks_pos


def kendall_w(rks, top_k):
    # compute pos list from ranked lists
    rks = [rk[:top_k] for rk in rks]
    rks = get_pos_list(rks)

    m = len(rks)  # number of ranked lists to compare
    n = len(rks[0])  # number of elements in each ranked list

    # compute kendall w
    r = np.sum(rks, axis=0)
    a = np.sum(r)/n
    d = [math.fabs(x-a) for x in r]
    d2 = [x**2 for x in d]
    s = np.sum(d2)
    w = (12*s)/(m**2*(n)*(n**2-1))

    # compute chi squared
    # x2 = m*(n-1)*w
    # v = chi2.isf(q=0.05, df=n-1)
    # reject = x2 < v

    return w


def compute_kendallw(x, y, top_k):
    rks = [x, y]
    return kendall_w(rks, top_k)


def compute_spearman(x, y, top_k):
    inter = []
    for elem in (set(x) | set(y)):
        inter.append((get_index(elem, x), get_index(elem, y)))

    spearman = 0
    n = len(inter)
    for i in range(0, n):
        spearman += abs(inter[i][0]-inter[i][1])

    spearman = spearman/(len(x)*(len(x)+1))

    return (1-spearman)


def kappa(rks, top_k):
    rks = [rk[:top_k] for rk in rks]
    taskdata = []
    for j, rk in enumerate(rks):
        taskdata += [[j, str(i), str(rk[i])] for i in range(0, len(rk))]
    ratingtask = agreement.AnnotationTask(data=taskdata)
    return ratingtask.kappa()


def compute_kappa(x, y, top_k):
    rks = [x, y]
    return kappa(rks, top_k)


def fleiss(rks, top_k):
    rks = [rk[:top_k] for rk in rks]
    taskdata = []
    for j, rk in enumerate(rks):
        taskdata += [[j, str(i), str(rk[i])] for i in range(0, len(rk))]
    ratingtask = agreement.AnnotationTask(data=taskdata)
    return ratingtask.multi_kappa()


def compute_fleiss(x, y, top_k):
    rks = [x, y]
    return fleiss(rks, top_k)


def alpha(rks, top_k):
    rks = [rk[:top_k] for rk in rks]
    taskdata = []
    for j, rk in enumerate(rks):
        taskdata += [[j, str(i), str(rk[i])] for i in range(0, len(rk))]
    ratingtask = agreement.AnnotationTask(data=taskdata)
    return ratingtask.alpha()


def compute_alpha(x, y, top_k):
    rks = [x, y]
    return alpha(rks, top_k)


def scotts(rks, top_k):
    rks = [rk[:top_k] for rk in rks]
    taskdata = []
    for j, rk in enumerate(rks):
        taskdata += [[j, str(i), str(rk[i])] for i in range(0, len(rk))]
    ratingtask = agreement.AnnotationTask(data=taskdata)
    return ratingtask.pi()


def compute_scotts(x, y, top_k):
    rks = [x, y]
    return scotts(rks, top_k)


def generalized_jaccard(rks, top_k):
    rks = [rk[:top_k] for rk in rks]
    union = set().union(*rks)
    intersec = set.intersection(*map(set, rks))
    return len(intersec)/len(union)


def compute_pair_correlation(correlation_function, rk1, rk2, top_k):
    n = int(len(rk1))
    total = 0
    for i in range(n):
        total += correlation_function(rk1[i][:top_k], rk2[i][:top_k], top_k)
    return total/n


def compute_tuple_correlation(correlation_function, rks, top_k):
    n = int(len(rks[0]))
    total = 0
    for i in range(n):
        rks_in = []
        for j in range(len(rks)):
            rks_in += [rks[j][i]]
        total += correlation_function(rks_in, top_k)
    return total/n


def compute_correlations_for_pairs(parameters,
                                   correlation_function,
                                   ranked_lists,
                                   pairs,
                                   top_k):
    correlations = {}
    print("\n Computing correlations...")
    n_pools = parameters["multithreading_pools"]
    pool_params = [[correlation_function,
                   ranked_lists[pair[0]],
                   ranked_lists[pair[1]],
                   top_k] for pair in pairs]
    with Pool(n_pools) as p:
        # Some print messages may not be reported while running pool map
        output_correlations = p.starmap(compute_pair_correlation, pool_params)
    for i, pair in enumerate(pairs):
        correlations[str(pair)] = output_correlations[i]
    print(" Done!")
    return correlations


def compute_correlations_for_tuples(parameters,
                                    correlation_function,
                                    ranked_lists,
                                    tuples,
                                    top_k):
    print("Running... ", tuples)
    correlations = {}
    print("\n Computing correlations...")
    rks = []
    for tup in tuples:
        rks.append([ranked_lists[tup[i]] for i in range(len(tup))])
    n_pools = parameters["multithreading_pools"]
    pool_params = [[correlation_function,
                    rks[i], top_k] for i in range(len(tuples))]
    with Pool(n_pools) as p:
        # Some print messages may not be reported while running pool map
        output_correlations = p.starmap(compute_tuple_correlation, pool_params)
    for i, tup in enumerate(tuples):
        correlations[str(tup)] = output_correlations[i]
    print(" Done!")
    return correlations
