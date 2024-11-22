# macOS Color Picker

一个强大的macOS原生颜色选择和图片生成工具，专为设计师、开发者和创意工作者设计。

## 主要功能

- 🎨 从图片中提取颜色
  - 实时显示鼠标位置的颜色值
  - 支持RGB和HEX格式
  - 一键复制颜色值到剪贴板

- 📸 生成纯色图片
  - 支持多种预设比例：16:9、4:3、1:1、3:2、9:16
  - 支持自定义尺寸
  - 最高支持8K分辨率(7680×4320)
  - 支持PNG和JPEG格式导出

- 🖥️ 原生macOS体验
  - 针对Apple Silicon (M1/M2)优化
  - 简洁直观的用户界面
  - 快速响应的交互体验

## 系统要求

- macOS 10.14或更高版本
- Python 3.9+
- 推荐使用Apple Silicon芯片的Mac设备

## 安装步骤

1. 克隆项目
```bash
git clone https://github.com/zenenznze/macos-color-picker.git
cd macos-color-picker
```

2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

## 运行应用

激活虚拟环境后运行：
```bash
python color_picker.py
```

## 使用说明

1. 打开图片：点击"打开图片"按钮选择要分析的图片
2. 提取颜色：
   - 移动鼠标查看实时颜色值
   - 点击图片固定选择该位置的颜色
3. 复制颜色：
   - 点击"复制RGB"获取RGB格式
   - 点击"复制HEX"获取十六进制格式
4. 生成图片：
   - 点击"生成纯色图片"
   - 选择预设比例或自定义尺寸
   - 选择保存位置和格式

## 技术栈

- Python 3.12
- PyQt6 6.5.0 - GUI框架
- Pillow 10.1.0 - 图像处理

## 许可证

本项目采用 [MIT](LICENSE) 许可证。

这意味着你可以：
- ✅ 商业使用
- ✅ 修改源码
- ✅ 分发
- ✅ 私人使用

唯一的要求是保留原始许可证和版权声明。

## 贡献

欢迎提交Issue和Pull Request！
