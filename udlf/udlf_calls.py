# <udlf_calls.py>
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


import os
import subprocess

cur_path = os.path.dirname(__file__)
udlf_path = os.path.join(cur_path, 'bin/')
udlf_bin = 'udlf'


def gen_config(parameters='', out_file='config.ini'):
    """
    Given the parameters, exports a config file.

    Keyword arguments:
    parameters -- parameters dictionary
    out_file -- path to output the new config file
    """
    # Parameter dicitionary {parameter: value}
    if parameters == '':
        config_dict = {'UDL_TASK': 'UDL',
                       'UDL_METHOD': 'NONE',
                       'SIZE_DATASET': 1400,
                       'INPUT_FILE_FORMAT': 'RK',
                       'INPUT_RK_FORMAT': 'NUM',
                       'INPUT_FILE': 'rks.txt',
                       'INPUT_FILE_LIST': 'lists.txt',
                       'INPUT_FILE_CLASSES': 'classes.txt',
                       'OUTPUT_FILE': 'FALSE',
                       'EFFICIENCY_EVAL': 'FALSE',
                       'EFFECTIVENESS_EVAL': 'TRUE',
                       'EFFECTIVENESS_COMPUTE_MAP': 'TRUE',
                       'EFFECTIVENESS_COMPUTE_PRECISIONS': 'FALSE',
                       'EFFECTIVENESS_COMPUTE_RECALL': 'FALSE',
                       'PARAM_NONE_L': 1400}
    else:
        config_dict = parameters

    # Write to file
    f = open(out_file, 'w+')
    for param in config_dict:
        f.write(param + ' = ' + str(config_dict[param]) + '\n')
    f.close()


def run_udlf(parameters='', effectiveness_measure="map", exec_num=0):
    """
    Given the parameters, performs a UDLF execution.
    WARNING: The function returns the MAP or Precision, so make sure
    to set the effectiveness parameters accordingly.

    Keyword arguments:
    parameters -- parameters dictionary
    effectiveness_measure -- supervised effectiveness measure to use
    exec_num -- used to generate the config.ini avoiding file concurrency
    """
    # Create config file with the specified parameters
    config_file = "config" + str(exec_num) + ".ini"
    gen_config(parameters=parameters,
               out_file=os.path.join(udlf_path, config_file))

    # The MAP value occurence changes when rank aggregation is being used
    if parameters['UDL_TASK'] == 'FUSION':
        map_occurrence = 3
        precision_occurrence = 1
    else:
        map_occurrence = 5
        precision_occurrence = 2

    # Strings for the execution call
    exec_call = (os.path.join(udlf_path, udlf_bin) + ' ' +
                 os.path.join(udlf_path, config_file))
    if effectiveness_measure == "precision":
        # P@K
        proc_string = (exec_call + ' | grep P@ | sed -n ' +
                       str(precision_occurrence) + 'p')
    else:
        # MAP
        proc_string = (exec_call + ' | grep MAP | sed -n ' +
                       str(map_occurrence) + 'p')

    # Run UDLF and get the MAP value from the output
    effec_value = subprocess.check_output(proc_string, shell=True,
                                          stderr=subprocess.DEVNULL)

    # Process the output string to get only the value
    effec_value = float(str(effec_value).split('\\t')[-1].rstrip("\\n'"))

    return effec_value


def eval_supervised_effectiveness(path_file,
                                  lists_path,
                                  classes_path,
                                  dataset_size,
                                  top_k=20,
                                  l_size=0,
                                  effectiveness_measure="map",
                                  exec_num=0):
    """
    This function returns the original MAP or Precision of the
    given ranked list file

    Keyword arguments:
    path_file -- path of the ranked list file
    lists_path -- path of the lists file
    classes_path -- path of the classes file
    dataset_size -- value of the dataset size
    l_size -- ranked lists size
    effectiveness_measure -- supervised effectiveness measure to use
    exec_num -- used to generate the config.ini avoiding file concurrency
    """
    path_file = os.path.abspath(path_file)

    if l_size == 0:
        l_size = dataset_size

    eval_par_dict = {'UDL_TASK': 'UDL',
                     'UDL_METHOD': 'NONE',
                     'SIZE_DATASET': dataset_size,
                     'INPUT_FILE_FORMAT': 'RK',
                     'INPUT_RK_FORMAT': 'NUM',
                     'INPUT_FILE': path_file,
                     'INPUT_FILE_LIST': lists_path,
                     'INPUT_FILE_CLASSES': classes_path,
                     'OUTPUT_FILE': 'FALSE',
                     'EFFICIENCY_EVAL': 'FALSE',
                     'EFFECTIVENESS_EVAL': 'TRUE',
                     'EFFECTIVENESS_COMPUTE_MAP': 'TRUE',
                     'EFFECTIVENESS_COMPUTE_PRECISIONS': 'TRUE',
                     'EFFECTIVENESS_PRECISIONS_TO_COMPUTE': top_k,
                     'EFFECTIVENESS_COMPUTE_RECALL': 'FALSE',
                     'PARAM_NONE_L': l_size}

    return run_udlf(parameters=eval_par_dict,
                    effectiveness_measure=effectiveness_measure,
                    exec_num=exec_num)


def fuse_tuple_cprr(tuple_combination,
                    path_files,
                    lists_path,
                    classes_path,
                    dataset_size,
                    top_k=20,
                    num_iterations=1,
                    l_size=0,
                    effectiveness_measure="map",
                    exec_num=0):
    """
    This function returns the MAP or Precision value of the CPRR fusion
    result for a given tuple/combination of descriptors.

    Keyword arguments:
    tuple_combination -- tuple of descriptors to be fused
    path_files -- path of the ranked lists files
    lists_path -- path of the lists file
    classes_path -- path of the classes file
    dataset_size -- value of the dataset size
    top_k -- CPRR neighborhood size
    num_iterations -- number of CPRR iterations
    l_size -- ranked lists size
    effectiveness_measure -- supervised effectiveness measure to use
    exec_num -- used to generate the config.ini avoiding file concurrency
    """
    if l_size == 0:
        l_size = dataset_size

    fuse_cprr_dict = {'UDL_TASK': 'FUSION',
                      'UDL_METHOD': 'CPRR',
                      'SIZE_DATASET': dataset_size,
                      'INPUT_FILE_FORMAT': 'RK',
                      'INPUT_RK_FORMAT': 'NUM',
                      'INPUT_FILE_LIST': os.path.abspath(lists_path),
                      'INPUT_FILE_CLASSES': os.path.abspath(classes_path),
                      'OUTPUT_FILE': 'FALSE',
                      'EFFICIENCY_EVAL': 'FALSE',
                      'EFFECTIVENESS_EVAL': 'TRUE',
                      'EFFECTIVENESS_COMPUTE_MAP': 'TRUE',
                      'EFFECTIVENESS_COMPUTE_PRECISIONS': 'TRUE',
                      'EFFECTIVENESS_PRECISIONS_TO_COMPUTE': top_k,
                      'EFFECTIVENESS_COMPUTE_RECALL': 'FALSE',
                      'PARAM_NONE_L': l_size,
                      'PARAM_CPRR_L': l_size,
                      'PARAM_CPRR_T': num_iterations,
                      'PARAM_CPRR_K': top_k}

    # Set input files
    fuse_cprr_dict["NUM_INPUT_FUSION_FILES"] = len(tuple_combination)
    path_files = os.path.abspath(path_files)
    for i, input_file in enumerate(tuple_combination):
        input_file = os.path.join(path_files, input_file + ".txt")
        fuse_cprr_dict['INPUT_FILES_FUSION_' + str(i+1)] = input_file

    output_effec = run_udlf(parameters=fuse_cprr_dict,
                            effectiveness_measure=effectiveness_measure,
                            exec_num=exec_num)

    return output_effec
