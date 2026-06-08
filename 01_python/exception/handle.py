try:
    x = int(input("请输入数字: "))
    print(10 / x)

except ValueError:
    print("输入不是数字")

except ZeroDivisionError:
    print("不能除以0")

finally:
    print("程序结束")