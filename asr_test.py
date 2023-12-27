from Levenshtein import *
# 计算两个字符串的最短编辑距离
# ref: 标注答案字符串
# hyp: 模型推理结果字符串
# return: 整型编辑距离
def levenshtein_distance(ref: str, hyp: str) -> int:
    assert type(ref) == str
    assert type(hyp) == str

    row = len(ref) + 1
    column = len(hyp) + 1

    cache = [ [0] * column for i in range(row) ]

    for i in range(row):
        for j in range(column):
            if i == 0 and j == 0:
                cache[i][j] = 0
            elif i == 0 and j != 0:
                cache[i][j] = j
            elif j == 0 and i != 0:
                cache[i][j] = i
            else:
                if ref[i - 1] == hyp[j - 1]:
                    cache[i][j] = cache[i - 1][j - 1]
                else:
                    replace = cache[i - 1][j - 1] + 1
                    insert = cache[i][j - 1] + 1
                    remove = cache[i - 1][j] + 1
 
                    cache[i][j] = min(replace, insert, remove)

    return cache[row - 1][column - 1]      

# 计算字错率
# ref: 标注答案字符串
# hyp: 模型推理结果字符串
# return: 字错率浮点型
def cer(ref: str, hyp: str) -> float:
    assert type(ref) == str
    assert type(hyp) == str

    dis = levenshtein_distance(ref, hyp)
    cerOutput = dis / len(ref)
    return cerOutput

# 计算句错率
# ref: 标注答案的字符串列表
# hyp: 模型推理的结果字符串列表
# return: 句错率浮点型
def ser(ref: list[str], hyp: list[str]) -> float:
    assert type(ref) == list
    assert type(hyp) == list
    assert len(ref) == len(hyp)

    total = len(ref)
    cerOutput = 0.0
    err = 0
    for i in range(total):
        cerOutput = cer(ref[i], hyp[i])
        if cerOutput == 0.0:
            err = err + 1
    serOutput = err / total
    return serOutput

if __name__ == "__main__":
    # levenstein距离检查
    refstr = "你吃饭了吗"
    hypstr = "你有没有吃饭"
    dis0 = distance(refstr, hypstr)
    dis1 = levenshtein_distance(refstr, hypstr)
    print("dis0: ")
    print(dis0)
    print("dis1: ")
    print(dis1)

    # 字错率测试，应输出正确结果
    output0 = cer("你吃饭了吗", "你吃饭了吗")
    print(output0)

    # 句错率测试，应输出正确结果
    ref1 = ["我准备睡觉了", "你吃饭了吗"]
    hyp1 = ["我准备睡了", "你吃饭了吗"]
    output1 = ser(ref=ref1, hyp=hyp1)
    print(output1)

    # 句错率测试，应报错说明2个list长度不一致
    ref2 = ["我准备睡觉了"]
    hyp2 = ["我准备睡了", "你吃饭了吗"]
    output2 = ser(ref=ref2, hyp=hyp2)
    print(output2)
