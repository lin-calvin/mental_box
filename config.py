vlm = make_llm(
    base_url="http://api.siliconflow.cn/v1/",
    model="openai/Qwen/Qwen2.5-VL-72B-Instruct",
    api_key="sk-whfsgciephkpcjrbmijijiqealycbbycxkwbkwgkyptofbah",
)
llm =  make_llm(
    base_url="http://api.siliconflow.cn/v1/",
    model="openai/Qwen/Qwen2.5-VL-72B-Instruct",
    api_key="sk-whfsgciephkpcjrbmijijiqealycbbycxkwbkwgkyptofbah",
)
tagging_llm =llm
emo_llm = llm
mocking={
    
}

db = playhouse.db_url.connect("sqlite:///db.sqlite")
