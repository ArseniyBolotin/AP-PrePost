from flask import Flask, request
from flask_restful import Api, Resource

from ap import AffinityPropagation
from prepost import PrePost
import numpy as np


def AffinityPropagationFlask(data, params):
    max_iter = int(params['max_iter'])
    damping = float(params['damping'])
    return AffinityPropagation(data, max_iter, damping)


def PrePostFlask(data, params):
    eps = float(params['eps'])
    return PrePost(data, eps)


app = Flask(__name__)


# Mock of getting data
def get_data(algo_id):
    if algo_id == 0:
        N = 100
        n = N // 2
        np.random.seed(42)
        x = np.random.normal(0, 1, (n, 2))
        x = np.append(x, np.random.normal(10, 1, (n, 2)), axis=0)
        return x
    if algo_id == 1:
        return [['a', 'c', 'g', 'f'],
                ['e', 'a', 'c', 'b'],
                ['e', 'c', 'b', 'i'],
                ['b', 'f', 'h'],
                ['b', 'f', 'e', 'c', 'd']]
    return None


experiments = {}

ALGORITHMS = [
    (AffinityPropagationFlask, {'max_iter': '200', 'damping': '0.5'}),
    (PrePostFlask, {'eps': '0.4'})
]


class Parameters(Resource):
    # get_ids
    def get(self):
        exp_dict = {}
        for key in experiments:
            exp_dict[key] = str(experiments[key])
        return exp_dict

    # set_params
    def post(self, experiment_id):
        if request.args.get('algo_id') is None:
            return "Request does not contain algorithm id.", 400
        if experiment_id not in experiments:
            experiments[experiment_id] = Experiment()
        exp = experiments[experiment_id]
        algo_id = int(request.args.get('algo_id'))
        exp.algorithm = ALGORITHMS[algo_id][0]
        exp.params = ALGORITHMS[algo_id][1]
        for param in exp.params:
            if request.args.get(param) is not None:
                exp.params[param] = request.args.get(param)
        return "Parameters updated.", 200


class Experiment(Resource):

    def __init__(self, algorithm_=None, params_=None):
        if params_ is None:
            params_ = {}
        self.results = None
        self.algorithm = algorithm_
        self.params = params_

    def __str__(self):
        return self.algorithm.__name__ + ' - ' + str(self.params)

    # get_results
    def get(self, result_id):
        if result_id not in experiments:
            return "Experiment does not exist", 404
        return str(experiments[result_id].results)

    # start
    def post(self, experiment_id):
        if experiment_id not in experiments:
            return "Experiment does not exist", 404
        algo_id = -1
        for i in range(len(ALGORITHMS)):
            if experiments[experiment_id].algorithm == ALGORITHMS[i][0]:
                algo_id = i
        data = get_data(algo_id)
        experiments[experiment_id].results = experiments[
            experiment_id].algorithm(data, experiments[experiment_id].params)
        return "Success.", 200


api = Api(app)
api.add_resource(Experiment, '/experiments/<int:experiment_id>/start',
                 '/experiments/<int:result_id>/get_results')
api.add_resource(Parameters, '/get_ids',
                 '/experiments/<int:experiment_id>/set_params')

if __name__ == '__main__':
    app.run()
