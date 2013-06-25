'''
common methods used by other py files
Author: Sun Jiankai
'''
import math
#used for pprocess to get a sequence
def getSequence_from_matrix(user_item_matrix):
    sequence=[]
    print len(user_item_matrix)
    print len(user_item_matrix[0])
    for i in range(len(user_item_matrix)):
        templist=[]
        for j in range(len(user_item_matrix[i])):
            if user_item_matrix[i][j]!=0:
                templist.append((j+1,user_item_matrix[i][j]))
        sequence.append((i+1,templist))
    return sequence
def getSequence(testfile):
    userlist=testfile.readlines()
    previoususer=userlist[0].split()[0]
    templist=[]
    sequence=[]
    for i in range(len(userlist)):
        nextuser=userlist[i].split()[0]
        filmid=userlist[i].split()[1]
        score=userlist[i].split()[2]
        if previoususer==nextuser:
            templist.append((filmid,score))
        else:
            sequence.append((previoususer,templist))
            templist=[]
            previoususer=nextuser
            templist.append((filmid,score))
    sequence.append((previoususer,templist))
    return sequence
def getSequence_1m(testfile):
    userlist=testfile.readlines()
    previoususer=userlist[0].split('::')[0]
    templist=[]
    sequence=[]
    for i in range(len(userlist)):
        nextuser=userlist[i].split('::')[0]
        filmid=userlist[i].split('::')[1]
        score=userlist[i].split('::')[2]
        if previoususer==nextuser:
            templist.append((filmid,score))
        else:
            sequence.append((previoususer,templist))
            templist=[]
            previoususer=nextuser
            templist.append((filmid,score))
    sequence.append((previoususer,templist))
    return sequence
def getSequence_2(userlist):
    previoususer=userlist[0].split()[0]
    templist=[]
    sequence=[]
    for i in range(len(userlist)):
        nextuser=userlist[i].split()[0]
        filmid=userlist[i].split()[1]
        scores=userlist[i].split()[2]
        score=int(float(scores)*5)
        if previoususer==nextuser:
            templist.append((filmid,score))
        else:
            sequence.append((previoususer,templist))
            templist=[]
            previoususer=nextuser
            templist.append((filmid,score))
    sequence.append((previoususer,templist))
    return sequence
def getSequence_eachmovie(userlist):
    previoususer=userlist[0].split()[0]
    templist=[]
    sequence=[]
    for i in range(len(userlist)):
        nextuser=userlist[i].split()[0]
        filmid=userlist[i].split()[1]
        scores=userlist[i].split()[2]
        score=int(float(scores)*5)
        if score==0:
            continue
        if previoususer==nextuser:
            templist.append((filmid,score))
        else:
            sequence.append((previoususer,templist))
            templist=[]
            previoususer=nextuser
            templist.append((filmid,score))
    sequence.append((previoususer,templist))
    return sequence
#attention neighbour size and oppositeflag
#**********************
#**********************
#**********************
def select_neighbour(user_item_list,user_user_sim_list,user_id,filmid_j,filmid_k,neighbour_size,oppositeflag):
    neighbour_list=[]
    common_rated_user=[]
    #find user that rated film j and k
    for i in range(len(user_item_list)):
        score_j=int(user_item_list[i].split()[filmid_j-1])
        score_k=int(user_item_list[i].split()[filmid_k-1])
        if score_j!=0 and score_k!=0:
            #add userid=i+1 and preference to common_rated_user_list
            common_rated_user.append((i+1,score_j-score_k))
    #find user-user-similarity
    for i in range(len(common_rated_user)):
        common_rated_user_id,preference=common_rated_user[i]
        if user_id<common_rated_user_id:
            sim=float(user_user_sim_list[user_id-1].split()[common_rated_user_id-1])
        else:
            sim=float(user_user_sim_list[common_rated_user_id-1].split()[user_id-1])
        neighbour_list.append((sim,preference))
    #notice that we used fabs to get a neighbour
    #attention
    #***********************
    #***********************
    #***********************
    if oppositeflag==True:
        neighbour_list.sort(key=lambda x:(math.fabs(x[0]),math.fabs(x[1])), reverse=True)
    else:
        neighbour_list.sort(key=lambda x:(x[0],x[1]), reverse=True)
        '''
        for i in range(len(neighbour_list)):
            if neighbour_list[i][0]<0:
                neighbour_list=neighbour_list[0:i]
                break  
                '''      
    #***********************
    #***********************
    #***********************
    neighbour_number=min(len(neighbour_list),neighbour_size)
    neighbour_list=neighbour_list[0:neighbour_number]   
    return neighbour_list
def select_neighbour_improved(user_list,user_user_sim_list,user_id,filmid_j,filmid_k,neighbour_size,oppositeflag):
    neighbour_list=[]
    common_rated_user=[]
    #find user that rated film j and k
    for i in range(len(user_list)):
        score_j=user_list[i][filmid_j-1]
        score_k=user_list[i][filmid_k-1]
        if score_j!=0 and score_k!=0:
            #add userid=i+1 and preference to common_rated_user_list
            common_rated_user.append((i+1,score_j-score_k))
    #find user-user-similarity
    for i in range(len(common_rated_user)):
        common_rated_user_id,preference=common_rated_user[i]
        if user_id<common_rated_user_id:
            sim=user_user_sim_list[user_id-1][common_rated_user_id-1]
        else:
            sim=user_user_sim_list[common_rated_user_id-1][user_id-1]
        neighbour_list.append((sim,preference))
    #notice that we used fabs to get a neighbour
    #attention
    #***********************
    #***********************
    #***********************
    if oppositeflag==True:
        neighbour_list.sort(key=lambda x:(math.fabs(x[0]),math.fabs(x[1])), reverse=True)
    else:
        neighbour_list.sort(key=lambda x:(x[0],x[1]), reverse=True)
    neighbour_number=min(len(neighbour_list),neighbour_size)
    neighbour_list=neighbour_list[0:neighbour_number]   
    return neighbour_list
def select_neighbour_by_singleitem(user_list,user_user_sim_list,user_id,filmid_j,neighbour_size,oppositeflag):
    neighbour_list=[]
    common_rated_user=[]
    #find user that rated film j and k
    for i in range(len(user_list)):
        score_j=user_list[i][filmid_j-1]
        if score_j!=0:
            #add userid=i+1 and preference to common_rated_user_list
            common_rated_user.append((i+1,score_j))
    #find user-user-similarity
    for i in range(len(common_rated_user)):
        common_rated_user_id,preference=common_rated_user[i]
        if user_id<common_rated_user_id:
            sim=user_user_sim_list[user_id-1][common_rated_user_id-1]
        else:
            sim=user_user_sim_list[common_rated_user_id-1][user_id-1]
        neighbour_list.append((sim,preference,common_rated_user_id))
    #notice that we used fabs to get a neighbour
    #attention
    #***********************
    #***********************
    #***********************
    if oppositeflag==True:
        neighbour_list.sort(key=lambda x:(math.fabs(x[0]),math.fabs(x[1])), reverse=True)
    else:
        neighbour_list.sort(key=lambda x:(x[0],x[1]), reverse=True)
    neighbour_number=min(len(neighbour_list),neighbour_size)
    neighbour_list=neighbour_list[0:neighbour_number]   
    return neighbour_list
def search_pre(filmid1,filmid2,item_pairs_predict_list):
    pre_j_k=-1
    for i in range(len(item_pairs_predict_list)):
        filmid_j=int(item_pairs_predict_list[i][1])
        filmid_k=int(item_pairs_predict_list[i][2])
        if filmid_j==filmid1 and filmid_k==filmid2:
            pre_j_k=float(item_pairs_predict_list[i][3])
            return pre_j_k 
def search_filmscore(filmid,item_pairs_predict_list):
    for i in range(len(item_pairs_predict_list)):
        filmid_j=int(item_pairs_predict_list[i][1])
        filmid_k=int(item_pairs_predict_list[i][2])
        if filmid==filmid_j:
            score=int(item_pairs_predict_list[i][4])
            return score
        if filmid==filmid_k:
            score=int(item_pairs_predict_list[i][5])
            return score     
#greedy algorithm
def greedy_order(item_pairs_predict_list):
    potential_value={}
    rank_list=[]
    for i in range(len(item_pairs_predict_list)):
        filmid_j=int(item_pairs_predict_list[i][1])
        filmid_k=int(item_pairs_predict_list[i][2])
        pre_j_k=float(item_pairs_predict_list[i][3])
        if potential_value.has_key(filmid_j):
            potential_value[filmid_j]+=pre_j_k
        else:
            potential_value[filmid_j]=pre_j_k
        if potential_value.has_key(filmid_k):
            potential_value[filmid_k]-=pre_j_k
        else:
            potential_value[filmid_k]=-pre_j_k
    potential_value_list=list(potential_value.items())
    potential_value_list.sort(key=lambda x:(x[1],x[0]),reverse=False)
    while len(potential_value_list)!=0:
        max_filmid=int(potential_value_list.pop()[0])
        max_filmid_score=search_filmscore(max_filmid,item_pairs_predict_list)
        rank_list.append((max_filmid,max_filmid_score))
        #delete max_preference film for dict
        del potential_value[max_filmid]
        for i in range(len(potential_value)):
            filmid_j=int(potential_value.items()[i][0])
            if max_filmid<filmid_j:
                delta_pre=search_pre(max_filmid,filmid_j,item_pairs_predict_list)
                potential_value[filmid_j]+=delta_pre
            else:
                delta_pre=search_pre(filmid_j,max_filmid,item_pairs_predict_list)
                potential_value[filmid_j]-=delta_pre 
        potential_value_list=list(potential_value.items())
        potential_value_list.sort(key=lambda x:(x[1],x[0]),reverse=False) 
    return rank_list 
#source_file->matrix
def get_user_list(rate_file,user_num,item_num):
    ratefile=open(rate_file,'r')
    ratefilelist=ratefile.readlines()
    user_list=[[0 for i in range(item_num)] for j in range(user_num)]
    for i in range(len(ratefilelist)):
        userid=int(ratefilelist[i].split()[0])
        filmid=int(ratefilelist[i].split()[1])
        score=float(ratefilelist[i].split()[2])
        user_list[userid-1][filmid-1]=score
    ratefile.close()
    return user_list
def get_sim_list(sim_file,user_num):
    simfile=open(sim_file,'r')
    simfilelist=simfile.readlines()
    sim_list=[[0 for i in range(user_num)] for j in range(user_num)]
    for i in range(len(simfilelist)):
        user_sim_list=simfilelist[i].split()
        for j in range(len(user_sim_list)):
            sim=float(user_sim_list[j])
            sim_list[i][j]=sim
    simfile.close()
    return sim_list
def get_avg_score_list(avg_score_file):
    avgfile=open(avg_score_file,'r')
    avgfilelist=avgfile.readlines()
    avg_list=[]
    for i in range(len(avgfilelist)):
        avg=float(avgfilelist[i].split()[0])
        avg_list.append(avg)
    avgfile.close()
    return avg_list
