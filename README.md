# AP-PrePost
This is Affinity Propagation and PrePost algorithms implementation with web-server requests support with Flask. 

Start main on localhost(127.0.0.1), default port - 5000

Requests description:

http://127.0.0.1:5000/get_ids - get ids of current experiments

http://127.0.0.1:5000/experiments/{exp_id}/set_params?{params} - set parametrs in exp_id experiment

http://127.0.0.1:5000/experiments/{exp_id}/start - run exp_id experiment

http://127.0.0.1:5000/experiments/{exp_id}/get_results - results of exp_id experiment
