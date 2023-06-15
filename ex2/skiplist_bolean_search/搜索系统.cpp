#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <set>
#include <list>
#include <algorithm>
#include <sstream>
#include <stack>

#include "porter2_stemmer.h" // 导入Porter Stemmer库
#include "SkipList.h"     //导入实现的SkipList

class InvertedIndex {
public:
    void add_document(const std::string& document, int doc_id) {
        std::stringstream ss(document);
        std::string word;
        while (ss >> word) {
            std::string lower_word = to_lower(word);
            std::string stemmed_word = stem(lower_word);
            index[stemmed_word].insert(doc_id);
        }
        for (auto entry : index) {
            if (entry.second.size < 10)break; //数据太少没必要建表
            entry.second.renew();  // 更新 SkipList 索引层
        }
        
    }

    const SkipList& get_posting_list(const std::string& word) const {
        auto it = index.find(word);
        if (it == index.end()) {
            static const SkipList empty_set;
            return empty_set;
        }
        return it->second;
    }
    void print_index(int mod=0) const {
        for (auto entry : index) {
            std::cout << entry.first << ": ";
            entry.second.print(mod);
            std::cout << std::endl;
        }
    }


private:
    std::string stem(const std::string& word) {
        std::string stemmed_word = word;
        Porter2Stemmer::stem(stemmed_word);
        return stemmed_word;
    }

    std::string to_lower(const std::string& str) {
        std::string lower_str = str;
        std::transform(lower_str.begin(), lower_str.end(), lower_str.begin(),
            [](unsigned char c) { return std::tolower(c); });
        return lower_str;
    }

    std::unordered_map<std::string, SkipList> index;
};



class BooleanQuery {
public:
    BooleanQuery(const InvertedIndex& index) : index(index) {}

    SkipList query(const std::string& input) {
        std::stringstream ss(input);
        std::string token;
        std::stack<SkipList> operands;
        std::stack<char> operators;

        while (ss >> token) {
            token = to_lower(token);
            if (token == "and" || token == "or") {
                operators.push(token[0]);
            }
            else if (token == "(") {
                operators.push(token[0]);
            }
            else if (token == ")") {
                while (!operators.empty() && operators.top() != '(') {
                    apply_operator(operators.top(), operands);
                    operators.pop();
                }
                if (!operators.empty() && operators.top() == '(') {
                    operators.pop();
                }
            }
            else {
                std::string stemmed_word = stem(token);
                operands.push(index.get_posting_list(stemmed_word));
            }
        }
        
        while (!operators.empty()) {
            apply_operator(operators.top(), operands);
            //operands.top().print();
            operators.pop();
        }

        return operands.empty() ? SkipList() : operands.top();
    }

private:
    std::string to_lower(const std::string& str) {
        std::string lower_str = str;
        std::transform(lower_str.begin(), lower_str.end(), lower_str.begin(),
            [](unsigned char c) { return std::tolower(c); });
        return lower_str;
    }

    std::string stem(const std::string& word) {
        std::string stemmed_word = word;
        Porter2Stemmer::stem(stemmed_word);
        return stemmed_word;
    }

    void apply_operator(char op, std::stack<SkipList>& operands) {
        if (operands.size() < 2) return;
        SkipList right = operands.top();
        operands.pop();
        SkipList left = operands.top();
        operands.pop();
        SkipList result;

        if (op == 'a' || op == 'A') { // AND
            result = SkipList::boolean_and_ORI(left, right);
            //result = SkipList::boolean_and_OPT(left, right);
            //result.print(0);
        }
        else if (op == 'o' || op == 'O') { // OR
            result = SkipList::boolean_or(left, right);
        }
        operands.push(result);
    }

    const InvertedIndex& index;
};/*
int main(void) {
    SkipList skip_list1;
    SkipList skip_list2; 
    SkipList skip_list3;
    int arr[17] = { 3, 5, 9, 15, 24, 39, 60, 68, 75, 81, 84, 89, 92, 96, 97, 100, 115 };
    for(auto i:arr) { 
        skip_list1.insert(i); 
    }
    int arr2[6] = { 3,5, 96, 99 ,100, 101 } ;
    int arr3[5] = { 25, 60, 68, 120, 150 };
    for (auto i : arr2) {
        skip_list2.insert(i);
    }for (auto i : arr3) {
        skip_list3.insert(i);
    }
    skip_list1.renew();
    skip_list1.print(2);
    skip_list3.print(2);
    //skip_list3.print(1);
    //SkipList and_result = SkipList::boolean_and_OPT(skip_list1, skip_list2);
    SkipList and_result = SkipList::boolean_and_OPT(skip_list1, skip_list3);
    //跳表优化
    //SkipList and_result1 = SkipList::boolean_and_ORI(skip_list1, skip_list2);

    // SkipList or_result = SkipList::boolean_or(skip_list1, skip_list2);

     // Output the results here
    and_result.print(2);
    // or_result.print(0);
    return 0;    //调试跳表
}*/

int main() {
    std::string file_path;
    int query_count;
    file_path = "../files/HW1.txt";
    std::cout << "文件路径: " << file_path;
    std::ifstream file(file_path);

    if (!file.is_open()) {
        std::cerr << "无法打开文件！" << std::endl;
        return 1;
    }

    InvertedIndex index;
    std::string line;
    int doc_id = 1;
    while (std::getline(file, line)) {
        index.add_document(line, doc_id);
        doc_id++;
    }
    file.close();
    index.print_index(0);  //调试代码

    std::cout << "请输入查询次数: ";
    std::cin >> query_count;

    BooleanQuery boolean_query(index);
    std::cin.ignore();
    for (int i = 0; i < query_count; ++i) {
        std::string query;
        std::cout << "第" << i + 1 << "次查询，请输入查询" << ": ";
        std::getline(std::cin, query);
        SkipList SkipList_result = boolean_query.query(query);
        std::set<int>result = SkipList_result.turn_into_set();
        if (result.empty()) {
            std::cout << "没有找到结果！" << std::endl;
        }
        else {
            std::cout << "查询结果: ";
            for (int doc_id : result) {
                std::cout << doc_id << " ";
            }
            std::cout << std::endl;
        }
    }

    return 0;
}
