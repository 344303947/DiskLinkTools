# DiskLinkTools
C盘目录迁移工具，需要安装python环境，帮助迁移大文件目录软连接到其他盘，实现压缩C盘空间目的。

使用管理员权限打开终端工具 cmd ,powershell
使用方式 python  C:\Users\sean.su\Desktop\mlink_tools.py 

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
    
使用方式2 python  C:\Users\sean.su\Desktop\mlink_tools_ui.py   
通过界面选择目录，实现撤回等功能
