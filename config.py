vlm = make_llm(
    base_url="https://api.siliconflow.cn/v1/",
    model="openai/Pro/Qwen/Qwen2-VL-7B-Instruct",
    api_key="sk-whfsgciephkpcjrbmijijiqealycbbycxkwbkwgkyptofbah",
)
llm =  make_llm(
    base_url="https://api.siliconflow.cn/v1/",
    model="openai/Pro/Qwen/Qwen2-VL-7B-Instruct",
    api_key="sk-whfsgciephkpcjrbmijijiqealycbbycxkwbkwgkyptofbah",
)
tagging_llm =llm
emo_llm = llm

db = playhouse.db_url.connect("sqlite:///db.sqlite")
