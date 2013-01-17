ins = open( "adult_data.txt", "r" )
array = []
for line in ins:
    if '?' not in line:
        array.append( line.replace(" ",""))
 
k = []  
for x in array:
    k.append(x.split(","))

k1 = []
for x in k:
    x.pop(0)
    x.pop(1)
    x.pop(2)
    x.pop(7)
    x.pop(7)
    x.pop(7)
    x.pop(7)
    x.pop(7)
    x.pop(6)
    x.pop(1)
    
    k1.append(x)
#print k1

z= [[],[],[],[],[]]
for x in range(len(k1)):
    for y in range(len(k1[0])):
        if k[x][y] not in z[y]:
            z[y].append(k[x][y])
        
print z

f = open('dataset_lenses.txt', 'w')
for x in k1:
    strng = "\t".join(x)    
    f.write(str(strng + '\n'))    
f.close()        



#for x in z:
#    print  len(x),x
    
    #" ".join(["132","432"])