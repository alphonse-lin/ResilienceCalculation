import matsim
import pandas as pd
from collections import defaultdict
import os
import matplotlib.pyplot as plt

def exportBasedOnTime(geo, output_path, t_start, t_end):
    link_counts = defaultdict(int)
    events = matsim.event_reader(os.path.join(input_dir,'output_events.xml.gz'), types='entered link,left link')
    print(f"{str(t_start)}-{str(t_end)}")
    for event in events:
        if event['type'] == 'entered link' and int(event['time']) > t_start and int(event['time']) <=t_end:
            link_counts[event['link']] += 1

    # link_counts = pd.DataFrame.from_dict(link_counts, orient='index', columns=['count']).rename_axis('link_id')
    # link_counts.to_csv('link_counts.csv')

    # convert our link_counts dict to a pandas dataframe,
    # with 'link_id' column as the index and 'count' column with value:
    link_counts = pd.DataFrame.from_dict(link_counts, orient='index', columns=['count']).rename_axis('link_id')
    print(link_counts)
    # attach counts to our Geopandas network from above
    volumes = geo.merge(link_counts, on='link_id')
    volumes.to_excel(output_path)
    
    # volumes.plot(column='count', figsize=(10,10), cmap='Wistia') #cmap is colormap
    # plt.show()



if __name__ == '__main__':
    input_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\output_ucl\002\r_global\output'
    # -------------------------------------------------------------------
    # 1. NETWORK: Read a MATSim network:
    net = matsim.read_network(os.path.join(input_dir, 'output_network.xml.gz'))

    geo = net.as_geo()
    # geo.plot()    # try this in a notebook to see your network!

    # -------------------------------------------------------------------
    # 2. EVENTS: Stream through a MATSim event file.

    # The event_reader returns a python generator function, which you can then
    # loop over without loading the entire events file in memory.
    #
    # ---------
    # Example 1: Sum up all 'entered link' events to get link volumes.
    # Supports both .xml.gz and protobuf .pb.gz event file formats!
    # Only returns events of type 'entered link' and 'left link':
    from collections import defaultdict
    
    output_dir=r'D:\Code\114_temp\008_CodeCollection\005_java\matsim_preparation\src\main\resources\output_ucl\002\r_global\output_img'
    events = matsim.event_reader(os.path.join(input_dir,'output_events.xml.gz'), types='entered link,left link')
    # t_start=32400
    # t_end=36000

    # defaultdict creates a blank dict entry on first reference; similar to {} but more friendly
    link_counts = defaultdict(int)
    for event in events:
        if event['type'] == 'entered link':
            link_counts[event['link']] += 1

    # convert our link_counts dict to a pandas dataframe,
    # with 'link_id' column as the index and 'count' column with value:
    link_counts = pd.DataFrame.from_dict(link_counts, orient='index', columns=['count']).rename_axis('link_id')

    # attach counts to our Geopandas network from above
    volumes = geo.merge(link_counts, on='link_id')
    # volumes.plot(column='count', figsize=(10,10), cmap='Wistia') #cmap is colormap
    volumes.to_excel(os.path.join(output_dir,f'link_counts.xlsx'))


    # print("start loop")
    # for i in range(0,30):
    #     t_start=i*3600
    #     t_end=(i+1)*3600
    #     exportBasedOnTime(geo, os.path.join(output_dir,'output_events_{0}.xlsx'.format(i)), t_start, t_end)
    #     print("export {0} done".format(i))

