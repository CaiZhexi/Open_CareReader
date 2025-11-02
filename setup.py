#!/usr/bin/env python3
"""
CareReader 项目初始化脚本
自动配置环境和依赖
"""

import os
import sys
import subprocess
from pathlib import Path


def print_step(step, message):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"步骤 {step}: {message}")
    print('='*60)


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major != 3 or version.minor < 10:
        print(f"错误: 需要Python 3.10或更高版本，当前版本: {version.major}.{version.minor}")
        return False
    print(f"Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True


def create_venv():
    """创建虚拟环境"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("虚拟环境已存在")
        return True
    
    try:
        print("正在创建虚拟环境...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("虚拟环境创建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"创建虚拟环境失败: {e}")
        return False


def get_venv_python():
    """获取虚拟环境中的Python路径"""
    if os.name == 'nt':  # Windows
        return Path("venv/Scripts/python.exe")
    else:  # Unix-like
        return Path("venv/bin/python")


def install_dependencies():
    """安装依赖"""
    python_path = get_venv_python()
    if not python_path.exists():
        print("错误: 虚拟环境Python未找到")
        return False
    
    try:
        print("正在安装依赖包...")
        subprocess.run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(python_path), "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装依赖失败: {e}")
        return False


def create_env_file():
    """创建.env文件"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print(".env文件已存在")
        response = input("是否要重新配置? (y/N): ")
        if response.lower() != 'y':
            return True
    
    if not env_example.exists():
        print("警告: .env.example文件不存在")
        return False
    
    print("\n请输入配置信息:")
    api_key = input("SiliconFlow API密钥 (必填): ").strip()
    
    if not api_key:
        print("错误: API密钥不能为空")
        return False
    
    # 读取模板并替换
    with open(env_example, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('your-api-key-here', api_key)
    
    # 写入.env文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(".env文件创建成功")
    return True


def print_next_steps():
    """打印后续步骤"""
    print("\n" + "="*60)
    print("配置完成！")
    print("="*60)
    print("\n后续步骤:")
    print("\n1. 激活虚拟环境:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. 运行Gradio界面:")
    print("   python ui/app_gradio.py")
    print("   或执行: ./run_gradio.sh")
    
    print("\n3. 运行FastAPI服务:")
    print("   python app/main.py")
    print("   或执行: ./run_api.sh")
    
    print("\n4. 使用Docker:")
    print("   docker-compose up gradio")
    
    print("\n5. 访问应用:")
    print("   Gradio界面: http://localhost:7860")
    print("   API文档: http://localhost:8080/docs")
    print("\n" + "="*60)


def main():
    """主函数"""
    print("="*60)
    print("CareReader 项目初始化")
    print("="*60)
    
    # 切换到项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 步骤1: 检查Python版本
    print_step(1, "检查Python版本")
    if not check_python_version():
        return 1
    
    # 步骤2: 创建虚拟环境
    print_step(2, "创建虚拟环境")
    if not create_venv():
        return 1
    
    # 步骤3: 安装依赖
    print_step(3, "安装依赖")
    if not install_dependencies():
        return 1
    
    # 步骤4: 配置环境变量
    print_step(4, "配置环境变量")
    if not create_env_file():
        print("警告: .env文件配置未完成，请手动创建")
    
    # 打印后续步骤
    print_next_steps()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

