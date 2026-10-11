age=int(input("请输入你的年龄："))
study_hours=int(input("你每天学习多少小时AI："))
experience = input("你有没有编程经验？（有/没有）：")
willingness = input("你每天愿意坚持学习吗？（愿意/不愿意）：")
if age >=18 and study_hours >= 1 and experience == "有" and willingness == "愿意": 
    print("你可以尝试直接进入 AI 应用开发！" )
elif age >=18 and study_hours >= 1 and experience == "没有" and willingness == "愿意":
    print("从 Python 开始，你完全来得及！" )
else:
    print("先建立稳定的学习习惯。") 