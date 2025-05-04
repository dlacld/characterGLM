import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import time
from api import (
    generate_role_appearance,
    get_chatglm_response_via_sdk,  # 使用新版SDK的ChatGLM
    CharacterMeta,
    TextMsgList
)

class RolePlayGenerator:
    def __init__(self):
        self.dialogue_history: List[Dict] = []

    def generate_role_profile(self, raw_text: str) -> Dict[str, str]:
        """生成角色人设信息"""
        instruction = f"""请根据以下文本生成角色设定，必须包含：
name: 角色名
gender: 性别  
age: 年龄
personality: 性格特点
background: 背景故事
features: 特征

严格按照以下格式：
name: 值
gender: 值
age: 值
personality: 值
background: 值
features: 值

文本内容：
{raw_text}"""
        
        response = "".join(list(generate_role_appearance(instruction)))
        profile = {}
        for line in response.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                profile[key.strip().lower()] = val.strip()
        return profile

    def simulate_conversation(
        self,
        role1: Dict[str, str],
        role2: Dict[str, str],
        max_turns: int = 4,
        scene: str = "在咖啡馆相遇"
    ) -> bool:
        """使用ChatGLM模拟对话"""
        
        # 构建对话上下文
        context = [
            {
                "role": "system",
                "content": (
                    f"你正在模拟两个角色之间的对话。\n"
                    f"角色1: {role1['name']}({role1['personality']})\n"
                    f"角色2: {role2['name']}({role2['personality']})\n"
                    f"场景: {scene}\n"
                    f"请交替生成两个角色的回复，保持对话自然连贯。"
                )
            }
        ]

        current_speaker = role1
        next_speaker = role2
        
        for turn in range(max_turns):
            try:
                time.sleep(1)  # 请求间隔
                
                # 生成当前角色的发言
                prompt = (
                    f"请以{current_speaker['name']}的身份回复，"
                    f"性格特点: {current_speaker['personality']}\n"
                    f"背景: {current_speaker['background']}\n"
                    "请生成一段自然对话内容:"
                )
                
                context.append({"role": "user", "content": prompt})
                
                # 使用新版SDK调用ChatGLM
                response = list(get_chatglm_response_via_sdk(
                    messages=context
                ))
                reply = "".join(response).strip()
                
                if not reply:
                    print(f"第{turn+1}轮收到空响应")
                    return False
                
                # 添加到对话历史
                self.dialogue_history.append({
                    "role": "assistant",
                    "content": reply,
                    "speaker": current_speaker["name"]
                })
                
                # 切换角色
                current_speaker, next_speaker = next_speaker, current_speaker
                
            except Exception as e:
                print(f"生成对话出错: {e}")
                return False
        
        return True

    def save_dialogue(
        self,
        file_path: str,
        role1: Dict[str, str],
        role2: Dict[str, str],
        dialogue: List[Dict]
    ):
        """保存对话数据"""
        data = {
            "metadata": {
                "role1": role1,
                "role2": role2,
                "generate_time": datetime.now().isoformat()
            },
            "dialogue": dialogue
        }
        
        Path(file_path).parent.mkdir(exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # 测试角色数据
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

    print("=== 开始对话生成(使用ChatGLM) ===")
    generator = RolePlayGenerator()
    
    if generator.simulate_conversation(
        role1, role2,
        max_turns=6,
        scene="在网络安全会议上讨论数据加密技术"
    ):
        # 保存结果
        output_file = "output/chatglm_dialogue.json"
        generator.save_dialogue(output_file, role1, role2, generator.dialogue_history)
        
        print("\n对话生成成功！")
        for msg in generator.dialogue_history:
            print(f"{msg['speaker']}: {msg['content']}")
    else:
        print("\n生成失败，请检查API_KEY和网络连接")

if __name__ == "__main__":
    main()