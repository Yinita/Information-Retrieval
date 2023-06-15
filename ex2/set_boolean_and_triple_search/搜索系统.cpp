#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <sstream>
#include <stack>
#include <regex>  //正则
#include "porter2_stemmer.h" // 导入Porter Stemmer库

class InvertedIndex {
public:
    void add_document(const std::string& document, int doc_id) {
        std::stringstream ss(document);
        std::string word;
        int position = 0;
        while (ss >> word) {
            std::string lower_word = to_lower(word);  // 转换为小写字母格式
            std::string stemmed_word = stem(lower_word);
            index[stemmed_word][doc_id].insert(position);
            boolean_index[stemmed_word].insert(doc_id);
            position++;
        }
        boolean_index;
    }
    //无mod,查三元组；有的话，查布尔,用一个重载函数,仿佛不规范
    
    const std::set<int>& get_posting_list(const std::string& word,int mod) const {
        auto it = boolean_index.find(word);
        if (it == boolean_index.end()) {
            static const std::set<int> empty_set;
            return empty_set;
        }
        return it->second;
    }

    // 输出哈希表中所有键值对
    void print_index() const {
        for (const auto& entry : boolean_index) {
            std::cout << entry.first << ": ";
            for (const auto& doc_id : entry.second) {
                std::cout << doc_id << " ";
            }
            std::cout << std::endl;
        }
    }
    const std::map<int, std::set<int>>& get_posting_list(const std::string& word) const {
        auto it = index.find(word);
        if (it == index.end()) {
            static const std::map<int, std::set<int>> empty_map;
            return empty_map;
        }
        return it->second;

        /*if (it != index.end()) {
            for (const auto& entry : it->second) {
                std::cout << "Doc ID: " << entry.first << ", Positions: ";
                for (const auto& position : entry.second) {
                    std::cout << position << " ";
                }
                std::cout << std::endl;
            }
        }
        else {
            std::cout << "Word not found in the index" << std::endl;
        }*/
    }


    // 输出哈希表中所有键值对
    void print_pos_index() const {
        for (const auto& entry : index) {
            std::cout << entry.first << ": ";
            for (const auto& doc_id_pos : entry.second) {
                std::cout << "<" << doc_id_pos.first << ">: ";
                for (const auto& pos : doc_id_pos.second) {
                    std::cout << pos << " ";
                }
            }
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
    std::map<std::string, std::set<int>> boolean_index;
    std::map<std::string, std::map<int, std::set<int>>> index;
};


class BooleanQuery {
public:
    BooleanQuery(const InvertedIndex& index) : index(index) {}

    std::set<int> query(const std::string& input) {
        std::stringstream ss(input);
        std::string token;
        std::stack<std::set<int>> operands;
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
                operands.push(index.get_posting_list(stemmed_word, 0));
            }
        }

        while (!operators.empty()) {
            apply_operator(operators.top(), operands);
            operators.pop();
        }

        return operands.empty() ? std::set<int>() : operands.top();
    }
    std::vector<int> triplet_query(const std::string& term1, const std::string& term2, int proximity) {
        std::vector<int> results;   //容器存结果
        auto posting_list1 = index.get_posting_list(stem(to_lower(term1)));
        auto posting_list2 = index.get_posting_list(stem(to_lower(term2)));
        std::cout << "First word: \n";
        for (const auto& entry : posting_list1) {
            int key = entry.first;
            const std::set<int>& value_set = entry.second;

            std::cout << "Key: " << key << ", Values: ";

            for (const int& value : value_set) {
                std::cout << value << " ";
            }

            std::cout << std::endl;
        }std::cout << "Second word: \n";
        for (const auto& entry : posting_list2) {
            int key = entry.first;
            const std::set<int>& value_set = entry.second;

            std::cout << "Key: " << key << ", Values: ";

            for (const int& value : value_set) {
                std::cout << value << " ";
            }

            std::cout << std::endl;
        }/**/
        for (const auto& doc_positions1 : posting_list1) {
            int doc_id = doc_positions1.first;
            auto it = posting_list2.find(doc_id);
            if (it != posting_list2.end()) {
                const std::set<int>& positions1 = doc_positions1.second;
                const std::set<int>& positions2 = it->second;
                for (int pos1 : positions1) {
                    for (int pos2 : positions2) {
                        if (proximity > 0 && pos1 >= pos2 + 1 && pos1 <= pos2 + proximity) {
                            results.push_back(doc_id);
                            results.push_back(pos1);
                            results.push_back(pos2);
                        }
                        else if (proximity<0&&pos2 >= pos1 + 1 && pos2 <= pos1 + proximity) {
                            results.push_back(doc_id);
                            results.push_back(pos1);
                            results.push_back(pos2);
                        }
                    }
                }
            }
        }
        return results;
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

    void apply_operator(char op, std::stack<std::set<int>>& operands) {
        if (operands.size() < 2) return;
        std::set<int> right = operands.top();
        operands.pop();
        std::set<int> left = operands.top();
        operands.pop();
        std::set<int> result;

        if (op == 'a' || op == 'A') { // AND
            std::set_intersection(left.begin(), left.end(), right.begin(), right.end(),
                std::inserter(result, result.begin()));
        }
        else if (op == 'o' || op == 'O') { // OR
            std::set_union(left.begin(), left.end(), right.begin(), right.end(),
                std::inserter(result, result.begin()));
        }
        operands.push(result);
    }

    const InvertedIndex& index;
};

int main() {
    std::string file_path;
    int query_count;
    file_path = "../files/HW2.txt"; //修改新的文件目录
    std::cout << "文件路径: " << file_path<<std::endl;
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
    //index.print_pos_index();  //调试代码

    std::cout << "请输入查询次数: ";
    std::cin >> query_count;
    BooleanQuery boolean_query(index);
    std::cin.ignore();
    for (int i = 0; i < query_count; ++i) {
        std::string query;
        std::cout << "第" << i + 1 << "次查询，请输入查询" << ": ";
        std::getline(std::cin, query);
        std::set<int> result = boolean_query.query(query);
        if (result.empty()) {
            std::cout << "没有找到结果！" << std::endl;
        }
        else {
            std::cout << "查询结果: " ;
            for (int doc_id : result) {
                std::cout << doc_id << " ";
            }
            std::cout << std::endl;
        }
    }
    // Triplet query
    std::cout << "请输入三元组查询次数: ";
    int triplet_query_count;
    std::cin >> triplet_query_count;
    std::cin.ignore();
    for (int i = 0; i < triplet_query_count; ++i) {
        std::string term1, term2, input;
        int proximity=0;
        std::cout << "第" << i + 1 << "次三元组查询，请输入查询: ";
        std::getline(std::cin, input);

        std::regex re(R"(\s*\(\s*([\w-]+)\s*,\s*([\w-]+)\s*,\s*([-+]?\d+)\s*\)\s*)");
        std::smatch match;

        if (std::regex_match(input, match, re)) {
            term1 = match[1].str();
            term2 = match[2].str();
            proximity = std::stoi(match[3].str());
            //std::cout << term1 << " " << term2 << " " << proximity << " ";
            
        }
        else {
            std::cout << "Invalid query format. Please try again." << std::endl;
        }
        auto results = boolean_query.triplet_query(term1, term2, proximity);
        if (results.empty()) {
            std::cout << "没有找到结果！" << std::endl;
        }
        else {
            std::cout << "查询结果: " << std::endl;
            while (!results.empty()) {
                std::cout << "文档" << results[0] << "中," << term1 << " - " << results[1] + 1 << term2 << " - " << results[2] + 1;
                std::cout << std::endl;
                results.erase(results.begin()); results.erase(results.begin()); results.erase(results.begin());
            }
            
            
        }
    }
    return 0;
}


