from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv 
load_dotenv(override=True)



DeepSeek_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# print(DeepSeek_API_KEY)  # 可以通过打印查看


# 初始化 Playwright 浏览器：
sync_browser = create_sync_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
tools = toolkit.get_tools()


# 通过 LangChain Hub 拉取提示词模版
prompt = hub.pull("hwchase17/openai-tools-agent")


# # 初始化模型
model = init_chat_model("deepseek-chat", model_provider="deepseek")

# 通过 LangChain 创建 OpenAI 工具代理
agent = create_openai_tools_agent(model, tools, prompt)

# 通过 AgentExecutor 执行代理
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


if __name__ == "__main__":
    # 定义任务
    command = {
        "input": "访问这个网站 https://github.com/fufankeji/MateGen/blob/main/README_zh.md 并帮我总结一下这个网站的内容"
    }

    # 执行任务
    response = agent_executor.invoke(command)
    print(response)