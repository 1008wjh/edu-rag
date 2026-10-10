# 该脚本用于: 文本预处理.
# 导入分词库
import jieba
# 导入日志
from base import logger

def preprocess_text(text):
    # 预处理文本
    logger.info("开始预处理文本")
    try:
        # 分词并转换为小写
        return jieba.lcut(text.lower())
    except AttributeError as e:
        # 记录预处理失败
        logger.error(f"文本预处理失败: {e}")
        # 返回空列表
        return []
if __name__ == "__main__":
    # 测试预处理函数
    print(preprocess_text("用上下文管理器实现函数运行时间的计算?"))
