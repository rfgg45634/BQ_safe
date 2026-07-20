from .url_check import check
from utils.save import data_save

def scanner(targets, tr, ts, output_dir):
    
    request_res, selenium_res = check(targets, tr, ts)
    
    result={
        "alive":[],
        "possible":[],
        "dead":[]
    }

    selenium_map = {item["url"]: item for item in selenium_res}

    for item in request_res:
        url = item["url"]
        final = selenium_map.get(url, item)   # 有复核结果就用复核的，没有就用request阶段的
        result[final["alive"]].append(final)

    for item in request_res + selenium_res:

        if item["alive"]=="alive":

            result["alive"].append(item)

        elif item["alive"]=="possible":

            result["possible"].append(item)

        else:

            result["dead"].append(item)

    if not output_dir:
        output_dir = "result.json" 

    data_save(result, output_dir)
