# -*- coding: utf-8 -*-

import random
import time

import sqlglot
from sqlglot.expressions import Expression
import pickle
import copy
from sqlglot_manager import ExpressionSetManager

# 2.11 todolist�?
# []插入和删�?
# 改进manager实现按照经验对节点分布进行插入删除，以及变异后更新manager
# 1w条的测试，主要测试fill

manager = None

def set_expression_manager(mgr):
    global manager
    manager = mgr
# 读取文件并解�? SQL �?�?
def process_sql_file(file_path: str, manager: ExpressionSetManager):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                sql = line.strip()  # 
                if sql.endswith(";"):
                    sql = sql[:-1]  # 
                if sql:
                    tree = sqlglot.parse_one(sql,read='mysql')
                    for node in tree.walk():
                        if node != tree:
                            manager.add_node(node, node.parent)
        # print("Finished processing SQL file.")
    except Exception as e:
        pass
        # print(f"Error processing SQL file: {e}")


class SQLRandomReplacer:
    def __init__(self):
        """
        """

    def check_func(self, tree):
        for node in tree.find_all(sqlglot.expressions.Select):
            # 忽略嵌�?�的查�??，仅检查顶层查询的 SELECT
            if node.parent is None:  # �?处理顶层查�??
                # 检�? SELECT �?�?否有聚合函数
                for child in node.find_all(sqlglot.expressions.Sum):
                    if child.parent == node:
                        return True
        return False

    def insert_delete(self, node):

        return node

    def replace_nodes(self, parsed_sql):
        """
        
        """
        mutation_num = 0
        root = 0
        for node in parsed_sql.walk():
            # print(parsed_sql)
            # print("1")
            if mutation_num >= 10:
                break
            # 插入替换
            if node.key == 'select':
                new_node = self.insert_delete(node)
                # print("INSERT OR DELETE")
                if new_node is not None:
                    node.replace(new_node)
                    mutation_num = mutation_num + 1
                    # print(parsed_sql)
                    continue

            # 跳过根节点（�?选）
            if node.parent is None:
                # print(2)
                continue
            # 调用随机节点生成函数生成新的节点

            for a in range(10):
                # print(3)
                new_node = manager.get_random_node(node.parent)
                if node.key == new_node.key:
                    # 执�?�替换操�?
                    if new_node is not None:
                        node.replace(new_node)
                        mutation_num = mutation_num + 1
                        # print(parsed_sql)
                        break

        return parsed_sql

    # based on experience insert&delete followed by the seeds
    def mutation(self, parsed_sql):
        mutation_num = 20
        for node in parsed_sql.walk(bfs=True):


            if mutation_num < 0:
                break
            if random.random() > 0.8:

                std_node = manager.get_random_node_v2(node)

                if std_node is not None:

                    std_key = [key for key, value in std_node.args.items() if value is not None]
                    node_key = [key for key, value in node.args.items() if value is not None]
                    # insert from std_node
                    if random.random() > 0.8:
                        for key in std_key:

                            if key not in node_key:
                                # node.args[key] = std_node.args[key]
                                # print([node])
                                node.set(key, std_node.args[key])
                                # print([node])
                                # print(node.sql())
                                mutation_num = mutation_num -1
                    if random.random() < 0.2:
                        for key in node_key:

                            if key not in std_key:
                                node.set(key, None)
                                mutation_num = mutation_num - 1
                # print(std_node)
                # print(node)
            #replace
            if random.random() > 0.5 and node.parent is not None:

                new_node = manager.get_random_node_v2(node)

                if new_node is not None and node.key == new_node.key:
                    node.replace(new_node)
                    mutation_num = mutation_num - 1

            try:
                # print(parsed_sql.sql(dialect='mysql'))
                current_sql = str(parsed_sql.sql(dialect='mysql'))+';'
                # print(current_sql)
                check_sql = sqlglot.parse(current_sql,read='mysql')
            except Exception as e:
                return None
            else:
                pass
                # print("correct")

        return parsed_sql

def get_mutated_sql(sql):
    # print("mmm")
    # print(sql)/home/SQLynx/srcs/sqlglot-pgsql/pg
    if manager is None:
        raise RuntimeError("ExpressionSetManager not initialized")
    # with open("memtest.txt", "a") as f:
    #     f.write(f"sqlglot_mutation mutation module expression_manager id: {id(manager)}\n")
    parsed = sqlglot.parse(sql,dialect='mysql')
    replacer = SQLRandomReplacer()

    new_sql = copy.deepcopy(random.choice(parsed))
    transformed_sql = replacer.mutation(new_sql)

    try:
        if transformed_sql is not None:
            check_sql = sqlglot.parse_one(transformed_sql.sql(dialect='mysql'),read='mysql')
    except Exception as e:
        # print("failed")
        return None
    else:
        # print("success")
        return transformed_sql.sql(dialect='mysql')

if __name__ == "__main__":
    start_time = time.time()
    file_path = "/home/SQLynx/srcs/sqlynx-mysql/mysql_seed.pkl"

    manager.load_from_file(file_path)
#from squirrel-pgsql
    sql = """
    CREATE TABLE v0 ( v1 INT , v2 INT , v3 INT CONSTRAINT xx CHECK ( v3 ) ) ;
    create index x on v0(v2, v3);
    insert into x(v3) values(1),(2);
    UPDATE v0 SET v3 = NULL ;
    select v3 from x;

    """
    sql2="""
    
    update v0 set v1 = 1 where v1=20;
    """
    parsed = sqlglot.parse(sql,dialect='mysql')
    print(parsed[0].args)
    replacer = SQLRandomReplacer()
    num = 0
    # 假�?�文件名
    output_file = "mutation-mysql.txt"
    with open(output_file, "a", encoding="utf-8") as f:
        for i in range(100):
            print(i)
            new_sql = copy.deepcopy(random.choice(parsed))
            print("choice")
            print(new_sql)
            transformed_sql = replacer.mutation(new_sql)

            try:
                print("!")
                if transformed_sql is not None:
                    check_sql = sqlglot.parse_one(transformed_sql.sql(dialect='mysql'),read='mysql')
                print("@")
            except Exception as e:
                print("failed")
                print(repr(transformed_sql))
            else:
                print("success")
                print(transformed_sql)
                if transformed_sql is not None:
                    f.write(transformed_sql.sql(dialect='mysql') + ";\n")
                # print(repr(transformed_sql))
                    num = num + 1

    print("success num:")
    print(num)
    end_time = time.time()
    
# 1w test
# success num:
# 9997
# 运�?�时�?: 167.36811637878418 �?
