import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

class ImageProcessor:
    @staticmethod
    def convert_format(file_path, target_format, quality=90, output_dir=None):
        """
        转换图像格式
        
        Args:
            file_path: 图像文件路径
            target_format: 目标格式（如'jpg', 'png', 'webp'等）
            quality: 输出质量（1-100，仅对jpg和webp有效）
            output_dir: 输出目录，如果为None则在原目录中保存
            
        Returns:
            转换后的文件路径
        """
        try:
            # 打开图像
            img = Image.open(file_path)
            
            # 创建输出文件路径
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            name_without_ext = os.path.splitext(file_name)[0]
            
            # 确保格式名称正确
            target_format = target_format.lower().strip('.')
            
            # 创建新文件名
            new_name = f"{name_without_ext}.{target_format}"
            
            if output_dir:
                output_path = os.path.join(output_dir, new_name)
            else:
                output_path = os.path.join(file_dir, new_name)
            
            # 保存为新格式
            if target_format.lower() in ['jpg', 'jpeg']:
                # 如果原图像有透明通道，需要先转换为RGB
                if img.mode in ['RGBA', 'LA'] or (img.mode == 'P' and 'transparency' in img.info):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                    background.save(output_path, 'JPEG', quality=quality)
                else:
                    img.convert('RGB').save(output_path, 'JPEG', quality=quality)
            elif target_format.lower() == 'png':
                img.save(output_path, 'PNG')
            elif target_format.lower() == 'webp':
                img.save(output_path, 'WEBP', quality=quality)
            elif target_format.lower() == 'gif':
                img.save(output_path, 'GIF')
            else:
                img.save(output_path, target_format.upper())
            
            return output_path
        except Exception as e:
            raise Exception(f"转换图像格式时出错: {str(e)}")
    
    @staticmethod
    def resize_image(file_path, width=None, height=None, keep_aspect_ratio=True, output_dir=None):
        """
        调整图像大小
        
        Args:
            file_path: 图像文件路径
            width: 目标宽度，如果为None则根据高度和原始比例计算
            height: 目标高度，如果为None则根据宽度和原始比例计算
            keep_aspect_ratio: 是否保持原始宽高比
            output_dir: 输出目录，如果为None则在原目录中保存
            
        Returns:
            调整大小后的文件路径
        """
        try:
            # 打开图像
            img = Image.open(file_path)
            original_width, original_height = img.size
            
            # 计算新尺寸
            if width is None and height is None:
                # 如果没有指定宽度和高度，则保持原始尺寸
                new_width, new_height = original_width, original_height
            elif width is None:
                # 如果只指定了高度，则根据原始比例计算宽度
                new_height = height
                if keep_aspect_ratio:
                    new_width = int(original_width * (new_height / original_height))
                else:
                    new_width = original_width
            elif height is None:
                # 如果只指定了宽度，则根据原始比例计算高度
                new_width = width
                if keep_aspect_ratio:
                    new_height = int(original_height * (new_width / original_width))
                else:
                    new_height = original_height
            else:
                # 如果同时指定了宽度和高度
                if keep_aspect_ratio:
                    # 保持原始比例，取较小的缩放比例
                    width_ratio = width / original_width
                    height_ratio = height / original_height
                    
                    if width_ratio < height_ratio:
                        new_width = width
                        new_height = int(original_height * width_ratio)
                    else:
                        new_height = height
                        new_width = int(original_width * height_ratio)
                else:
                    # 不保持原始比例，直接使用指定的宽度和高度
                    new_width, new_height = width, height
            
            # 调整图像大小
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # 创建输出文件路径
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            name_parts = os.path.splitext(file_name)
            
            # 创建新文件名
            new_name = f"{name_parts[0]}_resized{name_parts[1]}"
            
            if output_dir:
                output_path = os.path.join(output_dir, new_name)
            else:
                output_path = os.path.join(file_dir, new_name)
            
            # 保存调整大小后的图像
            resized_img.save(output_path)
            
            return output_path
        except Exception as e:
            raise Exception(f"调整图像大小时出错: {str(e)}")
    
    @staticmethod
    def add_watermark(file_path, watermark_text=None, watermark_image=None, position='center', 
                      opacity=0.5, rotation=0, output_dir=None):
        """
        为图像添加水印
        
        Args:
            file_path: 图像文件路径
            watermark_text: 水印文本，如果为None则使用水印图像
            watermark_image: 水印图像路径，如果为None则使用水印文本
            position: 水印位置，可以是'center', 'top-left', 'top-right', 'bottom-left', 'bottom-right'
            opacity: 水印不透明度（0-1）
            rotation: 水印旋转角度
            output_dir: 输出目录，如果为None则在原目录中保存
            
        Returns:
            添加水印后的文件路径
        """
        try:
            # 打开原始图像
            img = Image.open(file_path).convert('RGBA')
            
            # 创建水印层
            watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            
            if watermark_text:
                # 使用文本水印
                try:
                    # 尝试加载系统字体
                    font = ImageFont.truetype("arial.ttf", 36)
                except IOError:
                    # 如果找不到系统字体，则使用默认字体
                    font = ImageFont.load_default()
                
                # 计算文本大小
                text_width, text_height = draw.textsize(watermark_text, font=font)
                
                # 计算文本位置
                if position == 'center':
                    text_position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
                elif position == 'top-left':
                    text_position = (10, 10)
                elif position == 'top-right':
                    text_position = (img.width - text_width - 10, 10)
                elif position == 'bottom-left':
                    text_position = (10, img.height - text_height - 10)
                elif position == 'bottom-right':
                    text_position = (img.width - text_width - 10, img.height - text_height - 10)
                else:
                    text_position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
                
                # 绘制文本水印
                draw.text(text_position, watermark_text, fill=(255, 255, 255, int(255 * opacity)), font=font)
                
                # 如果需要旋转
                if rotation != 0:
                    watermark = watermark.rotate(rotation, expand=1)
                    # 重新调整水印大小以匹配原始图像
                    watermark = watermark.resize(img.size)
            
            elif watermark_image:
                # 使用图像水印
                wm_img = Image.open(watermark_image).convert('RGBA')
                
                # 调整水印图像大小（最大为原图的1/4）
                wm_width, wm_height = wm_img.size
                max_wm_width = img.width // 4
                max_wm_height = img.height // 4
                
                if wm_width > max_wm_width or wm_height > max_wm_height:
                    scale = min(max_wm_width / wm_width, max_wm_height / wm_height)
                    wm_width = int(wm_width * scale)
                    wm_height = int(wm_height * scale)
                    wm_img = wm_img.resize((wm_width, wm_height), Image.LANCZOS)
                
                # 调整水印不透明度
                if opacity < 1:
                    wm_img = ImageEnhance.Brightness(wm_img).enhance(opacity)
                
                # 如果需要旋转
                if rotation != 0:
                    wm_img = wm_img.rotate(rotation, expand=1)
                
                # 计算水印位置
                if position == 'center':
                    wm_position = ((img.width - wm_width) // 2, (img.height - wm_height) // 2)
                elif position == 'top-left':
                    wm_position = (10, 10)
                elif position == 'top-right':
                    wm_position = (img.width - wm_width - 10, 10)
                elif position == 'bottom-left':
                    wm_position = (10, img.height - wm_height - 10)
                elif position == 'bottom-right':
                    wm_position = (img.width - wm_width - 10, img.height - wm_height - 10)
                else:
                    wm_position = ((img.width - wm_width) // 2, (img.height - wm_height) // 2)
                
                # 将水印图像粘贴到水印层
                watermark.paste(wm_img, wm_position, wm_img)
            
            # 将水印层与原始图像合并
            result = Image.alpha_composite(img, watermark)
            
            # 创建输出文件路径
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            name_parts = os.path.splitext(file_name)
            
            # 创建新文件名
            new_name = f"{name_parts[0]}_watermarked{name_parts[1]}"
            
            if output_dir:
                output_path = os.path.join(output_dir, new_name)
            else:
                output_path = os.path.join(file_dir, new_name)
            
            # 保存添加水印后的图像
            result = result.convert('RGB')  # 转换回RGB模式以支持所有格式
            result.save(output_path)
            
            return output_path
        except Exception as e:
            raise Exception(f"添加水印时出错: {str(e)}")
    
    @staticmethod
    def batch_process(file_paths, operations, output_dir=None):
        """
        批量处理图像
        
        Args:
            file_paths: 图像文件路径列表
            operations: 操作列表，每个操作是一个字典，包含操作类型和参数
            output_dir: 输出目录
            
        Returns:
            处理后的文件路径列表
        """
        try:
            processed_files = []
            
            for file_path in file_paths:
                current_file = file_path
                
                for operation in operations:
                    op_type = operation.get("type")
                    
                    if op_type == "convert_format":
                        target_format = operation.get("target_format")
                        quality = operation.get("quality", 90)
                        current_file = ImageProcessor.convert_format(current_file, target_format, quality, output_dir)
                    
                    elif op_type == "resize":
                        width = operation.get("width")
                        height = operation.get("height")
                        keep_aspect_ratio = operation.get("keep_aspect_ratio", True)
                        current_file = ImageProcessor.resize_image(current_file, width, height, keep_aspect_ratio, output_dir)
                    
                    elif op_type == "add_watermark":
                        watermark_text = operation.get("watermark_text")
                        watermark_image = operation.get("watermark_image")
                        position = operation.get("position", "center")
                        opacity = operation.get("opacity", 0.5)
                        rotation = operation.get("rotation", 0)
                        current_file = ImageProcessor.add_watermark(
                            current_file, watermark_text, watermark_image, position, opacity, rotation, output_dir
                        )
                
                processed_files.append(current_file)
            
            return processed_files
        except Exception as e:
            raise Exception(f"批量处理图像时出错: {str(e)}")
    
    @staticmethod
    def apply_filter(file_path, filter_type, intensity=1.0, output_dir=None):
        """
        应用图像滤镜
        
        Args:
            file_path: 图像文件路径
            filter_type: 滤镜类型，可以是'blur', 'sharpen', 'contour', 'detail', 'edge_enhance', 'emboss', 'smooth', 'brightness', 'contrast'
            intensity: 滤镜强度（0.0-2.0）
            output_dir: 输出目录，如果为None则在原目录中保存
            
        Returns:
            应用滤镜后的文件路径
        """
        try:
            # 打开图像
            img = Image.open(file_path)
            
            # 应用滤镜
            if filter_type == 'blur':
                filtered_img = img.filter(ImageFilter.GaussianBlur(radius=intensity * 2))
            elif filter_type == 'sharpen':
                filtered_img = img
                for _ in range(int(intensity * 3)):
                    filtered_img = filtered_img.filter(ImageFilter.SHARPEN)
            elif filter_type == 'contour':
                filtered_img = img.filter(ImageFilter.CONTOUR)
            elif filter_type == 'detail':
                filtered_img = img.filter(ImageFilter.DETAIL)
            elif filter_type == 'edge_enhance':
                filtered_img = img
                for _ in range(int(intensity * 3)):
                    filtered_img = filtered_img.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_type == 'emboss':
                filtered_img = img.filter(ImageFilter.EMBOSS)
            elif filter_type == 'smooth':
                filtered_img = img.filter(ImageFilter.SMOOTH_MORE)
            elif filter_type == 'brightness':
                enhancer = ImageEnhance.Brightness(img)
                filtered_img = enhancer.enhance(intensity)
            elif filter_type == 'contrast':
                enhancer = ImageEnhance.Contrast(img)
                filtered_img = enhancer.enhance(intensity)
            else:
                raise ValueError(f"不支持的滤镜类型: {filter_type}")
            
            # 创建输出文件路径
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            name_parts = os.path.splitext(file_name)
            
            # 创建新文件名
            new_name = f"{name_parts[0]}_{filter_type}{name_parts[1]}"
            
            if output_dir:
                output_path = os.path.join(output_dir, new_name)
            else:
                output_path = os.path.join(file_dir, new_name)
            
            # 保存应用滤镜后的图像
            filtered_img.save(output_path)
            
            return output_path
        except Exception as e:
            raise Exception(f"应用图像滤镜时出错: {str(e)}")