import os
import re
import shutil
import datetime
import pandas as pd
from pathlib import Path

class FileRenamer:
    @staticmethod
    def add_prefix(file_path, prefix, output_dir=None):
        """
        为文件添加前缀
        
        Args:
            file_path: 文件路径
            prefix: 要添加的前缀
            output_dir: 输出目录，如果为None则在原目录中重命名
            
        Returns:
            重命名后的文件路径
        """
        try:
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            new_name = f"{prefix}{file_name}"
            
            if output_dir:
                new_path = os.path.join(output_dir, new_name)
                shutil.copy2(file_path, new_path)
            else:
                new_path = os.path.join(file_dir, new_name)
                shutil.move(file_path, new_path)
            
            return new_path
        except Exception as e:
            raise Exception(f"添加前缀时出错: {str(e)}")
    
    @staticmethod
    def add_suffix(file_path, suffix, output_dir=None):
        """
        为文件添加后缀（在扩展名之前）
        
        Args:
            file_path: 文件路径
            suffix: 要添加的后缀
            output_dir: 输出目录，如果为None则在原目录中重命名
            
        Returns:
            重命名后的文件路径
        """
        try:
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            name_parts = file_name.rsplit('.', 1)
            
            if len(name_parts) > 1:
                new_name = f"{name_parts[0]}{suffix}.{name_parts[1]}"
            else:
                new_name = f"{file_name}{suffix}"
            
            if output_dir:
                new_path = os.path.join(output_dir, new_name)
                shutil.copy2(file_path, new_path)
            else:
                new_path = os.path.join(file_dir, new_name)
                shutil.move(file_path, new_path)
            
            return new_path
        except Exception as e:
            raise Exception(f"添加后缀时出错: {str(e)}")
    
    @staticmethod
    def replace_text(file_path, find_text, replace_text, use_regex=False, output_dir=None):
        """
        替换文件名中的文本
        
        Args:
            file_path: 文件路径
            find_text: 要查找的文本
            replace_text: 替换的文本
            use_regex: 是否使用正则表达式
            output_dir: 输出目录，如果为None则在原目录中重命名
            
        Returns:
            重命名后的文件路径
        """
        try:
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            
            if use_regex:
                new_name = re.sub(find_text, replace_text, file_name)
            else:
                new_name = file_name.replace(find_text, replace_text)
            
            if output_dir:
                new_path = os.path.join(output_dir, new_name)
                shutil.copy2(file_path, new_path)
            else:
                new_path = os.path.join(file_dir, new_name)
                shutil.move(file_path, new_path)
            
            return new_path
        except Exception as e:
            raise Exception(f"替换文本时出错: {str(e)}")
    
    @staticmethod
    def delete_text(file_path, text_to_delete, use_regex=False, output_dir=None):
        """
        删除文件名中的文本
        
        Args:
            file_path: 文件路径
            text_to_delete: 要删除的文本
            use_regex: 是否使用正则表达式
            output_dir: 输出目录，如果为None则在原目录中重命名
            
        Returns:
            重命名后的文件路径
        """
        return FileRenamer.replace_text(file_path, text_to_delete, "", use_regex, output_dir)
    
    @staticmethod
    def sequence_rename(file_paths, pattern, start_number=1, step=1, padding=1, output_dir=None):
        """
        使用数字序列重命名文件
        
        Args:
            file_paths: 文件路径列表
            pattern: 文件名模式，使用{n}作为序列号占位符
            start_number: 起始序列号
            step: 序列号步长
            padding: 序列号填充长度
            output_dir: 输出目录，如果为None则在原目录中重命名
            
        Returns:
            重命名后的文件路径列表
        """
        try:
            renamed_files = []
            current_number = start_number
            
            for file_path in file_paths:
                file_dir = os.path.dirname(file_path)
                file_name = os.path.basename(file_path)
                ext = os.path.splitext(file_name)[1]
                
                # 替换模式中的序列号占位符
                sequence_str = str(current_number).zfill(padding)
                new_name = pattern.replace("{n}", sequence_str) + ext
                
                if output_dir:
                    new_path = os.path.join(output_dir, new_name)
                    shutil.copy2(file_path, new_path)
                else:
                    new_path = os.path.join(file_dir, new_name)
                    shutil.move(file_path, new_path)
                
                renamed_files.append(new_path)
                current_number += step
            
            return renamed_files
        except Exception as e:
            raise Exception(f"序列化重命名时出错: {str(e)}")
    
    @staticmethod
    def date_sequence_rename(file_paths, pattern, date_format="%Y%m%d", start_date=None, days_step=1, output_dir=None):
        """
        使用日期序列重命名文件
        
        Args:
            file_paths: 文件路径列表
            pattern: 文件名模式，使用{d}作为日期占位符
            date_format: 日期格式
            start_date: 起始日期，如果为None则使用当前日期
            days_step: 日期步长（天数）
            output_dir: 输出目录，如果为None则在原目录中重命名
            
        Returns:
            重命名后的文件路径列表
        """
        try:
            renamed_files = []
            
            if start_date is None:
                current_date = datetime.datetime.now()
            else:
                if isinstance(start_date, str):
                    current_date = datetime.datetime.strptime(start_date, date_format)
                else:
                    current_date = start_date
            
            for file_path in file_paths:
                file_dir = os.path.dirname(file_path)
                file_name = os.path.basename(file_path)
                ext = os.path.splitext(file_name)[1]
                
                # 替换模式中的日期占位符
                date_str = current_date.strftime(date_format)
                new_name = pattern.replace("{d}", date_str) + ext
                
                if output_dir:
                    new_path = os.path.join(output_dir, new_name)
                    shutil.copy2(file_path, new_path)
                else:
                    new_path = os.path.join(file_dir, new_name)
                    shutil.move(file_path, new_path)
                
                renamed_files.append(new_path)
                current_date += datetime.timedelta(days=days_step)
            
            return renamed_files
        except Exception as e:
            raise Exception(f"日期序列重命名时出错: {str(e)}")
    
    @staticmethod
    def custom_sequence_rename(file_paths, pattern, sequence, output_dir=None):
        """
        使用自定义序列重命名文件
        
        Args:
            file_paths: 文件路径列表
            pattern: 文件名模式，使用{s}作为序列项占位符
            sequence: 自定义序列项列表
            output_dir: 输出目录，如果为None则在原目录中重命名
            
        Returns:
            重命名后的文件路径列表
        """
        try:
            renamed_files = []
            
            # 如果序列项少于文件数，则循环使用序列项
            for i, file_path in enumerate(file_paths):
                file_dir = os.path.dirname(file_path)
                file_name = os.path.basename(file_path)
                ext = os.path.splitext(file_name)[1]
                
                # 获取当前序列项
                seq_item = sequence[i % len(sequence)]
                
                # 替换模式中的序列项占位符
                new_name = pattern.replace("{s}", str(seq_item)) + ext
                
                if output_dir:
                    new_path = os.path.join(output_dir, new_name)
                    shutil.copy2(file_path, new_path)
                else:
                    new_path = os.path.join(file_dir, new_name)
                    shutil.move(file_path, new_path)
                
                renamed_files.append(new_path)
            
            return renamed_files
        except Exception as e:
            raise Exception(f"自定义序列重命名时出错: {str(e)}")
    
    @staticmethod
    def batch_rename(file_paths, operations, output_dir=None):
        """
        批量重命名文件
        
        Args:
            file_paths: 文件路径列表
            operations: 重命名操作列表，每个操作是一个字典，包含操作类型和参数
            output_dir: 输出目录，如果为None则在原目录中重命名
            
        Returns:
            重命名后的文件路径列表
        """
        try:
            renamed_files = []
            
            # 如果提供了输出目录，先复制所有文件
            if output_dir:
                temp_files = []
                for file_path in file_paths:
                    file_name = os.path.basename(file_path)
                    new_path = os.path.join(output_dir, file_name)
                    shutil.copy2(file_path, new_path)
                    temp_files.append(new_path)
                file_paths = temp_files
            
            # 应用所有重命名操作
            current_files = file_paths
            
            for operation in operations:
                op_type = operation.get("type")
                
                if op_type == "add_prefix":
                    prefix = operation.get("prefix", "")
                    new_files = []
                    for file_path in current_files:
                        new_path = FileRenamer.add_prefix(file_path, prefix)
                        new_files.append(new_path)
                    current_files = new_files
                
                elif op_type == "add_suffix":
                    suffix = operation.get("suffix", "")
                    new_files = []
                    for file_path in current_files:
                        new_path = FileRenamer.add_suffix(file_path, suffix)
                        new_files.append(new_path)
                    current_files = new_files
                
                elif op_type == "replace_text":
                    find_text = operation.get("find_text", "")
                    replace_text = operation.get("replace_text", "")
                    use_regex = operation.get("use_regex", False)
                    new_files = []
                    for file_path in current_files:
                        new_path = FileRenamer.replace_text(file_path, find_text, replace_text, use_regex)
                        new_files.append(new_path)
                    current_files = new_files
                
                elif op_type == "delete_text":
                    text_to_delete = operation.get("text_to_delete", "")
                    use_regex = operation.get("use_regex", False)
                    new_files = []
                    for file_path in current_files:
                        new_path = FileRenamer.delete_text(file_path, text_to_delete, use_regex)
                        new_files.append(new_path)
                    current_files = new_files
            
            return current_files
        except Exception as e:
            raise Exception(f"批量重命名时出错: {str(e)}")
    
    @staticmethod
    def rename_from_excel(file_paths, excel_path, name_column, output_dir=None):
        """
        从Excel文件导入重命名规则
        
        Args:
            file_paths: 文件路径列表
            excel_path: Excel文件路径
            name_column: 包含新文件名的列名
            output_dir: 输出目录，如果为None则在原目录中重命名
            
        Returns:
            重命名后的文件路径列表
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(excel_path)
            
            if name_column not in df.columns:
                raise ValueError(f"Excel文件中不存在列 '{name_column}'")
            
            # 获取新文件名列表
            new_names = df[name_column].tolist()
            
            # 如果新文件名少于文件数，则只重命名前面的文件
            renamed_files = []
            
            for i, file_path in enumerate(file_paths):
                if i >= len(new_names):
                    break
                
                file_dir = os.path.dirname(file_path)
                file_name = os.path.basename(file_path)
                ext = os.path.splitext(file_name)[1]
                
                # 获取新文件名
                new_name = str(new_names[i])
                
                # 如果新文件名没有扩展名，则添加原文件的扩展名
                if not os.path.splitext(new_name)[1]:
                    new_name += ext
                
                if output_dir:
                    new_path = os.path.join(output_dir, new_name)
                    shutil.copy2(file_path, new_path)
                else:
                    new_path = os.path.join(file_dir, new_name)
                    shutil.move(file_path, new_path)
                
                renamed_files.append(new_path)
            
            return renamed_files
        except Exception as e:
            raise Exception(f"从Excel导入重命名规则时出错: {str(e)}")