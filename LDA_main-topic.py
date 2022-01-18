import re
import os

__author__ = "YU Yang"


# Extract topic keywords
def extract_source(filedir):

    with open(filedir, 'r', encoding = 'utf-8') as record:
        data = record.readlines()

    topic_list = []
        
    for line in data:
        try:
            topic = line.split(": INFO :")[1].strip()
            if topic.startswith("topic #"):
                topic_list.append(topic)
        except:
            continue
            
    topic_list = list(set(topic_list))   #remove completely same topic

    topic_dict = {}

    for topic_line in topic_list:
        index = topic_line.split(":")[0].strip()
        num = re.findall(r"topic #(.+?) ", index)[0]
        
        num = '#' + str(num)
        keywords = topic_line.split(":")[1].split(" + ")
        
        for keyword in keywords:
            if num not in topic_dict:
                topic_dict[num] = set()
            topic_dict[num].add(keyword.strip())


    for index, keywords_set in topic_dict.items():
        key_weight_dict = {}
        for keywords in keywords_set:
            try:
                weight = (keywords.split("*")[0])
                key = keywords.split("*")[1].strip('"')
            except:
                continue

            if key not in key_weight_dict:
                key_weight_dict[key] = [weight]
            else:
                key_weight_dict[key].append(weight)
            
        topic_dict[index] = key_weight_dict


    topic_dict = dict(sorted(topic_dict.items()))
    topic_num = len(topic_dict.keys())
    print("Total topic nums: {}".format(topic_num))
    return topic_dict, topic_num


# Write topic keywords to local
def write_topic(topic_dict, filename, topic_num):
    
    with open('./Topic/{}_Topic-{}.txt'.format(filename, topic_num), 'w+', encoding = "utf-8") as f:
        for topic in topic_dict.items():
            f.write(str(topic))
            f.write("\n\n")
        
        f.write("\n\n")
        f.write("----------------------------------------------------")
        f.write("\n\n")
        f.write("Total topic nums: {}".format(len(topic_dict.keys())))


# Main function
def main():
    os.chdir(os.path.dirname(__file__))

    for root, _, filenames in os.walk("./LDA_source/"):
        for filename in filenames:
            filedir = os.path.join(root, filename)
            
            topic_dict, topic_num = extract_source(filedir)
            write_topic(topic_dict, filename, topic_num)
    
    print("Extract complete!")

if __name__ == "__main__":
    main()