
# BASELINE4DESA_STM/MM
This repo is forked from [STM/MM](https://github.com/zeromike/bid-lands), I modified some code in the repo to make it a baseline model for [DESA](https://github.com/qinjr/deep-bid-lands/tree/master/published_code), which is the implementation of the model proposed in a KDD'18 submitted paper, "Deep Survival Analysis for Fine-grained Bid Landscape Forecasting in Real-time Bidding Advertising".
Many thanks to the authors of `STM`.

### Data Preparation
We have upload a tiny data sample for training and evaluation.
The full dataset for this project can be download from this [link](http://apex.sjtu.edu.cn/datasets/13).
After download please replace the sample data in `deep-bid-lands-data/` folder with the full data files.

### Installation and Running
Please install `sklearn` first.
To run the demo, just execute
```
python demo.py
```
and the result(AUC, Log-Loss and ANLP) will be printed on the screen. And the result can also be found in `data/baseline_kdd15_Rversion`(for `MM`) and `data/SurvivalModel`(for `STM`), the results files are named in the pattern `evalution_xxxx.txt`(`STM`) or `baseline_kdd15_xxx.txt`(`MM`).
To run the file with full volume data, just change the `campaign_list` variable in `python/demo.py` and execute it.
