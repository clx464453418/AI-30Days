def study_check(name, hours):
    if hours>=3 :
        return name +"今天学习非常努力"
    elif hours>=1:
        return name+"今天完成了学习任务"
    else:
        return name+"今天学习时间不足！"


n=0
while n<3:
    name=input("请输入学生姓名:")
    hours=int(input("请输入学习小时数量:"))
    print(study_check(name,hours))
    n=n+1