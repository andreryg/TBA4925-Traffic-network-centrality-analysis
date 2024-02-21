import pandas as pd

testList = [1,2,3,4]

testListnavn = ["en", "to", "tre", "fire","null","dank"]
"""a = []
a.append(dict((v, [*testList, 0][i]) for i,v in enumerate(testListnavn)))
a.append(dict((v, [*testList, 0][i]) for i,v in enumerate(testListnavn)))

print(pd.DataFrame(a, columns=testListnavn))"""

new_list = []
for i,v in enumerate(testListnavn):
    if i%2 != 0 and i !=0:
        new_list.append([testListnavn[i-1],testListnavn[i]])
print(new_list)