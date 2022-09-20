# powerdatagen : Power Grid Datasets Generator
Generates a dataset of [pandapower](https://pandapower.org) power grids datasets from a single snapshot.

# Usage
```
python main.py --config_file config.json
```

# Infos

It generates both a train and a test sets from the same data generating process.

# Configuration

The file `config.json` defines the parameters of the data generation process.

| parameter          | purpose                                                                |
|--------------------|------------------------------------------------------------------------|
| `default_net_path` | Path to the default pandapower network. Should be a `.json` file.      |
| `dataset_name`     | Path where the generated dataset should be stored.                     |
| `n_train`          | Amount of samples in the train set.                                    |
| `n_test`           | Amount of samples in the test set.                                     |
| `sampling`         | Defines the data generating process from which power grids are sampled |

In the `sampling` field, one can define how the topology, loads and generation are built :

| parameter          | purpose                                                       |
|--------------------|---------------------------------------------------------------|
| `topology`         | Sampling of lines, generators and loads to be disconnected.   |
| `total_load`       | Sampling of total summed load in *MW*.                        |
| `active_load`      | Sampling of individual active load in *MW*.                   |
| `reactive_load`    | Sampling of individual reactive loads in *MVAr*.              |
| `active_gen`       | Sampling of individual active generation in *MW*.             |
| `voltage_setpoint` | Sampling of individual generator voltage setpoints in *p.u.*. |

## Topology

Sampling of the power grid topology.

| method                 | parameters | process                                           |
|------------------------|------------|---------------------------------------------------|
| `constant`             | 0          | Does nothing                                      |
| `random_disconnection` | X          | Randomly disconnects lines, generators and loads. |

In the `random_disconnection` mode, one should define a list of disconnection probabilities
for generators, loads and lines. The first value of the list is the probability that
no object of the given class is disconnected, the second is the probability that one
object is disconnected, the third is the probability that two objects are disconnected, 
and so on.
Then, once the amount of object to disconnect has been sampled, the process chooses randomly
this amount of objects uniformly from the list of existing devices.

For instance, let us consider the following parameters :
```
{"sampling_method": "random_disconnection", "params": {"gen": [0.6, 0.4], "load": [1.0], "line": [0.0, 1.0]}}
```
There is a *60%* probability that no generators are disconnected, and *40%* probability that 
one of them is disconnected.
There is a *100%* probability that no loads is disconnected, and a *100%* probability
that exactly one transmission line is disconnected.

## Total load

Sampling of the total consumption of the grid, denoted as $P_{tot}^{new}$.
The following sampling methods are available, where parameters are denoted as $\alpha$ :

| method           | parameters | process                                                                                           |
|------------------|------------|---------------------------------------------------------------------------------------------------|
| `constant`       | 0          | $P_{tot}^{new} = P_{tot}^{old}$.                                                                  |
| `uniform_factor` | 2          | $P_{tot}^{new} = \epsilon \times P_{tot}^{old}$ ; $\epsilon \sim \mathcal{U}(\alpha_1, \alpha_2)$ |
| `normal_factor`  | 2          | $P_{tot}^{new} = \epsilon \times P_{tot}^{old}$ ; $\epsilon \sim \mathcal{N}(\alpha_1, \alpha_2)$ |
| `uniform_values` | 2          | $P_{tot}^{new} \sim \mathcal{U}(\alpha_1, \alpha_2)$                                              |
| `normal_values`  | 2          | $P_{tot}^{new} \sim \mathcal{N}(\alpha_1, \alpha_2)$                                              |

## Active load

Sampling of the individual active loads in *MW*.
The following sampling methods are available, where parameters are denoted as $\alpha$ :

| method                       | parameters | process                                                            |
|------------------------------|------------|--------------------------------------------------------------------|
| `homothetic`                 | 0          | Homothetically adjusts loads to fit the total load.                |
| `uniform_independent_factor` | 1          | Uniform sampling over a simplex centered around the old value[^1]. |
| `normal_independent_factor`  | 1          | Normal sampling around the old value[^1].                          |
| `uniform_independent_values` | 1          | Uniform sampling over a simplex[^1].                               |
| `normal_independent_values`  | 1          | Normal sampling[^1].                                               |

[^1]: scaled so that it respects the total load.

In the four last sampling methods, the parameter $\alpha \in [0,1]$ controls the spread 
of the distribution. Let us consider the case of the `uniform_independent_values`.
- If $\alpha = 0$, then the distribution is a dirac where all loads are the same.
- If $\alpha = 1$ then the distribution is uniform over a simplex.

![Active load sampling](./figures/active_load_dark.png#gh-dark-mode-only)
![Active load sampling](./figures/active_load_light.png#gh-light-mode-only)

> **WARNING**: The marginal distributions displayed in the figures above are only valid 
> if there are only two loads. When dealing with n loads, the uniform sampling 
> will amount to sampling from a n-dimensional simplex, thus making the marginal 
> distributions skewed towards low values.