# characterGLM


## 介绍

characterGLM  是一个使用 AI LLM 实现2个不同角色的 AI 机器人进行相互问答

这个工具使用了大型语言模型 (LLMs) ，基于 Python 构建，并且具有灵活、模块化和面向对象的设计。



## 特性

- [x] 基于Markdown 格式虚拟2个不同角色的机器人进行对换
- [x] 基于场景的人设，可以指定场景进行聊天，交替生成回复
- [x] 生成的对话数据保存至Jason文件


## 开始使用

### 环境准备

1.克隆仓库 `git clone `

2.需要 Python 3.10 或更高版本，使用 pip install  提前安装依赖项

3.默认使用智谱 LLM  glm-3-turbo 进行调用

### 使用示例

命令行直接运行：

```bash
python main.py
```

代码中使用最多6轮进行双角色的互动. 

```python
    if generator.simulate_conversation(
       role1, role2,
       max_turns=6,
     	 scene="在网络安全会议上讨论数据加密技术"
```

角色类型也可以在主文件定义，使用Markdown 格式

```python
    role1 = {
        "name": "李博",
        "gender": "男",
        "age": "28",
        "personality": "冷静理性,注重细节",
        "background": "网络安全专家",
        "features": "随身携带加密U盘"
    }
    
    role2 = {
        "name": "林记者",
        "gender": "女", 
        "age": "25",
        "personality": "好奇心强,善于提问",
        "background": "科技记者",
        "features": "带着录音笔"
    }
```

## 运行页面案例



![sample_car_pic](images/diag_snap.png)

## 许可证

该项目采用 GPL-3.0 许可证。有关详细信息，请查看 [LICENSE](LICENSE) 文件。



