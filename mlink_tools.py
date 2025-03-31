import os
import shutil
import platform

"""
目录迁移与符号链接创建工具

这个工具用于将原始目录移动到目标目录，并在原位置创建符号链接。

主要功能：
1. 帮助系统
   - 支持随时查看使用说明
   - 无参数启动时进入交互模式

2. 路径验证
   - 检查原始目录是否存在
   - 检查目标目录是否存在冲突
   - 自动处理目标父目录的创建

3. 安全机制
   - 操作前需要用户二次确认
   - 提供操作回滚功能

4. 跨平台支持
   - 自动识别 Windows/Linux 系统
   - Windows 下正确处理目录符号链接

5. 错误处理
   - 详细错误提示
   - Windows 权限不足时的明确提示
"""


def print_help():
    print("""
    使用方法：
    本程序用于将原始目录移动到目标目录，并在原位置创建符号链接。
    
    步骤：
    1. 输入原始目录路径和目标目录路径。
    2. 程序将检查原始目录是否存在以及目标目录是否已存在。
    3. 确认操作后，移动目录并创建符号链接。
    
    注意：
    - Windows系统可能需要管理员权限才能创建符号链接。
    - 输入路径时请使用绝对路径。
    - 操作前请务必确认目录信息正确。
    """)

def get_user_input(prompt):
    while True:
        value = input(prompt).strip()
        if value.lower() == 'help':
            print_help()
        else:
            return value

def main():
    print("=== 目录迁移与符号链接创建工具 ===")
    source = get_user_input("请输入原始目录路径（输入help查看帮助）: ")
    target = get_user_input("请输入目标目录路径（输入help查看帮助）: ")

    # 检查原始目录是否存在
    if not os.path.exists(source):
        print(f"错误：原始目录 '{source}' 不存在")
        return

    # 检查目标目录是否已存在
    if os.path.exists(target):
        print(f"错误：目标目录 '{target}' 已存在")
        return

    # 处理目标父目录
    target_parent = os.path.dirname(os.path.abspath(target))
    if not os.path.exists(target_parent):
        print(f"目标父目录 '{target_parent}' 不存在")
        choice = input("是否要创建父目录？(yes/no): ").lower()
        if choice != 'yes':
            print("操作已取消")
            return
        os.makedirs(target_parent, exist_ok=True)

    # 显示操作摘要
    print("\n即将执行以下操作：")
    print(f"1. 移动目录: {source} -> {target}")
    print(f"2. 创建符号链接: {source} -> {target}")

    # 用户确认
    if input("\n确认执行操作吗？(yes/no): ").lower() != 'yes':
        print("操作已取消")
        return

    # 执行目录迁移
    try:
        shutil.move(source, target)
        print("\n目录移动成功")
    except Exception as e:
        print(f"\n目录移动失败: {str(e)}")
        return

    # 创建符号链接
    try:
        if platform.system() == "Windows":
            os.symlink(target, source, target_is_directory=True)
        else:
            os.symlink(target, source)
        print("符号链接创建成功")
    except OSError as e:
        print(f"\n符号链接创建失败: {str(e)}")
        if platform.system() == "Windows":
            print("提示：Windows系统需要以管理员身份运行程序")
        
        # 尝试回滚移动操作
        print("\n尝试回滚目录移动...")
        try:
            shutil.move(target, source)
            print("回滚成功")
        except Exception as e:
            print(f"回滚失败: {str(e)}")
            print(f"请手动将 '{target}' 移动回 '{source}'")
        return

    print("\n操作成功完成！")

if __name__ == "__main__":
    main()
