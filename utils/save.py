import json, os
from datetime import datetime
from config import OUTPUT_DIR

def data_save(data, path = "result.json"):
    
    if path.lower().endswith(".txt"):
       func = "txt"
    elif path.lower().endswith(".json"):
        func = "json"
    else:
        raise ValueError(
            "目前仅限保存为.json文件或者.txt文件，请修改后缀后重新提交"
        )
    
    if os.path.basename(path) != path:
        raise ValueError(
        "只允许输入文件名"
    )  

    date = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    output_dir = os.path.join(
        OUTPUT_DIR,
        date
    )

     
    
    path = os.path.join(
        output_dir,
        path
    )


    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    if func == "json":

        with open(
            path,
            "w",
            encoding = "utf-8"
        ) as f:
            json.dump(
                data,
                f,
                ensure_ascii = False,
                indent = 4
            )

    else:

        with open(
            path,
            "w",
            encoding = "utf-8"
        ) as f:
            for res in data:
                f.write(str(res) + "\n")  

    return path