import streamlit as st
import json
import requests
import altair as alt
from streamlit_option_menu import option_menu
   
def main(prompt):
        
    url = "https://qianfan.baidubce.com/v2/app/conversation/runs"
    
    payload = json.dumps({
        "app_id": "b27975aa-187e-4c62-a42a-a264715f1d95",
        "query": prompt,
        "conversation_id": "83f18dc3-d0ff-4690-9175-d3f4fd4e383d",
        "stream": False
    }, ensure_ascii=False)
    headers = {
        'Content-Type': 'application/json',
        'X-Appbuilder-Authorization': 'Bearer bce-v3/ALTAK-p9qRLsft9cRyQk3bbmlal/fceb7d71a4e1b8a0059d74123e8b1517962e20bb'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    # output=json.loads(response.text)
    
    return response.text  

st.set_page_config(    
    page_title="医学统计AI+",    
    page_icon="🏂",    
    layout="wide",    
    initial_sidebar_state="expanded")    

alt.themes.enable("dark")    
    
with st.sidebar:
    st.header('🤖统计分析AI+')
    selected = option_menu(menu_title='目录',options=['连续性变量',
                                                    '离散性变量',
                                                    '其它'],menu_icon='hospital-fill',icons=['activity', 'heart', 'bar-chart-fill'],default_index=0)
    
if selected == '连续性变量':  
    st.subheader('🤖连续性变量的AI辅助分析')
    with st.sidebar.container():
        st.sidebar.write('说明：')
        st.sidebar.write('该APP结合了LLM理解用户意图、解释分析结果等特点和统计API服务相结合，以实现准确智能的医学统计分析。')
    st.sidebar.write('''
    问句示例：
    1. 请提供一组rm_anova模拟数据
    2. 使用模拟数据进行球形检验
    3. 将结果整理成表格，并解释说明                   
    ''')
    
    #经典的问句
    # api_key=st.secrets["API_key"]
    # secret_key=st.secrets["secret_key"]
    # 刚开始没有任何对话的时候，（state里面没有messages这个字段）
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "你好！我是AI辅助医学统计分析，可以进行统计分析的规划、执行和生成报告等工作。"}]
    # for msg in st.session_state["messages"]:
    #     st.chat_message(msg["role"]).write(msg["content"])  
    # 添加用户输入到message，字典{role: user, content: prompt}
    if prompt := st.chat_input():   
        st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the prior chat messages
    for message in st.session_state.messages: 
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = main(prompt)
                msg = json.loads(response)
                answer = msg["answer"]
                st.session_state.messages.append({'role':'assistant','content':answer})#后台necessary，role 和content
                st.write(answer)#

elif selected == '离散性变量':
    st.subheader('🤖离散性变量')
    "building..."
elif selected == '其它':
    st.subheader('🤖其它')
    "building..."