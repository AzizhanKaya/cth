def find_node():
    index = 0
    node = "<node "
    l_index = []

    while True:
        index = content.find(node, index + 1)
        if index == -1:
            break
        l_index.append(index)

    return l_index

def node_level(index):

    spaces=0

    while index > 0 and content[index-1] == ' ':
        spaces += 1
        index -= 1
    
    return spaces


def node_tree():

    indexes = find_node()
    
    return [node_level(idx) // 2 for idx in indexes]

def node_names():

    indexes = find_node()
    names=[]
    for index in indexes:
        lenght=0
        while True:
            if content[index+lenght+13]=='"':
                break
            lenght+=1
        names.append(content[index+12:index+lenght+13])

    return names


def grep_text(content):


    def find_reachtext():

        rich_text = "<rich_text"
        
        indexes = []
        index=0

        while True:
            index = content.find(rich_text, index + 1)
            if index == -1:
                break
            
            
            indexes.append(index)
            index = content.find('<', index + 1)
            indexes.append(index)


        indexes.sort()
        return indexes
    


    indexes = find_reachtext()
    texts=[]
    for n in range(0,len(indexes),2):
        
        texts.append(content[indexes[n]+11:indexes[n+1]])

    return texts


def grep_images():

    def find_image(content):

        encoded_png = "<encoded_png"
        
        indexes = []
        index=0

        while True:
            index = content.find(encoded_png, index + 1)
            
            if index == -1:
                break
            
            index = content.find('>', index + 1)
            indexes.append(index)
            index = content.find('<', index + 1)
            indexes.append(index)

        indexes.sort()
        return indexes
    

    node_indexes = find_node()
    images=[]

    for i in range(len(node_indexes)):

        encoded = []

        if i == len(node_indexes)-1:
            image_indexes = find_image(content[node_indexes[i]:])

            for n in range(0,len(image_indexes),2):
                encoded.append(content[node_indexes[i]:][image_indexes[n]:image_indexes[n+1]])

            images.append(encoded)
            break

        image_indexes = find_image(content[node_indexes[i]:node_indexes[i+1]])

        for n in range(0,len(image_indexes),2):

            encoded.append(content[node_indexes[i]:node_indexes[i+1]][image_indexes[n]:image_indexes[n+1]])

        images.append(encoded)

    


    return images


def process_text(texts, level):

    image = 0

    for index,text in enumerate(texts):
        

        text = text.split('>')
        if len(text) == 1:
            continue

        if text[0][:20] == 'justification="left"':

            texts[index]=f"<img src=/img/{level}/image-{image}.png></img>"

            image +=1
            
            continue

        vars = text[0].split(' ')


        for var in vars:

            if var.split('=')[0] == 'foreground':

                color = var.split('=')[1][2:-1]

                if len(color) == 12:
                    tmp=""
                    for n in range(0,12,2):
                        tmp += color[2*n:2*n+2] 
                    color = tmp
                break

            

        if len(vars) == 1 and vars[0].split('=')[0] == 'scale':

            scale = vars[0].split('=')[1][1:3]
            texts[index] = f"<{scale}>{text[1]}</{scale}>"
            continue
            
        if len(vars) == 2 and vars[0].split('=')[0] == 'scale' and vars[1].split('=')[0] == 'foreground':
            texts[index] = f"<{scale} style='color: #{color}'>{text[1]}</{scale}>"
            continue

        if len(vars) == 2 and vars[0].split('=')[0] == 'foreground' and vars[1].split('=')[0] == 'weight':
            
            texts[index] = f"<b style='color: #{color}'>{text[1]}</b>"
            continue
        
        if len(vars) == 1 and vars[0].split('=')[0] == 'foreground':
            texts[index] = f"<span style='color: #{color}'>{text[1]}</span>"
            continue
        
        if vars[0].split('=')[0] == 'link':

            if vars[0].split('=')[1][1:] == 'webs':
                texts[index] = f"<a href=\"{vars[1]}>{text[1]}</a>"
                continue

            if vars[0].split('=')[1][1:] == 'node':
                texts[index] = f"<node data-id={vars[1][0]}>{text[1]}</node>"

        

    return texts

def get_nodes(node=None):


    indexes = find_node()
    levels = node_tree()
    nodes=[]
    for i in range(0,len(indexes)):

        if i == len(indexes)-1:
            nodes.append(process_text(grep_text(content[indexes[i]:]),i))
            break

        nodes.append(process_text(grep_text(content[indexes[i]:indexes[i+1]]),i))
    
    if node==None:
        return nodes
    else:
        return nodes[node-1]

def parse():

    nodes=[]
    for node in get_nodes():
            
        cherry=""
        for line in node:
            cherry+=line
        
        nodes.append(cherry)

    return node_tree(),node_names(),nodes

def parse_file(file):
    global content
    with open(file, encoding='UTF-8') as f:
        content = f.read()
    
    return parse()

