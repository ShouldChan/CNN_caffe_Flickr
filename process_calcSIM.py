import numpy as np
import time
import multiprocessing

# caocao=np.load('./1.npy')
# pengpeng=np.load('./2.npy')

# num=float(caocao.T * pengpeng)
# denom=np.linalg.norm(caocao)*linalg.norm(pengpeng)
# cos=num/denom
# sim=0.5+0.5*cos
# print sim

# with open('./1.txt','r') as fread:
#   lines=fread.readlines()
#   for line in lines:
#       mtx=np.matrix(line)
#       print mtx

# mtx=np.loadtxt(open('./1.txt','rb'))
# print mtx

t0 = time.time()

image_dict = {}

with open('./Toro_photoID_DESCRIPTION.txt','r') as fi:
    lines = fi.readlines()
    for line in lines:
        tempData = line.strip().split('\t')
        photo_id,jpg_name = tempData[0],tempData[1]
        image_dict[jpg_name] = photo_id
print 'read image_dict done...'

featAll = {}

with open('./vector_Toro.txt','r') as fread:
    lines = fread.readlines()
    x = 0
    for line in lines:
        # print x
        x += 1
        featAll[x] = line
        # print line
print 'featAll done...', time.time() - t0

# print featAll[1]

global N
N = 39301
t1 = time.time()


def compute(start):
    simi_list = []
    for i in range(start, N):
        # print featAll[i]
        mtx_i = np.matrix(featAll[i])
        for j in range(start, N): 
        # print line
            if i != j:
                mtx_j = np.matrix(featAll[j])
                num = float(mtx_i * mtx_j.T)
                denom = np.linalg.norm(mtx_i) * np.linalg.norm(mtx_j)
                cos = num / denom
                sim = 0.5 + 0.5 * cos
                jpg_name_i = str(i) + '.jpg'
                jpg_name_j = str(j) + '.jpg'
                last_i = image_dict[jpg_name_i]
                last_j = image_dict[jpg_name_j]
                simi_list.append([last_i, last_j, sim])
                # print i,'->',j,'----',sim
            j += 1
        i += 1
    return simi_list
    # print 'compute done...', time.time() - t1

j=0
i=0
while j<39301:
    pool = multiprocessing.Pool(processes=4)

    for k in range(0, 4):
        j=j+k
        res = pool.apply_async(compute, (j))
    pool.close()
    pool.join()    

print 'muliwrite photoID_url elapsed: ', time.time() - t1


# writing
t2 = time.time()
fwrite = open('./Toro_similarity.txt','a+')
# for [last_i, last_j, sim] in simi_list:
#     fwrite.write(str(last_i)+'\t'+str(last_j)+'\t'+str(sim)+'\n')
# fwrite.close()
print 'write done...', time.time() - t2
