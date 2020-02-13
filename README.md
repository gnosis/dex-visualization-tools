# BATCH AUCTION VISUALIZATIONS

## Installation

* Create virtual Python 3.6 environment:
    `virtualenv --python=/usr/bin/python3.6 venv`
* Activate virtual environment:
    `source venv/bin/activate`
* Install requirements:
    `pip install -r requirements.txt`
    
## Run

* Instance plots (tokens/orders):
    `python plot_order_graph.py [--jsonFile INSTANCE_JSON]`
* Solution plots (execution details):
    `python plot_solution_graph.py [SOLUTION_JSON]`
* Orderbook plots (buy and sell amounts for token pairs):
	`python plot_orderbook_tokenpair.py [TOKEN1] [TOKEN2] [--jsonFile INSTANCE_JSON]`
    
If no JSON file is provided for `plot_order_graph.py` and `plot_orderbook_tokenpair.py`, the script will fetch the data directly from the dfusion smart contract.

## Example data

in `data/`:
* `kraken_{instance|solution}.json` - instance and solution from Kraken exchange
* `dfusion_{instance|solution}.json` - instance and solution from dfusion PoC

example runs:
* `python plot_order_graph.py --jsonFile data/dfusion_input.json`
* `python plot_solution_graph.py data/kraken_solution.json`
* `python plot_orderbook_tokenpair.py PAX WETH
