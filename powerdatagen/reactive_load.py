import numpy as np


def sample_reactive_load(net, default_net, config):
    """Samples reactive loads based on those found in default_net."""
    method = config["sampling_method"]
    params = config["params"]
    if method == 'constant':
        pass
    elif method == 'constant_pq_ratio':
        apply_constant_pq_ratio(net, default_net)
    elif method == 'uniform_homothetic_factor':
        sample_uniform_homothetic_factor(net, default_net, params)
    elif method == 'normal_homothetic_factor':
        sample_normal_homothetic_factor(net, default_net, params)
    elif method == 'uniform_independent_factor':
        sample_uniform_independent_factor(net, default_net, params)
    elif method == 'normal_independent_factor':
        sample_normal_independent_factor(net, default_net, params)
    elif method == 'uniform_independent_values':
        sample_uniform_independent_values(net, params)
    elif method == 'normal_independent_values':
        sample_normal_independent_values(net, params)


def apply_constant_pq_ratio(net, default_net):
    """Modifies the active loads, to have the same P/Q ratio as in the default_net."""
    pq_ratio = default_net.load.p_mw / default_net.load.q_mvar
    net.load.q_mvar = net.load.p_mw / pq_ratio


def sample_uniform_homothetic_factor(net, default_net, params):
    """Applies a homothetic transform to default values, sampled uniformly from U([params[0], params[1]])."""
    factor = np.random.uniform(params[0], params[1])
    net.load.q_mvar = factor * default_net.load.q_mvar


def sample_normal_homothetic_factor(net, default_net, params):
    """Applies a homothetic transform to default values, sampled normally from N(params[0], params[1])."""
    factor = np.random.normal(params[0], params[1])
    net.load.q_mvar = factor * default_net.load.q_mvar


def sample_uniform_independent_factor(net, default_net, params):
    """Applies independent multiplicative factors, sampled uniformly from U([params[0], params[1]])."""
    n_load = len(net.load)
    factor = np.random.uniform(params[0], params[1], size=n_load)
    net.load.q_mvar = factor * default_net.load.q_mvar


def sample_normal_independent_factor(net, default_net, params):
    """Applies independent multiplicative factors, sampled normally from N(params[0], params[1])."""
    n_load = len(net.load)
    factor = np.random.normal(params[0], params[1], size=n_load)
    net.load.q_mvar = factor * default_net.load.q_mvar


def sample_uniform_independent_values(net, params):
    """Samples values uniformly from U([params[0], params[1]])."""
    n_load = len(net.load)
    values = np.random.uniform(params[0], params[1], size=n_load)
    net.load.q_mvar = values


def sample_normal_independent_values(net, params):
    """Samples values normally from N(params[0], params[1])."""
    n_load = len(net.load)
    values = np.random.normal(params[0], params[1], size=n_load)
    net.load.q_mvar = values
