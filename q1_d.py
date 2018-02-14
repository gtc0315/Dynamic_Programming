import numpy as np

# problem 1(d)
# [[freezing],[modest],[burning]]
T = np.array([[2.0/3,0.25,0],\
              [1.0/3,0.5,0.5],\
              [0,0.25,0.5]],dtype=np.float32)
p0 = np.array([[1],[0],[0]],dtype=np.float32)
p1 = T.dot(p0)
p2 = T.dot(p1)
p3 = T.dot(p2)
p4 = T.dot(p3)
total_probability = 0
cnt = 0

for s1 in range(3):
    for s2 in range(3):
        for s3 in range(3):
            for s4 in range(3):
                occurance = np.array([1,0,0]) # [freezing,modest,burning]
                for i in np.array([s1,s2,s3,s4]):
                    occurance[i] += 1
                if 0 in occurance: # didn't collect all three seasons
                    total_probability += p1[s1,0]*p2[s2,0]*p3[s3,0]*p4[s4,0]
                    cnt += 1
print total_probability, cnt

