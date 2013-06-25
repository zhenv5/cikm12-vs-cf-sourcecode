'''
predict file
Author: Sun Jiankai
'''

'''
user_user_sim='afterdone/user_user_similarity/user_user_sim_ml1m_weight_tw_kendallrank.data'
user_user_sim_theta='afterdone/user_user_similarity/user_user_sim_ml1m_weight_theta_kendallrank.data'
from weighted_score_kendallrank_tw import main
print 'start tw sim'
main(user_user_sim,user_user_sim_theta)
'''
#eachmovie degree-speciliaty weighted, using vector space model computing
#similarity, user_user_sim_eachmovie_weight.data
#eachmovie used for train

train_file='dataset/split_eachmovie_train.data'
test_movie='dataset/split_eachmovie_test.data'
user_user_sim='afterdone/user_user_similarity/user_user_sim_eachmovie_weight.data'
'''
#movilelengs used for train

train_file='dataset/split_train_1m.data'
test_movie='dataset/split_test_1m.data'
user_user_sim='afterdone/user_user_similarity/user_user_sim_1m_split_iiia9.data'
'''
print 'now predicting....'
import datetime
import pprocess
import math
from meta_weight import user_num
from meta_weight import item_num
from meta_weight import limit
from meta_method_weight import getSequence
from meta_method_weight import select_neighbour_improved
from meta_method_weight import get_user_list
from meta_method_weight import get_sim_list
from meta_method_weight import greedy_order

user_user_sim_list=get_sim_list(user_user_sim,user_num)
user_list=get_user_list(train_file,user_num,item_num)
def schulze_method(item_pairs_predict_list):
    C=int((math.sqrt(len(item_pairs_predict_list)*8+1)+1)/2)
    d=[[0 for i in range(C)] for j in range(C)]
    p=[[0 for i in range(C)] for j in range(C)]
    rank_list=[]
    for i in range(C):
        for j in range(C):
            if i<j:
                index=i*(C)-i*(i+1)/2+(j-i)-1
                d[i][j]=float(item_pairs_predict_list[index][3])
            elif i>j:
                d[i][j]=-d[j][i]
    for i in range(C):
        for j in range(C):
            if i!=j:
                if d[i][j]>d[j][i]:
                    p[i][j]=d[i][j]
                else:
                    p[i][j]=0
    for i in range(C):
        for j in range(C):
            if i!=j:
                for k in range(C):
                    if i!=k and j!=k:
                        p[j][k]=max(p[j][k],min(p[j][i],p[i][k]))
    dict_d={}
    for i in range(C):
        dict_d[i]=0
    for i in range(C):
        count=0
        for j in range(C):
            if i!=j:
                if p[i][j]>p[j][i]:
                    count+=1
        dict_d[i]=count
    dict_list=list(dict_d.items())
    dict_list.sort(key=lambda x:(x[1],x[0]), reverse=True)
    for i in range(len(dict_list)):
        index=int(dict_list[i][0])
        if index==0:
            filmid_j=int(item_pairs_predict_list[index][1])
            score_j=int(item_pairs_predict_list[index][4])
        else:
            filmid_j=int(item_pairs_predict_list[index-1][2])
            score_j=int(item_pairs_predict_list[index-1][5])
        rank_list.append((filmid_j,score_j))
    return rank_list
def calculate(t):
    user_id,item_list=t
    item_pairs_list=[]
    item_pairs_predict_list=[]
    rank_list=[]
    if len(item_list)>1:
        for j in range(len(item_list)-1):
            filmid_j,score_j=item_list[j]
            for k in range(j+1,len(item_list)):
                filmid_k,score_k=item_list[k]
                item_pairs_list.append((filmid_j,filmid_k,score_j,score_k))
        #print 'user '+user_id+' item pairs ok, length is '+str(len(item_pairs_list))
        for i in range(len(item_pairs_list)):
            filmid_j,filmid_k,score_j,score_k=item_pairs_list[i]
            neighbour_list=select_neighbour_improved(user_list,user_user_sim_list,int(user_id),int(filmid_j),int(filmid_k),neighbour_size,oppositeflag)
            total_sim=0
            total_pre=0
            for j in range(len(neighbour_list)):
                sim,pre=neighbour_list[j]
                total_pre+=sim*pre
                total_sim+=sim
            if total_sim==0:
                pre_j_k=0
            else:
                pre_j_k=round(total_pre/total_sim,8)
            item_pairs_predict_list.append((user_id,filmid_j,filmid_k,pre_j_k,int(score_j),int(score_k)))
            #print 'userid '+user_id+' film id j and k '+filmid_j+' '+filmid_k+'predict pre: '+str(pre_j_k)+' real is '+str(int(score_j)-int(score_k))
        #get item_pairs_perdict preference,then use greedy algorithm to get rank list
        if greedyflag==True:
            rank_list=greedy_order(item_pairs_predict_list)
        else:
            rank_list=schulze_method(item_pairs_predict_list)
    else:
        rank_list.append((item_list[0][0],item_list[0][1]))
    return user_id,rank_list            
def predict_rankbased(testfilename,resultfilename):
    testfile=open(testfilename,'r')
    resultfile=open(resultfilename,'w')
    sequence=getSequence(testfile)  
    results=pprocess.pmap(calculate, sequence, limit)
    for i in range(len(sequence)):
        userid,rank_list=results[i]
        for j in range(len(rank_list)):
            resultfile.write(str(userid))
            resultfile.write(' ')
            resultfile.write(str(rank_list[j][1]))
            resultfile.write(' ')
            resultfile.write(str(rank_list[j][0]))
            resultfile.write('\n') 
        print str(userid)+' done'
    testfile.close()
    resultfile.close()
start=datetime.datetime.now()
print 'start at '+str(start)
print str(user_num)
neighbour_sizes=[1,5,10,50,60,70,80,90,100]

for i in range(len(neighbour_sizes)):
    neighbour_size=neighbour_sizes[i]
    
    greedyflag=True
    oppositeflag=False
    predict_rankbased(test_movie,
                      'afterdone/predict/pre_g_r_WeightedKendallTau_eachmovie_'+str(neighbour_size)+'.data') 
    print '*************************'
    print 'neighbor size='+str(neighbour_size)+' ok'
    print 'greedy '
    print '*************************'
    
    greedyflag=False
    oppositeflag=False
    predict_rankbased(test_movie,
                      'afterdone/predict/pre_s_c_WeightedKendallTau_eachmovie_'+str(neighbour_size)+'.data') 
    print '*************************'

    print 'neighbor size='+str(neighbour_size)+' ok'
    print 'schulze '
 
    print '*************************'
    
end=datetime.datetime.now()
print 'start at '+str(start)
print 'end at '+str(end)
print 'total used '+str(end-start)

    
