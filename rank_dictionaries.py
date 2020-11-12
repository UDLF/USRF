# <rank_dictionaries.py>
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


def rank_descriptors_by_effec_estim(effectiveness):
    effec_rk = [[desc, effectiveness[desc]] for desc in effectiveness]
    effec_rk = sorted(effec_rk, key=lambda x: x[1], reverse=True)
    return effec_rk


def rank_pairs_by_correlation(correlations):
    cor_rk = [[pair, correlations[str(pair)]] for pair in correlations]
    cor_rk = sorted(cor_rk, key=lambda x: x[1])
    return cor_rk


def rank_pairs_by_selection(selection):
    sel_rk = [[pair, selection[str(pair)]] for pair in selection]
    sel_rk = sorted(sel_rk, key=lambda x: x[1], reverse=True)
    return sel_rk


def rank_pairs_by_map(pairs_map):
    pairs_map_rk = [[pair, pairs_map[str(pair)]] for pair in pairs_map]
    pairs_map_rk = sorted(pairs_map_rk, key=lambda x: x[1], reverse=True)
    return pairs_map_rk


def rank_descriptors_by_map(descriptors_map):
    descriptors_map_rk = [[desc, descriptors_map[desc]]
                          for desc in descriptors_map]
    descriptors_map_rk = sorted(descriptors_map_rk,
                                key=lambda x: x[1],
                                reverse=True)
    return descriptors_map_rk
