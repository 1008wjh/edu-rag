# 该脚本用于: MySQL数据库的基础操作.
import pymysql
import pandas as pd
import  sys,os
current_dir=os.path.dirname(os.path.abspath(__file__))
module_dir=os.path.dirname(current_dir)
project_root=os.path.dirname(module_dir)
#print(project_root)
sys.path.insert(0,project_root)
from base import config,logger
class MySQLClient:
    def __init__(self):
        self.logger = logger
        try:
            self.connection = pymysql.connect(
                host=config.MYSQL_HOST,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                db=config.MYSQL_DATABASE,
                #charset='utf8mb4',
                #cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor=self.connection.cursor()
            self.logger.info("MySQLClient 连接成功")
        except Exception as e:
            self.logger.error("MySQLClient 连接失败: %s" % e)
            raise

    def create_table(self):
        create_table_query = '''
                             CREATE TABLE IF NOT EXISTS jpkb \
                             ( \
                                 id           INT AUTO_INCREMENT PRIMARY KEY, \
                                 subject_name VARCHAR(20), \
                                 question     VARCHAR(1000), \
                                 answer       VARCHAR(1000) \
                             ) \
                             '''
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            logger.info("建表语句执行成功！")
        except Exception as e:
            logger.error("建表语句执行失败: {}".format(e))
            raise

    def insert_data(self, csv_path):
        data_frame = pd.read_csv(csv_path)
        #print(data_frame.head())
        try:
            for _, row in data_frame.iterrows():
                question = row['问题']
                answer = row['答案']
                subject = row['学科名称']
                # 防注入
                # insert into jpkb (question, answer, subject_name) values ('a','a','a');drop table jpkb
                sql = 'insert into jpkb (question, answer, subject_name) values (%s, %s, %s)'
                self.cursor.execute(sql, (question, answer, subject))
            # 把这几百条数据的提交作为一次事务，要么全部成功，要不全部失败
            self.connection.commit()
            logger.info("输入导入成功，共：{}条".format(data_frame.count()))
        except Exception as e:
            # 事务回滚
            self.connection.rollback()
            logger.error("数据导入失败: {}".format(e))

    def fetch_questions(self):
        try:
            sql = "select question from jpkb"
            self.cursor.execute(sql)
            # tuple[tuple] -> [条数=467，列=1]
            results = self.cursor.fetchall()
            # row in results ：拿到每条数据（包含多个列）
            # row[0] ：拿到question列
            questions = [row[0] for row in results]
            logger.info("获取到了所有的问题：{}条".format(len(questions)))
            return questions
        except Exception as e:
            logger.error("获取所有的问题失败: {}".format(e))
            return []

    def fetch_answer(self, question):
        try:
            sql = "select answer from jpkb where question = %s"
            self.cursor.execute(sql, (question,))
            result = self.cursor.fetchone()
            if result:
                logger.info("获取问题: {} 对应的答案成功".format(question))
                return result[0]
            else:
                logger.error("没有找到问题对应的答案: {}".format(question))
                return None
        except Exception as e:
            logger.error("查询问题对应的答案失败: {}".format(e))
            return None

    def close(self):
        # 关闭数据库连接
        try:
            self.cursor.close()
            # 关闭连接
            self.connection.close()
            # 记录关闭成功
            self.logger.info("MySQL 连接已关闭")
        except pymysql.MySQLError as e:
            # 记录关闭失败
            self.logger.error(f"关闭连接失败: {e}")
if __name__ =='__main__':
    mysql_client=MySQLClient()
    mysql_client.create_table()
    mysql_client.insert_data("E:\integrated_qa_system\mysql_qa\data\JP学科知识问答.csv")
    #mysql_client.fetch_questions()
    #print(mysql_client.fetch_answer("用上下文管理器实现函数运行时间的计算?"))
    mysql_client.close()