eus = [{i,(0,i)} for i in range(10)]
for e in eus:
    print(e)
for  e in eus:
    eus.pop({2,(0,2)})
print("")
for e in eus:
    print(e)