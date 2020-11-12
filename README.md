# [Unsupervised Selective Rank Fusion Framework](https://github.com/UDLF/USRF/)

**Authors:** [Lucas Pascotti Valem](http://www.lucasvalem.com) and [Daniel Carlos Guimarães Pedronette](http://www.ic.unicamp.br/~dcarlos/)

Dept. of Statistic, Applied Math. and Computing, Universidade Estadual Paulista ([UNESP](http://www.rc.unesp.br/)), Rio Claro, Brazil

## Overview
A framework for ranked lists selection and fusion, completely unsupervised.
If you use this code, please cite our [paper](https://doi.org/10.1016/j.neucom.2019.09.065):

```
    @article{VALEM2020182,
    title = "Unsupervised selective rank fusion for image retrieval tasks",
    journal = "Neurocomputing",
    volume = "377",
    pages = "182 - 199",
    year = "2020",
    issn = "0925-2312",
    doi = "https://doi.org/10.1016/j.neucom.2019.09.065",
    url = "http://www.sciencedirect.com/science/article/pii/S0925231219313335",
    author = "Lucas Pascotti Valem and Daniel Carlos Guimarães Pedronette",
    keywords = "Content-based image retrieval, Unsupervised late fusion, Rank-aggregation, Correlation measure, Effectiveness estimation",
    }
```

## How to run

You should install the dependencies specified in the "requirements.txt" file and call it like this:
`python usrf.py dataset_name`

The `dataset_name` can be `flowers`, for example.

This repository contains 6 different feature extractions for the [OxfordFlowers-17](https://www.robots.ox.ac.uk/~vgg/data/flowers/17/index.html) dataset, which can be used for testing.

In the future, we intend to provide a documentation of how to incorporate custom datasets.

## Dependencies

This repository includes a binary file of the [UDLF](https://github.com/UDLF/UDLF/) framework, which is licensed under the GPLv2.

There is also [Octave](https://github.com/UDLF/USRF/), which is an optional dependency in case the user wants to generate some plots for the results.

## Source files explained

[usrf.py]  
The main file in the project and should be used to call an execution.

[config.py]  
Contains all the parameters and dataset configurations (file paths and others).

[stages.py]  
Contains the stages of the framework execution  
    - loading stage  
    - pre-selection stage  
    - selection stage  
    - fusion stage  
    - evaluation stage  

[show_messages.py]  
Print messages shown during the USRAF execution.

[rank_dictionaries.py]  
From dictionaries, get lists with the values ranked according to the scores.

[load_data.py]  
Implements functions to read the data (the ranked lists) from the files into memory.

[parameters_estimation.py]  
Estimation of the parameters if enabled in the config are done by the
functions declared in this file.

[correlation_functions.py]  
Routines to compute the correlation measures (Jaccard, RBO, and others).

[effectiveness_estimation_functions.py]  
Routines to compute the effec. estim. measures (Authority and Reciprocal).

[selection_functions.py]  
Routines that implement the selection score.

[tuples_processing.py]  
Compute available pairs, tuples, intersection of pairs, and others.

[evaluation_functions.py]  
Some functions used in the evaluation stage.

[execute_udlf.py]  
Set the parameters and prepare the executions for the UDL framework.
The executions are processed in parallel (using pools).

[udlf/udlf_calls.py]  
Functions to call the UDL framework.

[octave_calls.py]  
Functions that generate octave scripts and build them.
This is used by the evaluation stage.

## Contact
**Lucas Pascotti Valem**: `lucaspascottivalem@gmail.com` or `lucas.valem@unesp.br`

**Daniel Carlos Guimarães Pedronette**: `daniel.pedronette@unesp.br`

## Acknowledgments
The authors are grateful to São Paulo Research Foundation - [FAPESP](http://www.fapesp.br/en/) (grants 2017/02091-4 and 2013/08645-0).

## License
This project is licensed under GPLv2. See [details.](https://github.com/UDLF/USRF/blob/main/LICENSE)
