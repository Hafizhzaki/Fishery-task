import pandas as pd
import glob
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def pseudo2time(pseudo_timestamp):
    timestamp = datetime.fromtimestamp(pseudo_timestamp / 1000)
    return timestamp

def eat_feeding_durarion(combined_df):
    eat_duration=[]
    df_start=combined_df[combined_df['label'].diff()==1].reset_index(drop=True)
    df_end=combined_df[combined_df['label'].diff()==-1].reset_index(drop=True)    
    if combined_df['label'][0]==1:
        start=combined_df['timestamp'][0]
        eat_duration=[df_end["timestamp"][0]-start]
        for i in range(len(df_start)):
            eat_duration.append(df_end["timestamp"][i+1]-df_start['timestamp'][i])
    else:
        for i in range(len(df_start)):
            eat_duration.append(df_end["timestamp"][i]-df_start['timestamp'][i])
    feeding_duration=df_start["timestamp"].diff().tolist()
    feeding_duration[0]=df_start["timestamp"][0]-start
    sum_time=timedelta(days=0, hours=0, minutes=0)
    for e in feeding_duration:
        sum_time+=e
    average_feeding=sum_time/len(feeding_duration)
    sum_time=timedelta(days=0, hours=0, minutes=0)
    for e in eat_duration:
        sum_time+=e
    average_eat=sum_time/len(eat_duration)
    return feeding_duration,eat_duration,average_feeding,average_eat

def eat_vs_noteat(combined_df):
    combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])
    # Membuat plot
    fig, ax = plt.subplots()

    # Mengelompokkan data berdasarkan label
    groups = combined_df.groupby('label')

    # Looping untuk menggambar setiap grup
    id2label={0:"tidak makan",1:"makan"}
    for label in ["x","y","z"]:
        for name, group in groups:
            ax.plot(group['timestamp'], group[label], label=id2label[name])

        # Menambahkan judul dan label sumbu
        ax.set_title('Line Chart %s'%label)
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Value')

        # Menampilkan legenda
        ax.legend()

        # Menampilkan plot
        plt.savefig('image/eat_vs_noteat_%s.png'%label)
    return groups

def eat_group(combined_df):
    combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])
    eat_df=combined_df[combined_df["label"]==1]
    time_diff = eat_df['timestamp'].diff()
    time_threshold = pd.Timedelta(seconds=1)
    group_labels = (time_diff > time_threshold).cumsum()
    eat_df['group'] = group_labels
    eat_df=eat_df.reset_index(drop=True)
    return eat_df

if __name__ == '__main__':
    dfs = []
    files = glob.glob("dataset/*.xlsx")
    for file in files:
        df = pd.read_excel(file)
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df = combined_df.sort_values('timestamp').reset_index(drop=True)
    combined_df['timestamp'] = combined_df['timestamp'].apply(pseudo2time)
    feeding_duration,eat_duration,average_feeding,average_eat=eat_feeding_durarion(combined_df)
    groups_eat_noteat=eat_vs_noteat(combined_df)
    eat_df=eat_group(combined_df)

    #preprocessing
    print(combined_df)
    #waktu makan
    print(eat_duration,average_eat)
    #jadwal makan
    print(feeding_duration,average_feeding)
    #eksplorasi data
    id2label={0:"tidak makan",1:"makan"}
    for name, group in groups_eat_noteat:
        print(id2label[name])
        print(group.describe()[['x','y','z']])
    for i in eat_df["group"].unique():
        print(i)
        eat_group=eat_df[eat_df["group"]==i]
        print(eat_group.describe()[['x','y','z']])