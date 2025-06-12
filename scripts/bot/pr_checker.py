#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub PR 检查机器人

此模块提供了检查 GitHub Pull Request 的功能。
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional, Tuple

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.insert(0, project_root)

try:
    from scripts.validation.domain_validator import validate_pull_request, load_config
except ImportError as e:
    print(f"导入错误: {e}", file=sys.stderr)
    print(f"当前目录: {current_dir}", file=sys.stderr)
    print(f"项目根目录: {project_root}", file=sys.stderr)
    print(f"Python 路径: {sys.path[:3]}", file=sys.stderr)
    sys.exit(1)


def format_validation_result(results: Dict[str, List[str]]) -> str:
    """
    格式化验证结果为 Markdown 格式
    
    Args:
        results: 验证结果字典 {文件路径: 错误信息列表}
    
    Returns:
        Markdown 格式的验证结果
    """
    markdown = []
    markdown.append("# 🤖 域名配置验证结果\n")
    
    # 统计信息
    total_files = len(results)
    error_files = sum(1 for errors in results.values() if errors)
    success_files = total_files - error_files
    
    if error_files == 0:
        markdown.append("## ✅ 验证通过")
        markdown.append(f"所有 {total_files} 个文件验证通过，没有发现问题。\n")
    else:
        markdown.append("## ❌ 验证失败")
        markdown.append(f"共 {total_files} 个文件，其中 {error_files} 个文件有问题，{success_files} 个文件正常。\n")
    
    # 详细结果
    for file_path, errors in results.items():
        if errors:
            markdown.append(f"### ❌ `{file_path}`")
            markdown.append("")
            for i, error in enumerate(errors, 1):
                # 将多行错误信息格式化
                if '\n' in error:
                    lines = error.split('\n')
                    markdown.append(f"**错误 {i}:** {lines[0]}")
                    for line in lines[1:]:
                        if line.strip():
                            markdown.append(f"  - {line.strip()}")
                else:
                    markdown.append(f"**错误 {i}:** {error}")
            markdown.append("")
        else:
            markdown.append(f"### ✅ `{file_path}`")
            markdown.append("")
            markdown.append("验证通过，没有发现问题。")
            markdown.append("")
    
    # 添加帮助提示
    if error_files > 0:
        markdown.append("---")
        markdown.append("## 💡 常见问题解决方法")
        markdown.append("")
        markdown.append("### JSON 格式错误")
        markdown.append("- **缺少逗号**: 确保 JSON 对象中的字段用逗号分隔")
        markdown.append("- **缺少冒号**: 确保键值对用冒号分隔")
        markdown.append("- **引号不匹配**: 确保所有字符串用双引号包围")
        markdown.append("- **多余逗号**: 删除最后一个字段后的多余逗号")
        markdown.append("")
        markdown.append("### 推荐工具")
        markdown.append("- 使用 [JSONLint](https://jsonlint.com/) 验证 JSON 格式")
        markdown.append("- 使用支持 JSON 语法高亮的编辑器（如 VS Code）")
        markdown.append("")
        markdown.append("如需帮助，请查看 [用户指南](https://github.com/bestzwei/LibreDomains/blob/main/docs/user-guide.md)")
    
    return "\n".join(markdown)


def check_pr_files(pr_files: List[str], config: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    """
    检查 Pull Request 中的文件
    
    Args:
        pr_files: Pull Request 中的文件路径列表
        config: 项目配置信息 (可选)
    
    Returns:
        (是否所有文件有效, Markdown 格式的验证结果)
    """
    # 规范化文件路径
    normalized_files = []
    missing_files = []
    
    for file_path in pr_files:
        # 支持相对路径和绝对路径
        if not os.path.isabs(file_path):
            # 相对路径，从项目根目录开始
            abs_path = os.path.join(project_root, file_path)
        else:
            abs_path = file_path
        
        # 检查文件是否存在
        if os.path.exists(abs_path):
            normalized_files.append(abs_path)
        else:
            # 尝试相对于当前工作目录
            if os.path.exists(file_path):
                normalized_files.append(os.path.abspath(file_path))
            else:
                missing_files.append(file_path)
                print(f"警告: 文件不存在: {file_path} (尝试路径: {abs_path})", file=sys.stderr)
    
    # 调试信息
    print(f"项目根目录: {project_root}", file=sys.stderr)
    print(f"当前工作目录: {os.getcwd()}", file=sys.stderr)
    print(f"原始文件列表: {pr_files}", file=sys.stderr)
    print(f"规范化文件列表: {normalized_files}", file=sys.stderr)
    print(f"缺失文件列表: {missing_files}", file=sys.stderr)
    
    # 如果没有找到任何文件
    if not normalized_files:
        error_msg = "没有找到需要验证的文件。\n\n"
        if missing_files:
            error_msg += "缺失的文件:\n"
            for file_path in missing_files:
                error_msg += f"- {file_path}\n"
        return False, f"## ❌ 验证失败\n\n{error_msg}"
    
    try:
        # 验证文件
        all_valid, results = validate_pull_request(normalized_files, config)
        
        # 如果有缺失文件，添加到结果中
        for file_path in missing_files:
            results[file_path] = [f"文件不存在: {file_path}"]
            all_valid = False
        
        # 格式化结果
        markdown = format_validation_result(results)
        
        return all_valid, markdown
    except Exception as e:
        import traceback
        error_msg = f"验证过程中发生错误: {str(e)}"
        # 添加详细的错误追踪信息
        traceback_info = traceback.format_exc()
        print(f"详细错误信息:\n{traceback_info}", file=sys.stderr)
        
        # 添加环境调试信息
        print(f"环境调试信息:", file=sys.stderr)
        print(f"- Python 版本: {sys.version}", file=sys.stderr)
        print(f"- 当前目录: {os.getcwd()}", file=sys.stderr)
        print(f"- 脚本路径: {__file__}", file=sys.stderr)
        print(f"- 项目根目录: {project_root}", file=sys.stderr)
        
        return False, f"## ❌ 验证失败\n\n{error_msg}\n\n详细错误信息请查看 Actions 日志。"


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GitHub PR 检查工具')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--files', nargs='+', required=True, help='要检查的文件路径')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    # 启用调试模式
    if args.debug:
        print("=== 调试模式启用 ===", file=sys.stderr)
        print(f"命令行参数: {args}", file=sys.stderr)
        print(f"当前工作目录: {os.getcwd()}", file=sys.stderr)
        print(f"项目根目录: {project_root}", file=sys.stderr)
    
    try:
        # 加载项目配置
        config = None
        if args.config:
            config = load_config(args.config)
        else:
            try:
                config = load_config()
            except Exception as e:
                print(f"警告: 无法加载默认配置文件: {e}", file=sys.stderr)
        
        # 检查文件
        all_valid, markdown = check_pr_files(args.files, config)
        
        # 输出结果
        if args.output:
            output_dir = os.path.dirname(args.output)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"结果已保存到: {args.output}", file=sys.stderr)
        else:
            print(markdown)
        
        return 0 if all_valid else 1
    except Exception as e:
        import traceback
        error_msg = f"程序执行失败: {str(e)}"
        traceback_info = traceback.format_exc()
        print(error_msg, file=sys.stderr)
        print(f"详细错误信息:\n{traceback_info}", file=sys.stderr)
        
        if args.output:
            try:
                output_dir = os.path.dirname(args.output)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(f"## ❌ 执行失败\n\n{error_msg}\n\n```\n{traceback_info}\n```")
            except Exception as output_error:
                print(f"无法写入输出文件: {output_error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
