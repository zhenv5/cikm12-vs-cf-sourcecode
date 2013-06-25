'''
vector space model for computing similarity
Author: Sun Jiankai
'''
import datetime
import pprocess
import math
from meta_weight import item_num
from meta_weight import user_num
from meta_weight import limit
from meta_weight import score_weight_log
from meta_weight import confidence_weight_lambda_log
from meta_weight import confidence_weight_a
from meta_method_weight import getSequence
#trainfilename='dataset/split_train_1m.data'
trainfilename='dataset/split_eachmovie_train.data'
trainfile=open(trainfilename,'r')
user_itempairs_tf_idf_list=[]
user_itempairs_idf_list=[[0 for i in range(item_num)] for j in range(item_num)]
user_itempairs_tf_list=[]
print 'for test' 
def calculate_tf_idf(t):
    global user_itempairs_idf_list
    user_id,item_pairs_list=t
    user_itempairs_tf_idf_list_temp=[]
    for j in range(len(item_pairs_list)):
        item_i,item_j,tf,score=item_pairs_list[j]
        count_positive=user_itempairs_idf_list[int(item_i)-1][int(item_j)-1]
        count_negative=user_itempairs_idf_list[int(item_j)-1][int(item_i)-1]
        indicator=0
        if count_negative!=0 and count_negative!=0:
            if score>0:
                weight_lambda=round(math.log(1+count_negative*1.0/count_positive,confidence_weight_lambda_log),8)
                indicator=1
            else:
                weight_lambda=round(math.log(1+count_positive*1.0/count_negative,confidence_weight_lambda_log),8)
                indicator=-1
        else:
            weight_lambda=0
        weight_alpa=round(math.log(1.00+(confidence_weight_a-1)*(count_positive+count_negative)/user_num,confidence_weight_a),8)
        idf=round(weight_alpa*weight_lambda+1.00-weight_alpa,8)
        tf_idf=round(tf*idf,8)
        user_itempairs_tf_idf_list_temp.append((item_i,item_j,tf_idf,indicator))
    print 'user_id '+user_id+' is ok,tf-idf'
    return i,user_id,user_itempairs_tf_idf_list_temp
def calculate_sim(t):
    i,user_id_i,user_itempairs_tf_idf_list_temp_i=t
    global user_itempairs_tf_idf_list
    user_user_sim_list=[]
    for j in range(i+1,len(user_itempairs_tf_idf_list)):
        j,user_id_j,user_itempairs_tf_idf_list_temp_j=user_itempairs_tf_idf_list[j]
        len_i=len(user_itempairs_tf_idf_list_temp_i)
        len_j=len(user_itempairs_tf_idf_list_temp_j)
        pointer_i=0
        pointer_j=0
        euclidean=0
        inner_sum=0
       
        while pointer_i<len_i and pointer_j<len_j:
            item_i_i=int(user_itempairs_tf_idf_list_temp_i[pointer_i][0])
            item_j_i=int(user_itempairs_tf_idf_list_temp_i[pointer_i][1])
            item_i_j=int(user_itempairs_tf_idf_list_temp_j[pointer_j][0])
            item_j_j=int(user_itempairs_tf_idf_list_temp_j[pointer_j][1])
            if item_i_i==item_i_j:
                if item_j_i==item_j_j:
                    tf_idf_i=float(user_itempairs_tf_idf_list_temp_i[pointer_i][2])
                    tf_idf_j=float(user_itempairs_tf_idf_list_temp_j[pointer_j][2])
                    indicator_i=int(user_itempairs_tf_idf_list_temp_i[pointer_i][3])
                    indicator_j=int(user_itempairs_tf_idf_list_temp_j[pointer_j][3])
                    euclidean+=round(tf_idf_i*tf_idf_j,8)
                    inner_sum+=round(tf_idf_i*tf_idf_j*indicator_i*indicator_j,8)
                   
                
                    pointer_i+=1
                    pointer_j+=1
                elif item_j_i<item_j_j:
                    pointer_i+=1
                else:
                    pointer_j+=1    
            elif item_i_i<item_i_j:
                pointer_i+=1
            else:
                pointer_j+=1
        if euclidean!=0 :
            sim=round(inner_sum/euclidean,8)
        else:
            sim=0
        print 'i j sim is:'+user_id_i+' '+user_id_j+' '+str(sim)
        user_user_sim_list.append((user_id_i,user_id_j,sim))
    return user_user_sim_list      
        
def calculate_tf(t):
    user_id,templist=t
    item_nums=len(templist)
    item_pairs_list=[]
    for i in range(item_nums-1):
        item_i,score_i=templist[i]
        for j in range(i+1,item_nums):
            item_j,score_j=templist[j]
            #append to item pairs list
            if int(score_i)!=int(score_j):
                #item_pairs_list.append((item_i,item_j,int(score_i)-int(score_j)))
                tf=round(math.log(1+math.fabs((int(score_i)-int(score_j))),score_weight_log),8)
                item_pairs_list.append((item_i,item_j,tf,int(score_i)-int(score_j)))
    print 'tf userid:'+user_id
    return user_id,item_pairs_list
def main(resultfilename):
    start_1=datetime.datetime.now()
    print str(start_1)
    resultfile=open(resultfilename,'w')
    #used for computing tf
    sequence_tf=getSequence(trainfile)
    #used for computing idf
    global user_itempairs_idf_list,user_itempairs_tf_list
    user_user_sim_matrix=[[0 for i in range(user_num)]for j in range(user_num)]
    start_2=datetime.datetime.now()
    print str(start_2)+' 2 used '+str(start_2-start_1)+'total used '+str(start_2-start_1)
    results=pprocess.pmap(calculate_tf,sequence_tf,limit)
    for result in results:
        user_id,item_pairs_list=result
        user_itempairs_tf_list.append((user_id,item_pairs_list))
        for i in range(len(item_pairs_list)):
            item_i,item_j,tf,score=item_pairs_list[i]
            if score>0:
                user_itempairs_idf_list[int(item_i)-1][int(item_j)-1]+=1
            else:
                user_itempairs_idf_list[int(item_j)-1][int(item_i)-1]+=1
        #print 'user_id for tf '+user_id
    start_3=datetime.datetime.now()
    print str(start_3)+' 3 used '+str(start_3-start_2)+'total used '+str(start_3-start_1)
    global user_itempairs_tf_idf_list
    results=pprocess.pmap(calculate_tf_idf,user_itempairs_tf_list,limit)
    for result in results:
        user_itempairs_tf_idf_list.append(result)
    del user_itempairs_tf_list
    del user_itempairs_idf_list
    start_4=datetime.datetime.now()
    print str(start_4)+' 4 used '+str(start_4-start_3)+'total used '+str(start_4-start_1)
    results=pprocess.pmap(calculate_sim,user_itempairs_tf_idf_list,limit)
    for result in results:
        for i in range(len(result)):
            u_i=int(result[i][0])-1
            u_j=int(result[i][1])-1
            sim=float(result[i][2])
            user_user_sim_matrix[u_i][u_j]=sim
        #print str(u_i)+' is computed ok'
    start_5=datetime.datetime.now()
    del user_itempairs_tf_idf_list
    print str(start_5)+' 5 used '+str(start_5-start_4)+'total used '+str(start_5-start_1)
    for i in range(user_num):
        for j in range(user_num):
            resultfile.write(str(user_user_sim_matrix[i][j]))
            resultfile.write(' ')
        resultfile.write('\n')
    start_6=datetime.datetime.now()
    print str(start_6)+' 6 used '+str(start_6-start_5)+'total used '+str(start_6-start_1)
    resultfile.close()
    trainfile.close()
    start_7=datetime.datetime.now()
    print str(start_7)+' 7 used '+str(start_7-start_6)+'total used '+str(start_7-start_1)
    print 'sim end'
    print '********************************'

print 'start'
print str(user_num) 
main('afterdone/user_user_similarity/user_user_sim_eachmovie_weight.data')
     
   
        
