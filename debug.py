import json
from datetime import datetime
from typing import Dict, List
import time
from api import (
    generate_role_appearance,
    get_characterglm_response,
    CharacterMeta,
    TextMsg,
    TextMsgList
)
class RolePlayGenerator:
    def __init__(self):
        self.dialogue_history: List[Dict] = []

    def simulate_conversation(
        self,
        role1: Dict[str, str],
        role2: Dict[str, str],
        max_turns: int = 4,
        scene: str = "在咖啡馆聊天"
    ) -> bool:
        """更健壮的对话生成方法"""
        
        # 构建更详细的角色元数据
        meta1 = {
            "bot_name": role1["name"],
            "bot_info": (
                f"姓名：{role1['name']}\n"
                f"性别：{role1['gender']}\n"
                f"年龄：{role1['age']}\n"
                f"性格：{role1['personality']}\n"
                f"背景：{role1['background']}\n"
                f"特征：{role1['features']}"
            ),
            "user_name": role2["name"],
            "user_info": f"姓名：{role2['name']}\n性别：{role2['gender']}"
        }
        
        meta2 = {
            "bot_name": role2["name"],
            "bot_info": (
                f"姓名：{role2['name']}\n"
                f"性别：{role2['gender']}\n"
                f"年龄：{role2['age']}\n"
                f"性格：{role2['personality']}\n"
                f"背景：{role2['background']}\n"
                f"特征：{role2['features']}"
            ),
            "user_name": role1["name"],
            "user_info": f"姓名：{role1['name']}\n性别：{role1['gender']}"
        }

        # 更丰富的初始prompt
        initial_prompt = (
            f"场景：{scene}\n"
            f"{role1['name']}（{role1['personality'].split(',')[0]}）"
            f"和{role2['name']}（{role2['personality'].split(',')[0]}）"
            "正在进行对话。请根据他们的角色设定自然地展开对话。"
            f"由{role1['name']}先开始发言。"
        )
        
        self.dialogue_history = [{
            "role": "system", 
            "content": initial_prompt
        }]

        current_meta = meta1
        next_meta = meta2
        
        for turn in range(max_turns):
            try:
                print(f"\n第{turn+1}轮生成中...")
                time.sleep(2)  # 增加延迟
                
                # 打印调试信息
                print("当前角色:", current_meta["bot_name"])
                print("对话历史:", [msg["content"][:50]+"..." for msg in self.dialogue_history[-2:]])
                
                # 获取API响应
                response = list(get_characterglm_response(
                    messages=self.dialogue_history,
                    meta=current_meta
                ))
                
                print(f"API原始响应: {response}")  # 添加这行查看原始响应

                if not response:
                    print("⚠️ 收到空响应，尝试重新生成...")
                    response = list(get_characterglm_response(
                        messages=self.dialogue_history,
                        meta=current_meta))
                
                reply = "".join(response).strip()
                print("生成内容:", reply)
                
                if not reply:
                    print("❌ 仍然收到空响应，终止对话")
                    return False
                
                self.dialogue_history.append({
                    "role": "assistant",
                    "content": reply
                })
                
                # 切换角色
                current_meta, next_meta = next_meta, current_meta
                
            except Exception as e:
                print(f"❌ 出错: {str(e)}")
                return False
        
        return True


# 最小测试用例
role1 = {
    "name": "测试角色A",
    "gender": "男",
    "age": "30",
    "personality": "幽默,健谈,好奇",
    "background": "软件工程师",
    "features": "喜欢喝咖啡"
}

generator = RolePlayGenerator()
success = generator.simulate_conversation(
    role1, role1,  # 用相同角色测试
    max_turns=2,
    scene="在办公室闲聊"
)

# 在get_characterglm_response调用后添加
print("完整响应:", response)
print("响应类型:", type(response))
print("响应长度:", len(response))
