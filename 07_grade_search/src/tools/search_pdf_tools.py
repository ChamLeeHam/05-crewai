import os.path

from chonkie import SemanticChunker
from crewai.tools import BaseTool
from markitdown import MarkItDown
from pydantic import BaseModel, Field, ConfigDict
from typing import Type, Any
from sentence_transformers import SentenceTransformer
from pymilvus import MilvusClient, FieldSchema, DataType, CollectionSchema, IndexType


class PDFSearchToolArgs(BaseModel):
    query: str = Field(..., description="要查询的内容")


class PDFSearchTool(BaseTool):
    name: str = "PDF检索工具"
    description: str = """
        从指定的PDF文件中检索用户的成绩信息，

        Args:
            query:查询的内容
        Returns:
            检索到的相关片段，多个结果直接使用分隔符隔开。
    """
    args_schema: Type[BaseModel] = PDFSearchToolArgs  # 定义工具需要的参数
    model_config = ConfigDict(extra="allow")  # 允许工具添加额外字段

    def __init__(self, file_path: str):
        super().__init__()  # 初始化工具信息
        self.file_path = file_path
        self.mode_path = os.path.abspath("model/bge-base-zh")
        self.embedding_model = SentenceTransformer(self.mode_path)
        self.client = MilvusClient(uri="http://localhost:19530", token="")
        self.embedding_dim = self.embedding_model.get_embedding_dimension()
        self.collection_name = "grade_collection"

        # 创建集合
        self._create_collection()

        # 加载文档
        self._process_document()

    def _create_collection(self):
        """创建Milvus集合和索引"""
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),  # 主键
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=65535),  # 来源文件名
            FieldSchema(name="document", dtype=DataType.VARCHAR, max_length=65535),  # 文本内容
            # 使用动态维度（768）
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.embedding_dim)  # 向量字段
        ]
        schema = CollectionSchema(fields=fields, description="成绩PDF检索集合")

        if not self.client.has_collection(self.collection_name):
            self.client.create_collection(collection_name=self.collection_name, schema=schema)
            index_params = self.client.prepare_index_params()
            index_params.add_index(
                field_name="embedding",
                index_type=IndexType.HNSW,
                metric_type="COSINE",  # L2 或 "COSINE"（BGE 推荐用 COSINE）
            )
            self.client.create_index(collection_name=self.collection_name, index_params=index_params)
            self.client.load_collection(self.collection_name)

    def _process_document(self):
        """切片-》向量化-》入库"""
        # 1. 读取PDF文件
        md = MarkItDown()
        raw_text = md.convert(self.file_path).text_content  # 将pdf文件当作markdown进行读取

        # 2. 语义切块， 相邻两个句子判断相似性，如果相似度大于0.5，则合并为一个chunk
        chunker = SemanticChunker(
            embedding_model=self.mode_path,  # 提供具体的模型路径
            threshold=0.5,
            chunk_size=100
        )
        chunks = chunker.chunk(raw_text)
        docs = [chunk.text for chunk in chunks]
        sources = [os.path.basename(self.file_path)] * len(docs)
        ids = list(range(len(docs)))

        # 3. 向量化
        embeddings = self._encode_texts(docs)

        # 4. 入库
        data = [
            {
                "id": ids[_i],
                "source": sources[_i],
                "document": docs[_i],
                "embedding": embeddings[_i]
            }
            for _i in range(len(docs))
        ]

        if data:
            self.client.insert(collection_name=self.collection_name, data=data)

    def _encode_texts(self, texts: list):
        return self.embedding_model.encode(texts, normalize_embeddings=True).tolist()

    def _run(
            self,
            query: str,
    ) -> str:
        """工具执行的具体过程:根据这个query进行相似度检索"""
        query_vector = self._encode_texts([query])[0]
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            anns_field="embedding",
            output_fields=["document"],
            limit=2
        )
        docs = [hit["entity"]["document"] for hit in results[0]]

        return "\n".join(docs) if docs else "未找到相关内容"


