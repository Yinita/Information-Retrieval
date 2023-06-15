#include "SkipList.h"
int STEP = 0;
// 定义构造函数
SkipList::SkipList() : levels(LAYER), size(0), head(new Node(-1)) {
    for (auto i : head->forward) i = nullptr;
}
void SkipList::insert(int value) {
    Node* current = head;
    Node* insert_value = new Node(value);
    insert_value->forward.resize(levels, nullptr);
    size++;
    //更新主表
    while (current->forward[0] && current->forward[0]->value < value) {
        current = current->forward[0];
    }
    insert_value->forward[0] = current->forward[0];
    current->forward[0] = insert_value;
}

void SkipList::renew() {
        if (!head->forward[0]) {
            std::cerr << "表空无法更新！" << std::endl;
            return;
        }

        // 删除当前所有层（除了基本层）
        for (int i = 1; i < levels; ++i) {
            head->forward[i] = nullptr;
        }
        int cur_size = size;
        // 计算每个级别的步长
        std::vector<int> steps(levels);
        steps[0] = 1;
        for (int i = 1; i < levels; ++i) {
            cur_size=sqrt(cur_size);
            steps[i] = size/ cur_size;
        }

        // 使用容器存储每层的指针
        std::vector<Node*> level_pointers(levels, head);

        // 为每个级别添加索引
        for (int current_level = 1; current_level < levels; ++current_level) {
            Node* current = head->forward[0];
            int counter = 0;

            while (current) {
                if (counter % steps[current_level] == 0) {
                    // 确保 forward 向量足够大
                    if (current_level >= current->forward.size()) {
                        current->forward.resize(current_level + 1, nullptr);
                    }
                    if (current_level >= level_pointers[current_level]->forward.size()) {
                        level_pointers[current_level]->forward.resize(current_level + 1, nullptr);
                    }

                    level_pointers[current_level]->forward[current_level] = current;
                    level_pointers[current_level] = level_pointers[current_level]->forward[current_level];
                }
                current = current->forward[0];
                counter++;
            }
        }
    }

SkipList SkipList::boolean_and(const SkipList& lhs, const SkipList& rhs) {
    if (lhs.size > 10) {//大小大于10才开优化
        std::cout << "using boolean_and_OPT"<<std::endl;
        return boolean_and_OPT(lhs,rhs);
    }
    else if (rhs.size > 10) {
        std::cout << "using boolean_and_OPT" << std::endl;
        return boolean_and_OPT(rhs,lhs);
    }
    
    else {
        std::cout << "using boolean_and_ORI" << std::endl;
        return boolean_and_ORI(lhs, rhs);
    }
}

SkipList SkipList::boolean_and_ORI(const SkipList& lhs, const SkipList& rhs) {
        SkipList result;
        Node* lhs_current = lhs.head->forward[0];
        Node* rhs_current = rhs.head->forward[0];

        while (lhs_current && rhs_current) {
            //无优化，单纯遍历
            std::cout << "step "<<STEP << lhs_current->value << " " << rhs_current->value<<std::endl;//debug
            if (lhs_current->value < rhs_current->value) {
                lhs_current = lhs_current->forward[0];
            }
            else if (lhs_current->value > rhs_current->value) {
                rhs_current = rhs_current->forward[0];
            }
            else {
                result.insert(lhs_current->value);
                lhs_current = lhs_current->forward[0];
                rhs_current = rhs_current->forward[0];
            }
        }
        STEP = 0;//debug
        return result;
    }
SkipList SkipList::boolean_and_OPT(const SkipList& lhs, const SkipList& rhs) {
    SkipList result;

    Node* rhs_current = rhs.head->forward[0];
    Node* cur = lhs.head->forward[0]; //第一个都是一样的
    std::vector<Node*> lhs_prevs(lhs.levels);
    for (auto i = 0;  i < lhs.levels; i++) {
        lhs_prevs[i]= lhs.head->forward[i];
    }
    while (rhs_current) {
        cur = lhs_prevs[lhs.levels - 1];  //更新cur
        for (int i = lhs.levels - 1; i >= 0; i--) {
            std::cout << "第" << i << "行索引:" << std::endl;
            if (cur->value >= rhs_current->value) {  //刚刚好第一个就是或者已经大于了
                STEP++;
                std::cout << "step-" << STEP << " " << cur->value << "=" << rhs_current->value << std::endl;//debug
                if (cur->value == rhs_current->value) {
                    result.insert(rhs_current->value);
                    rhs_current = rhs_current->forward[0];
                }
            }
            while (cur->forward[i] && cur->forward[i]->value < rhs_current->value) {
                cur = cur->forward[i];
                STEP++;
                std::cout << "step-" << STEP << " " << cur->value << "<" << rhs_current->value << std::endl;//debug

            }
            if (cur->forward[i] && cur->forward[i]->value > rhs_current->value) {
                STEP++;
                std::cout << "step-" << STEP << " " << cur->forward[i]->value << ">" << rhs_current->value << std::endl;//debug
            }
            if (cur->forward[i] && cur->forward[i]->value == rhs_current->value) {
                cur = cur->forward[i];   //已经找到，现在跑掉剩下的索引进行优化即可
                STEP++;
                std::cout << "step-" << STEP << " " << cur->value << "=" << rhs_current->value << std::endl;//debug
                for (int j = i; j >= 0; j--)lhs_prevs[j] = cur; //优化，相当于将剩下的每一行索引的指针都固定到最近值
                break;
            }
            for (int j = i; j >= 0; j--)lhs_prevs[j] = cur; //优化，相当于将剩下的每一行索引的指针都固定到最近值
        }
        if (cur->value == rhs_current->value)result.insert(rhs_current->value);
        rhs_current = rhs_current->forward[0];// 移动到 rhs 链表的下一个节点
    }

    return result;
}





SkipList SkipList::boolean_or(const SkipList& lhs, const SkipList& rhs) {
        SkipList result;
        Node* lhs_current = lhs.head->forward[0];
        Node* rhs_current = rhs.head->forward[0];

        while (lhs_current || rhs_current) {
            if (lhs_current && rhs_current) {
                if (lhs_current->value < rhs_current->value) {
                    result.insert(lhs_current->value);
                    lhs_current = lhs_current->forward[0];
                }
                else if (lhs_current->value > rhs_current->value) {
                    result.insert(rhs_current->value);
                    rhs_current = rhs_current->forward[0];
                }
                else {
                    result.insert(lhs_current->value);
                    lhs_current = lhs_current->forward[0];
                    rhs_current = rhs_current->forward[0];
                }
            }
            else if (lhs_current) {
                result.insert(lhs_current->value);
                lhs_current = lhs_current->forward[0];
            }
            else {
                result.insert(rhs_current->value);
                rhs_current = rhs_current->forward[0];
            }
        }
        return result;
    }

void SkipList::print(int mod=0) {
    if (mod == 0) {
        Node* node = head->forward[0];
        while (node != nullptr) {
            std::cout << node->value << " ";
            node = node->forward[0];
        }
    }
    if (mod == 2) {
        for (int i = 0; i < levels; i++) {
            Node* node = head->forward[i];
            std::cout << "第" << i << "层:";
            while (node != nullptr) {
                std::cout << node->value << " ";
                node = node->forward[i];
            }
            std::cout <<std::endl;
        }
    }
    else{
        for (int i = 0; i < levels; i++) {
            Node* node = head->forward[i];
            std::cout << "第" << i << "层:";
            int tmp = 0;
            while (node != nullptr) {
                tmp++;
                node = node->forward[i];
            }
            std::cout << tmp << std::endl;
        }
    }
}

std::set<int> SkipList::turn_into_set() {
    Node* node = head->forward[0];
    std::set<int> result;
    while (node != nullptr) {
        result.insert(node->value);
        node = node->forward[0];
    }
    return result; 
}

SkipList::Node::Node(int value, int level) : value(value), forward(level, nullptr) {
}
