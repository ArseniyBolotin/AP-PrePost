from flask import Flask, request
from ap import AffinityPropagationFlask
from prepost import PrePostFlask
import numpy as np

# import matplotlib.pyplot as plt

app = Flask(__name__)


class Algorithm:
    cnt_id = -1

    def __init__(self, algo_, params_={}):
        Algorithm.cnt_id += 1
        self.algo = algo_
        self.id = Algorithm.cnt_id
        self.results = None
        self.params = params_

    def start(self, data):
        return self.algo(data, self.params)


algorithms = []


@app.route('/experiment/get_ids')
def get_ids():
    algorithms_dict = {}
    for i in range(len(algorithms)):
        algorithms_dict[algorithms[i].algo.__name__] = algorithms[i].id
    return algorithms_dict


def get_data(id):
    if id == 0:
        N = 100
        n = N // 2
        np.random.seed(42)
        x = np.random.normal(0, 1, (n, 2))
        x = np.append(x, np.random.normal(10, 1, (n, 2)), axis=0)
        return x
    if id == 1:
        return [['a', 'c', 'g', 'f'],
                ['e', 'a', 'c', 'b'],
                ['e', 'c', 'b', 'i'],
                ['b', 'f', 'h'],
                ['b', 'f', 'e', 'c', 'd']]


@app.route('/experiment/<int:algorithm_id>/start')
def run_algorithm(algorithm_id):
    data = get_data(algorithm_id)
    algorithms[algorithm_id].results = algorithms[algorithm_id].start(data)
    return 'Success.'


@app.route('/experiment/<int:algorithm_id>/get_results')
def get_results(algorithm_id):
    return str(algorithms[algorithm_id].results)


@app.route('/experiment/<int:algorithm_id>/set_params')
def set_params(algorithm_id):
    for param in algorithms[algorithm_id].params:
        if request.args.get(param) is not None:
            algorithms[algorithm_id].params[param] = request.args.get(param)
    return algorithms[algorithm_id].params


@app.route('/experiment/<int:algorithm_id>/get_params')
def get_params(algorithm_id):
    return algorithms[algorithm_id].params


if __name__ == '__main__':
    for f in [
                (AffinityPropagationFlask, {'max_iter': '200', 'damping': '0.5'}),
                (PrePostFlask, {'eps': '0.4'})
    ]:
        algorithms.append(Algorithm(f[0], f[1]))
    app.run()
