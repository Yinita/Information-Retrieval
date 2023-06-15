class InvertedIndex:
    # 倒排索引类，包含一个记录句子编号的列表和一个单词列表
    def __init__(self, words):
        self.line_list = []
        self.word_list = []
        self.inverted_index = {}
        dic = {}
        index = 0
        # 遍历每一行
        for line in words:
            self.line_list.append(line)
            tmp = line.split()
            for i in tmp:
                i = preprocess(i)
                if i not in dic:
                    dic[i] = 1
                    self.inverted_index[index] = []
                    self.word_list.append(i)
                    index += 1
        # 计算字典大小
        self.size = len(dic)
        self.word_list.sort()
        line_index = 0
        # 遍历每一行
        for line in self.line_list:
            tmp_line = line.split()
            # 对每一行的单词进行匹配并记录在字典中
            for word_in_line in tmp_line:
                self.insert(word_in_line, line_index)
            line_index += 1

    def insert(self, word, sentence_index):
        word = preprocess(word)
        word_index = find_index(word, self.word_list) # 在列表中找到单词的位置
        tmp = self.inverted_index[word_index]
        tmp.append(sentence_index)
        self.inverted_index[word_index] = tmp

    def search(self, word):
        index = find_index(word, self.word_list)
        if index == -1:  # 搜索失败
            return -1
        else:
            return self.inverted_index[index]

    def print(self, list=None):
        if list is None:
            print(self.word_list)  # 打印完整字典
            print(self.inverted_index)
        else:
            for i in list:
                if i > len(self.line_list):
                    print("字典错误")
                    return -1
                print(self.line_list[i])
            return

def preprocess(word):
    tmp = word
    tmp = tmp.replace(':', '')
    tmp = tmp.replace(',', '')
    tmp = tmp.replace('.', '')
    tmp = tmp.lower()
    return tmp

def find_index(word, list):
    index = 0  # 在列表中找到单词的索引
    for i in list:
        if word == i:
            return index
        else:
            index += 1
    return -1  # 非法单词


class Resolution:
    def __init__(self, sentence, inverted_index):
        self.result = []
        self.result = self.process(sentence, inverted_index)

    def processing(self, A, keyword, B, inverted_index):
        # A和B可以是1.书籍列表，2.单词，3.函数列表；如果是单词，它们都需要转换为列表
        if not isinstance(A, list):
            A = inverted_index.search(A)
        else:
            if not isinstance(A[0], int):
                A = self.resolve(A, inverted_index)

        if not isinstance(B, list):
            B = inverted_index.search(B)
        else:
            if not isinstance(B[0], int):
                B = self.resolve(B, inverted_index)
        # 现在A和B都是书籍列表
        result = []
        if keyword == 'AND':
            for i in A:
                if i in B:
                    result.append(i)
        if keyword == 'ANDNOT':
            for i in A:
                if i not in B:
                    result.append(i)
        if keyword == 'OR':
            result.extend(A)
            for i in B:
                if i not in result:
                    result.append(i)
            if result != []:
                result.sort()

        return result

    def resolve(self, command_list, Inverted_index):
        while len(command_list) > 2:
            # 如果长度大于2，则需要处理，如果长度为1，则直接返回
            # A command B，首先找到A，然后找到操作符，最后找到B
            if command_list[0] == '(':
                brackets_index = 1  # 括号数量 '('+1，')'-1
                for i in range(1, len(command_list)):
                    if command_list[i] == '(':
                        brackets_index += 1
                    if command_list[i] == ')':
                        brackets_index -= 1
                    if brackets_index == 0:
                        A = command_list[1:i]
                        command_list = command_list[i + 1:]
                        break
                if brackets_index != 0:
                    print("括号数量错误，请检查您的命令")
                    return -1
            else:
                A = command_list[0]
                command_list = command_list[1:]
            if not command_list:
                return self.resolve(A, Inverted_index)
            if command_list[0] == 'and' or command_list[0] == 'or':
                if command_list[0] == 'and' and command_list[1] == 'not':
                    keyword = 'ANDNOT'
                    command_list = command_list[2:]
                if command_list[0] == 'and':
                    keyword = 'AND'
                    command_list = command_list[1:]
                if command_list[0] == 'or':
                    keyword = 'OR'
                    command_list = command_list[1:]
                # 成功找到操作符
            else:
                print("错误，缺少操作符")
                return -1
            if command_list[0] == '(':
                brackets_index = 1
                for i in range(1, len(command_list)):
                    if command_list[i] == '(':
                        brackets_index += 1
                    if command_list[i] == ')':
                        brackets_index -= 1
                    if brackets_index == 0:
                        B = command_list[1:i]
                        command_list = command_list[i + 1:]
                        break
                if brackets_index != 0:
                    print("括号数量错误，请检查您的命令")
                    return -1
            else:
                B = command_list[0]
                command_list = command_list[1:]
            # 成功找到B
            command_list.insert(0, self.processing(A, keyword, B, Inverted_index))
            # 处理 A op B
            if len(command_list) == 1:
                if isinstance(command_list[0], list):
                    return command_list[0]
                else:
                    return Inverted_index.search(command_list[0])  # 只有一个单词

    def process(self, sentence, inverted_index):
        command_list = sentence.split()
        for i in range(len(command_list) - 1, -1, -1):  # 删除内部的()
            command_list[i] = preprocess(command_list[i])  # 将单词处理为小写
            index = 0
            while command_list[i][-1] == ')' and command_list[i] != ')':
                index += 1
                command_list[i] = command_list[i][:-1]
            for j in range(0, index):
                command_list.insert(i + 1, ')')  # 在下一个位置添加')'
            index = 0
            while command_list[i][0] == '(' and len(command_list[i]) != 1:
                index += 1
                command_list[i] = command_list[i][1:]
            for j in range(0, index):
                command_list.insert(i, '(') # 在当前位置添加'('
        result_list = self.resolve(command_list, inverted_index) # 开始解析
        print(result_list)
        return result_list


if __name__ == "__main__":
    file = open('D:\homework\\2023 -1l\IR\ex1\HW1.txt', 'r')
    dict = InvertedIndex(file)  # 创建倒排索引
    dict.print()
    n = input()
    for i in range(0, int(n)):
        command = input()
        answer = Resolution(command, dict)
        dict.print(answer.result)
    file.close()
