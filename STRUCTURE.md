# 批量工具箱目录结构

```
batch-toolbox/
├── backend/                  # 后端代码目录
│   ├── app.py                # 主应用程序文件，提供API接口
│   ├── requirements.txt      # 依赖包列表
│   └── modules/              # 功能模块目录
│       ├── word_processor.py # Word文档处理模块
│       ├── excel_processor.py# Excel文档处理模块
│       ├── file_renamer.py   # 文件重命名模块
│       └── image_processor.py# 图像处理模块
├── README.md                 # 项目说明文件
├── STRUCTURE.md              # 目录结构说明文件
└── start.sh                  # 启动脚本
```

## 模块说明

### Word文档处理模块 (word_processor.py)
提供Word文档的查找替换、合并、内容提取等功能。

### Excel文档处理模块 (excel_processor.py)
提供Excel文档的查找替换、合并等功能。

### 文件重命名模块 (file_renamer.py)
提供文件的批量重命名功能，包括添加前缀/后缀、文本替换、序列化重命名等。

### 图像处理模块 (image_processor.py)
提供图像的格式转换、调整大小、添加水印、应用滤镜等功能。

## API接口

API接口由app.py提供，包括以下几类：

1. Word文档处理API
2. Excel文档处理API
3. 文件重命名API
4. 图像处理API

详细的API文档可以在启动服务器后通过访问 http://localhost:8000/docs 查看。