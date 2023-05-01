import xml.etree.ElementTree as ET
import os

xml_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\output_ucl\001\r_1000\0th'
xml_path=os.path.join(xml_dir,'network.xml')


# 构建带有doctype声明的XML文本
doctype = '<?xml version="1.0" encoding="UTF-8"?>\n <!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v2.dtd">'


# Load XML file
tree = ET.parse(xml_path)
root = tree.getroot()

# Find the XML tag that we want to change the value of
index=0
for title in root.iter('link'):
    # Set the new value for the XML tag
    temp_id=int(title.attrib['id'])
    if temp_id>200:
        continue
    else:
        title.attrib['freespeed'] = "0.0"
        title.attrib['capacity'] = "0.0"
    index+=1

xml_str = ET.tostring(root).decode('utf-8')
xml_str_with_doctype = '{}{}'.format(doctype, xml_str)

# # Write the updated XML to the file
export_path=os.path.join(xml_dir,'network_output.xml')
# 输出XML文本
with open(export_path, 'w') as f:
    f.write(xml_str_with_doctype)
# print(type(tree))
# tree.write(export_path, xml_declaration=True, encoding='utf-8', method="xml")
print("XML tag updated successfully!")