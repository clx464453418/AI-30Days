n=int(input("请输入你想要实现的目标数量："))
goals=[]
for i in range(n):
    goals.append(input("请输入你第"+str(i+1)+"个目标："))
for i in range(n):
    print("第"+str(i+1)+"个目标是:"+goals[i])

print("你总共输入了"+str(len(goals))+"个目标")