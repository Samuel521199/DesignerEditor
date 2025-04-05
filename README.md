# UnityMindFlowPro Designer Editor

这是UnityMindFlowPro项目的设计编辑器部分，用于设计和编辑游戏内容。

## 功能特点

- 策划案管理
- 系统框架设计
- 游戏逻辑编辑
- 公式算法数值编辑

## 开发环境设置

1. 安装Python 3.8或更高版本
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 运行方式

### 开发模式
```bash
python src/main.py
```

### 打包成exe
```bash
pyinstaller pyinstaller.spec
```

## 项目结构

- `src/`: 源代码目录
- `resources/`: 资源文件目录
- `docs/`: 文档目录

## 注意事项

- 确保已安装所有依赖包
- 运行前检查Python版本兼容性
- 打包时需要确保resources目录中有icon.ico文件 