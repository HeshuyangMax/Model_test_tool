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
    cer = dis / len(ref)
    return cer


# 计算句错率
# ref: 标注答案的字符串列表
# hyp: 模型推理的结果字符串列表
# return: 句错率浮点型
def ser(ref: list[str], hyp: list[str]) -> float:

    total = len(ref)
    err = 0
    for i in range(total):
        cer = cer(ref[i], hyp[i])
        if cer == 0:
            err = err + 1
    ser = err / total
    return ser

if __name__ == "__main__":
    output = cer("你吃饭了吗", "你吃饭了吗")
    if output == 0:
        print("perfect")
    print(output)
