
def read_file(file):
    
    
    urls = set()

    with open(file, "r", encoding = "utf-8") as f:
        for line in f:

            line = line.strip()

            if line:
                urls.add(line)
            
    return list(urls)


def data_clear(urls):
    
    data = []
    
    for url in urls:
        
        lower_url = url.lower()

        if not (lower_url.startswith("http://") or lower_url.startswith("https://")):
            if not "." in url:

                print(f"{url}----数据有误")
                continue
            
            else:
                url = "http://" + url

        data.append(url)
        
    return data

def file_clean(filepath):

    urls=read_file(filepath)

    return data_clear(urls)