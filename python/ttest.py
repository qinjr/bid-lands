import numpy as np
from scipy.stats import ttest_ind
from matplotlib.pyplot import *
from DecisionTree import *
from evaluation import *
from baseline_kdd15_Rversion import getWinningPrice
from baseline_kdd15_Rversion_demo import getTestData_yzbx
from baseline import getTrainData_b
DAY_LIST = ['20130607','20131019']

def getNLP(q,info):
    print "getNLP()"
    testset = getTestData(info.fname_testlog, info.fname_testbid)
    nodeInfos = getNodeInfos(info)
    nlp = []
    for i in range(0,len(testset)):
        if i%10000==0:
            print str(i),

        pay_price = eval(testset[i][PAY_PRICE_INDEX])
        nodeIndex = 1
        while True:
            bestFeat = nodeInfos[nodeIndex].bestFeat
            KLD = nodeInfos[nodeIndex].KLD
            s1_keys = nodeInfos[nodeIndex].s1_keys
            s2_keys = nodeInfos[nodeIndex].s2_keys
            if testset[i][bestFeat] in s1_keys:
                nodeIndex = 2*nodeIndex
            elif testset[i][bestFeat] in s2_keys:
                nodeIndex = 2*nodeIndex+1
            else :  # feature value doesn't appear in train data
                nodeIndex = 2*nodeIndex+randint(0,1)

            if not nodeInfos.has_key(nodeIndex):
                nlp.append(-log(q[nodeIndex][pay_price]))

                break

    print "\ngetNLP() ends."
    return nlp

def ttest(info):
    # get nlp_stm
    q1,w,trainMinPrice,trainMaxPrice = getQ(info)
    nlp_stm = getNLP(q1,info)
    wt, _, __ = getTestData_yzbx(IFROOT+info.campaign+'/test.yzbx.txt')

    # get nlp_mm
    w = []
    for day in DAY_LIST:
        tmpw = getWinningPrice('../data/kdd15/WinningPrice/price_all_'+day+'.txt')
        w.extend(tmpw)

    laplace = info.laplace
    q2 = [0.0]*UPPER
    count = 0
    for i in range(0,len(w)):
        q2[w[i]] += 1
        count += 1
    for i in range(0,len(q2)):
        q2[i] = (q2[i]+laplace)/(count+len(q2)*laplace)        #laplace

    nlp_mm = [ -log(q2[wt[i]]) for i in range(0,len(wt)) ]

    # get nlp_nm
    w,winAuctions,winbid,losebid = getTrainData_b(info.fname_trainlog,info.fname_trainbid)
    wcount = [0]*UPPER
    for i in range(0,len(winAuctions)):
        if winAuctions[i]==1:
            wcount[w[i]] += 1

    q3 = calProbDistribution_n(wcount,0,UPPER,info)
    nlp_nm = [ -log(q3[wt[i]]) for i in range(0,len(wt)) ]

    # get nlp_sm
    q4 = calProbDistribution_s(wcount,winbid,losebid,0,UPPER,info)
    nlp_sm = [ -log(q4[wt[i]]) for i in range(0,len(wt)) ]


    print 'stm-mm: t-statistic = %f pvalue = %f' % ttest_ind(nlp_stm,nlp_mm)
    print 'stm-nm: t-statistic = %f pvalue = %f' % ttest_ind(nlp_stm,nlp_nm)
    print 'stm-sm: t-statistic = %f pvalue = %f' % ttest_ind(nlp_stm,nlp_sm)

if __name__ == '__main__':
    IFROOT = '../../deep-bid-lands/data/deep-bid-lands-data/'
    OFROOT = '../data/SurvivalModel/'
    BASE_BID = '0'

    suffix_list = ['n','s','f']

    for campaign in ['2259']:
        print
        print campaign
        for mode in [SURVIVAL]:
            for laplace in [LAPLACE]:
                print MODE_NAME_LIST[mode],
                modeName = MODE_NAME_LIST[mode]
                suffix = suffix_list[mode]

                info = Info()
                info.laplace = laplace
                info.basebid = BASE_BID
                info.mode = mode
                info.campaign = campaign
                info.fname_trainlog = IFROOT+campaign+'/train.log.txt'
                info.fname_testlog = IFROOT+campaign+'/test.log.txt'
                info.fname_nodeData = OFROOT+campaign+'/'+modeName+'/nodeData_'+campaign+suffix+'.txt'
                info.fname_nodeInfo = OFROOT+campaign+'/'+modeName+'/nodeInfos_'+campaign+suffix+'.txt'

                info.fname_trainbid = IFROOT+campaign+'/train.bid.txt'
                info.fname_testbid = IFROOT+campaign+'/test.bid.txt'
                info.fname_baseline = OFROOT+campaign+'/'+modeName+'/baseline_'+campaign+suffix+'.txt'

                info.fname_monitor = OFROOT+campaign+'/'+modeName+'/monitor_'+campaign+suffix+'.txt'
                info.fname_testKmeans = OFROOT+campaign+'/'+modeName+'/testKmeans_'+campaign+suffix+'.txt'
                info.fname_testSurvival = OFROOT+campaign+'/'+modeName+'/testSurvival_'+campaign+suffix+'.txt'

                info.fname_evaluation = OFROOT+campaign+'/'+modeName+'/evaluation_'+campaign+suffix+'.txt'
                info.fname_baseline_q = OFROOT+campaign+'/'+modeName+'/baseline_q_'+campaign+suffix+'.txt'
                info.fname_tree_q = OFROOT+campaign+'/'+modeName+'/tree_q_'+campaign+suffix+'.txt'
                info.fname_test_q = OFROOT+campaign+'/'+modeName+'/test_q_'+campaign+suffix+'.txt'
                info.fname_baseline_w = OFROOT+campaign+'/'+modeName+'/baseline_w_'+campaign+suffix+'.txt'
                info.fname_tree_w = OFROOT+campaign+'/'+modeName+'/tree_w_'+campaign+suffix+'.txt'
                info.fname_test_w = OFROOT+campaign+'/'+modeName+'/test_w_'+campaign+suffix+'.txt'

                info.fname_pruneNode = OFROOT+campaign+'/'+modeName+'/pruneNode_'+campaign+suffix+'.txt'
                info.fname_pruneEval = OFROOT+campaign+'/'+modeName+'/pruneEval_'+campaign+suffix+'.txt'
                info.fname_testwin = OFROOT+campaign+'/'+modeName+'/testwin_'+campaign+suffix+'.txt'

                ttest(info)
