# 批量工具箱 (Batch Toolbox)

批量工具箱是一个功能强大的工具集合，用于批量处理文档、重命名文件和处理图像。它提供了一个简单易用的API接口，可以集成到各种应用程序中。

## 功能特点

### 文档处理
- Word文档批量查找替换
- Word文档合并
- Word文档内容提取
- Excel文档批量查找替换
- Excel文档合并

### 文件重命名
- 添加前缀/后缀
- 文本替换
- 序列化重命名
- 日期序列重命名
- 自定义序列重命名
- 从Excel导入重命名规则

### 图像处理
- 格式转换
- 调整大小
- 添加水印
- 应用滤镜

## 安装说明

### 后端安装

1. 确保已安装Python 3.8或更高版本
2. 克隆仓库
   ```
   git clone https://github.com/yourusername/batch-toolbox.git
   cd batch-toolbox/backend
   ```
3. 安装依赖
   ```
   pip install -r requirements.txt
   ```
4. 运行服务器
   ```
   python app.py
   ```
   服务器将在 http://localhost:8000 上运行

## API文档

启动服务器后，可以通过访问 http://localhost:8000/docs 查看完整的API文档。

### 主要API端点

#### Word文档处理
- `POST /api/word/find-replace` - 查找替换Word文档中的文本
- `POST /api/word/batch-find-replace` - 批量查找替换多个Word文档
- `POST /api/word/merge` - 合并多个Word文档
- `POST /api/word/extract` - 提取Word文档中的内容

#### Excel文档处理
- `POST /api/excel/find-replace` - 查找替换Excel文档中的文本
- `POST /api/excel/batch-find-replace` - 批量查找替换多个Excel文档
- `POST /api/excel/merge` - 合并多个Excel文档

#### 文件重命名
- `POST /api/rename/batch` - 批量重命名文件
- `POST /api/rename/sequence` - 序列化重命名文件
- `POST /api/rename/date-sequence` - 日期序列重命名文件
- `POST /api/rename/from-excel` - 从Excel导入重命名规则

#### 图像处理
- `POST /api/image/convert` - 转换图像格式
- `POST /api/image/resize` - 调整图像大小
- `POST /api/image/watermark` - 添加水印
- `POST /api/image/filter` - 应用滤镜
- `POST /api/image/batch-process` - 批量处理图像

## 使用示例

### 使用Python请求API

```python
import requests

# 查找替换Word文档中的文本
files = {'file': open('document.docx', 'rb')}
data = {'find_text': '原始文本', 'replace_text': '替换文本', 'use_regex': 'false'}
response = requests.post('http://localhost:8000/api/word/find-replace', files=files, data=data)

# 保存结果
with open('result.docx', 'wb') as f:
    f.write(response.content)
```

### 使用curl请求API

```bash
# 转换图像格式
curl -X POST "http://localhost:8000/api/image/convert" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg;type=image/jpeg" \
  -F "target_format=png" \
  -F "quality=90" \
  --output image.png
```

## 许可证

MIT