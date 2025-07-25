import os
import shutil
import tempfile
import uuid
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from modules.word_processor import WordProcessor
from modules.excel_processor import ExcelProcessor
from modules.file_renamer import FileRenamer
from modules.image_processor import ImageProcessor

app = FastAPI(title="批量工具箱API", description="提供文档处理、文件重命名和图像处理功能")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
# 由于应用程序是从backend目录启动的，使用相对路径"../"指向项目根目录
app.mount("/", StaticFiles(directory="../", html=True), name="static")

# 创建临时文件夹
TEMP_DIR = os.path.join(tempfile.gettempdir(), "batch-toolbox")
os.makedirs(TEMP_DIR, exist_ok=True)

# 创建上传文件夹
UPLOAD_DIR = os.path.join(TEMP_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 创建输出文件夹
OUTPUT_DIR = os.path.join(TEMP_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 定义请求模型
class FindReplaceRequest(BaseModel):
    find_text: str
    replace_text: str
    use_regex: bool = False

class BatchFindReplaceRequest(BaseModel):
    replacements: List[Dict[str, str]]
    use_regex: bool = False

class ResizeImageRequest(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    keep_aspect_ratio: bool = True

class WatermarkRequest(BaseModel):
    text: Optional[str] = None
    position: str = "center"
    opacity: float = 0.5
    rotation: int = 0

class RenameRequest(BaseModel):
    operation: str  # "add_prefix", "add_suffix", "replace_text", "delete_text", "sequence", "date_sequence", "custom_sequence"
    params: Dict[str, Any]

class FilterRequest(BaseModel):
    filter_type: str
    intensity: float = 1.0

# 工具函数
def save_upload_file(upload_file: UploadFile) -> str:
    """保存上传的文件并返回文件路径"""
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(upload_file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_path

def create_output_path(original_filename: str, suffix: str = "") -> str:
    """创建输出文件路径"""
    file_id = str(uuid.uuid4())
    file_name, file_extension = os.path.splitext(original_filename)
    output_filename = f"{file_name}_{suffix}{file_extension}" if suffix else f"{file_name}{file_extension}"
    return os.path.join(OUTPUT_DIR, f"{file_id}_{output_filename}")

# API路由
@app.get("/api/status")
def read_root():
    return {"message": "批量工具箱API服务正在运行"}

# Word文档处理API
@app.post("/api/word/find-replace")
async def word_find_replace(
    file: UploadFile = File(...),
    find_text: str = Form(...),
    replace_text: str = Form(...),
    use_regex: bool = Form(False)
):
    try:
        # 保存上传的文件
        file_path = save_upload_file(file)
        
        # 创建输出路径
        output_path = create_output_path(file.filename, "replaced")
        
        # 执行查找替换
        result_path = WordProcessor.find_replace(file_path, find_text, replace_text, use_regex, os.path.dirname(output_path))
        
        # 返回处理后的文件
        return FileResponse(
            path=result_path,
            filename=os.path.basename(output_path),
            media_type="application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

@app.post("/api/word/batch-find-replace")
async def word_batch_find_replace(
    files: List[UploadFile] = File(...),
    request: str = Form(...)
):
    import json
    try:
        # 解析请求
        req_data = json.loads(request)
        replacements = [(item["find_text"], item["replace_text"]) for item in req_data["replacements"]]
        use_regex = req_data.get("use_regex", False)
        
        # 保存上传的文件
        file_paths = [save_upload_file(file) for file in files]
        
        # 创建输出目录
        output_dir = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
        os.makedirs(output_dir, exist_ok=True)
        
        # 执行批量查找替换
        result_paths = WordProcessor.batch_find_replace(file_paths, replacements, use_regex, output_dir)
        
        # 创建ZIP文件
        zip_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_batch_replaced.zip")
        shutil.make_archive(zip_path[:-4], 'zip', output_dir)
        
        # 返回ZIP文件
        return FileResponse(
            path=zip_path,
            filename="batch_replaced.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        for file_path in locals().get('file_paths', []):
            if os.path.exists(file_path):
                os.remove(file_path)
        if 'output_dir' in locals() and os.path.exists(output_dir):
            shutil.rmtree(output_dir)

@app.post("/api/word/merge")
async def word_merge(
    files: List[UploadFile] = File(...)
):
    try:
        # 保存上传的文件
        file_paths = [save_upload_file(file) for file in files]
        
        # 创建输出路径
        output_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_merged.docx")
        
        # 执行合并
        result_path = WordProcessor.merge_documents(file_paths, output_path)
        
        # 返回处理后的文件
        return FileResponse(
            path=result_path,
            filename="merged.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        for file_path in locals().get('file_paths', []):
            if os.path.exists(file_path):
                os.remove(file_path)

@app.post("/api/word/extract")
async def word_extract(
    file: UploadFile = File(...),
    extract_type: str = Form(...)
):
    try:
        # 保存上传的文件
        file_path = save_upload_file(file)
        
        # 创建输出路径
        output_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_extracted.txt")
        
        # 执行提取
        result_path = WordProcessor.extract_content(file_path, output_path, extract_type)
        
        # 返回处理后的文件
        return FileResponse(
            path=result_path,
            filename="extracted_content.txt",
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

# Excel文档处理API
@app.post("/api/excel/find-replace")
async def excel_find_replace(
    file: UploadFile = File(...),
    find_text: str = Form(...),
    replace_text: str = Form(...),
    sheet_range: Optional[str] = Form(None),
    use_regex: bool = Form(False)
):
    try:
        # 保存上传的文件
        file_path = save_upload_file(file)
        
        # 创建输出路径
        output_path = create_output_path(file.filename, "replaced")
        
        # 执行查找替换
        result_path = ExcelProcessor.find_replace(file_path, find_text, replace_text, sheet_range, use_regex, os.path.dirname(output_path))
        
        # 返回处理后的文件
        return FileResponse(
            path=result_path,
            filename=os.path.basename(output_path),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

@app.post("/api/excel/batch-find-replace")
async def excel_batch_find_replace(
    files: List[UploadFile] = File(...),
    request: str = Form(...)
):
    import json
    try:
        # 解析请求
        req_data = json.loads(request)
        replacements = [(item["find_text"], item["replace_text"]) for item in req_data["replacements"]]
        sheet_range = req_data.get("sheet_range")
        use_regex = req_data.get("use_regex", False)
        
        # 保存上传的文件
        file_paths = [save_upload_file(file) for file in files]
        
        # 创建输出目录
        output_dir = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
        os.makedirs(output_dir, exist_ok=True)
        
        # 执行批量查找替换
        result_paths = ExcelProcessor.batch_find_replace(file_paths, replacements, sheet_range, use_regex, output_dir)
        
        # 创建ZIP文件
        zip_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_batch_replaced.zip")
        shutil.make_archive(zip_path[:-4], 'zip', output_dir)
        
        # 返回ZIP文件
        return FileResponse(
            path=zip_path,
            filename="batch_replaced.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        for file_path in locals().get('file_paths', []):
            if os.path.exists(file_path):
                os.remove(file_path)
        if 'output_dir' in locals() and os.path.exists(output_dir):
            shutil.rmtree(output_dir)

@app.post("/api/excel/merge")
async def excel_merge(
    files: List[UploadFile] = File(...),
    merge_type: str = Form(...),
    remove_duplicates: bool = Form(False)
):
    try:
        # 保存上传的文件
        file_paths = [save_upload_file(file) for file in files]
        
        # 创建输出路径
        output_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_merged.xlsx")
        
        # 执行合并
        result_path = ExcelProcessor.merge_excel_files(file_paths, merge_type, output_path, remove_duplicates)
        
        # 返回处理后的文件
        return FileResponse(
            path=result_path,
            filename="merged.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        for file_path in locals().get('file_paths', []):
            if os.path.exists(file_path):
                os.remove(file_path)

# 文件重命名API
@app.post("/api/rename/batch")
async def batch_rename(
    files: List[UploadFile] = File(...),
    request: str = Form(...)
):
    import json
    try:
        # 解析请求
        req_data = json.loads(request)
        operations = req_data["operations"]
        
        # 保存上传的文件
        file_paths = [save_upload_file(file) for file in files]
        
        # 创建输出目录
        output_dir = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
        os.makedirs(output_dir, exist_ok=True)
        
        # 执行批量重命名
        result_paths = FileRenamer.batch_rename(file_paths, operations, output_dir)
        
        # 创建ZIP文件
        zip_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_renamed.zip")
        shutil.make_archive(zip_path[:-4], 'zip', output_dir)
        
        # 返回ZIP文件
        return FileResponse(
            path=zip_path,
            filename="renamed_files.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        for file_path in locals().get('file_paths', []):
            if os.path.exists(file_path):
                os.remove(file_path)
        if 'output_dir' in locals() and os.path.exists(output_dir):
            shutil.rmtree(output_dir)

@app.post("/api/rename/sequence")
async def sequence_rename(
    files: List[UploadFile] = File(...),
    pattern: str = Form(...),
    start_number: int = Form(1),
    step: int = Form(1),
    padding: int = Form(1)
):
    try:
        # 保存上传的文件
        file_paths = [save_upload_file(file) for file in files]
        
        # 创建输出目录
        output_dir = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
        os.makedirs(output_dir, exist_ok=True)
        
        # 执行序列重命名
        result_paths = FileRenamer.sequence_rename(file_paths, pattern, start_number, step, padding, output_dir)
        
        # 创建ZIP文件
        zip_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_renamed.zip")
        shutil.make_archive(zip_path[:-4], 'zip', output_dir)
        
        # 返回ZIP文件
        return FileResponse(
            path=zip_path,
            filename="renamed_files.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        for file_path in locals().get('file_paths', []):
            if os.path.exists(file_path):
                os.remove(file_path)
        if 'output_dir' in locals() and os.path.exists(output_dir):
            shutil.rmtree(output_dir)

@app.post("/api/rename/date-sequence")
async def date_sequence_rename(
    files: List[UploadFile] = File(...),
    pattern: str = Form(...),
    date_format: str = Form("%Y%m%d"),
    start_date: Optional[str] = Form(None),
    days_step: int = Form(1)
):
    try:
        # 保存上传的文件
        file_paths = [save_upload_file(file) for file in files]
        
        # 创建输出目录
        output_dir = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
        os.makedirs(output_dir, exist_ok=True)
        
        # 执行日期序列重命名
        result_paths = FileRenamer.date_sequence_rename(file_paths, pattern, date_format, start_date, days_step, output_dir)
        
        # 创建ZIP文件
        zip_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_renamed.zip")
        shutil.make_archive(zip_path[:-4], 'zip', output_dir)
        
        # 返回ZIP文件
        return FileResponse(
            path=zip_path,
            filename="renamed_files.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        for file_path in locals().get('file_paths', []):
            if os.path.exists(file_path):
                os.remove(file_path)
        if 'output_dir' in locals() and os.path.exists(output_dir):
            shutil.rmtree(output_dir)

@app.post("/api/rename/from-excel")
async def rename_from_excel(
    files: List[UploadFile] = File(...),
    excel_file: UploadFile = File(...),
    name_column: str = Form(...)
):
    try:
        # 保存上传的文件
        file_paths = [save_upload_file(file) for file in files]
        excel_path = save_upload_file(excel_file)
        
        # 创建输出目录
        output_dir = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
        os.makedirs(output_dir, exist_ok=True)
        
        # 执行从Excel导入重命名
        result_paths = FileRenamer.rename_from_excel(file_paths, excel_path, name_column, output_dir)
        
        # 创建ZIP文件
        zip_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_renamed.zip")
        shutil.make_archive(zip_path[:-4], 'zip', output_dir)
        
        # 返回ZIP文件
        return FileResponse(
            path=zip_path,
            filename="renamed_files.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        for file_path in locals().get('file_paths', []):
            if os.path.exists(file_path):
                os.remove(file_path)
        if 'excel_path' in locals() and os.path.exists(excel_path):
            os.remove(excel_path)
        if 'output_dir' in locals() and os.path.exists(output_dir):
            shutil.rmtree(output_dir)

# 图像处理API
@app.post("/api/image/convert")
async def convert_image(
    file: UploadFile = File(...),
    target_format: str = Form(...),
    quality: int = Form(90)
):
    try:
        # 保存上传的文件
        file_path = save_upload_file(file)
        
        # 执行格式转换
        result_path = ImageProcessor.convert_format(file_path, target_format, quality)
        
        # 返回处理后的文件
        return FileResponse(
            path=result_path,
            filename=f"{os.path.splitext(file.filename)[0]}.{target_format}",
            media_type="image/*"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

@app.post("/api/image/resize")
async def resize_image(
    file: UploadFile = File(...),
    width: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    keep_aspect_ratio: bool = Form(True)
):
    try:
        # 保存上传的文件
        file_path = save_upload_file(file)
        
        # 执行调整大小
        result_path = ImageProcessor.resize_image(file_path, width, height, keep_aspect_ratio)
        
        # 返回处理后的文件
        return FileResponse(
            path=result_path,
            filename=f"{os.path.splitext(file.filename)[0]}_resized{os.path.splitext(file.filename)[1]}",
            media_type="image/*"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

@app.post("/api/image/watermark")
async def add_watermark(
    file: UploadFile = File(...),
    watermark_text: Optional[str] = Form(None),
    watermark_image: Optional[UploadFile] = File(None),
    position: str = Form("center"),
    opacity: float = Form(0.5),
    rotation: int = Form(0)
):
    try:
        # 保存上传的文件
        file_path = save_upload_file(file)
        watermark_image_path = None
        
        if watermark_image:
            watermark_image_path = save_upload_file(watermark_image)
        
        # 执行添加水印
        result_path = ImageProcessor.add_watermark(file_path, watermark_text, watermark_image_path, position, opacity, rotation)
        
        # 返回处理后的文件
        return FileResponse(
            path=result_path,
            filename=f"{os.path.splitext(file.filename)[0]}_watermarked{os.path.splitext(file.filename)[1]}",
            media_type="image/*"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        if 'watermark_image_path' in locals() and watermark_image_path and os.path.exists(watermark_image_path):
            os.remove(watermark_image_path)

@app.post("/api/image/filter")
async def apply_filter(
    file: UploadFile = File(...),
    filter_type: str = Form(...),
    intensity: float = Form(1.0)
):
    try:
        # 保存上传的文件
        file_path = save_upload_file(file)
        
        # 执行应用滤镜
        result_path = ImageProcessor.apply_filter(file_path, filter_type, intensity)
        
        # 返回处理后的文件
        return FileResponse(
            path=result_path,
            filename=f"{os.path.splitext(file.filename)[0]}_{filter_type}{os.path.splitext(file.filename)[1]}",
            media_type="image/*"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

@app.post("/api/image/batch-process")
async def batch_process_images(
    files: List[UploadFile] = File(...),
    request: str = Form(...)
):
    import json
    try:
        # 解析请求
        req_data = json.loads(request)
        operations = req_data["operations"]
        
        # 保存上传的文件
        file_paths = [save_upload_file(file) for file in files]
        
        # 创建输出目录
        output_dir = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
        os.makedirs(output_dir, exist_ok=True)
        
        # 执行批量处理
        result_paths = ImageProcessor.batch_process(file_paths, operations, output_dir)
        
        # 创建ZIP文件
        zip_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}_processed.zip")
        shutil.make_archive(zip_path[:-4], 'zip', output_dir)
        
        # 返回ZIP文件
        return FileResponse(
            path=zip_path,
            filename="processed_images.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        for file_path in locals().get('file_paths', []):
            if os.path.exists(file_path):
                os.remove(file_path)
        if 'output_dir' in locals() and os.path.exists(output_dir):
            shutil.rmtree(output_dir)

# 定期清理临时文件
@app.on_event("startup")
async def startup_event():
    # 清理临时文件夹
    if os.path.exists(TEMP_DIR):
        for item in os.listdir(TEMP_DIR):
            item_path = os.path.join(TEMP_DIR, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"清理临时文件时出错: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)