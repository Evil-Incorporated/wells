import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns


def one_hot(table, dummy_columns=None):
    if dummy_columns is not None:
        table = pd.get_dummies(table, columns=dummy_columns)
    return table


def get_data():
    vehicle = pd.read_csv('Train.csv')
    # vehicle = pd.get_dummies(vehicle, columns=['DrivingStyle'])
    vehicle_travelling = pd.read_csv('Train_Vehicletravellingdata.csv')
    vehicle_travelling['Date time'] = pd.to_datetime(vehicle_travelling['Date time'])
    # vehicle_travelling = pd.get_dummies(vehicle_travelling, columns=['Lane of the road', 'Road Condition'])
    weather = pd.read_csv('Train_WeatherData.csv')
    weather['Date time'] = pd.to_datetime(weather['Date time'])
    # weather = pd.get_dummies(weather, columns=['Precipitation', 'Precipitation intensity', 'Day time'])
    weather = weather.drop(['ID', 'Date time'], axis=1)
    data = vehicle_travelling.merge(weather, left_index=True, right_index=True)
    data = vehicle.set_index('ID').join(data.set_index('ID'), how='left').reset_index()
    data = one_hot(data, dummy_columns=['DrivingStyle', 'Lane of the road', 'Road Condition', 'Precipitation',
                                        'Precipitation intensity', 'Day time'])
    # print(len(data.index))
    # print(len(weather.index))
    # data = data.set_index(['ID', 'Date time']).join(weather.set_index(['ID', 'Date time']), how='left').reset_index()
    return data


def plot_data(data):
    driving_style1 = []
    driving_style2 = []
    driving_style3 = []
    for id, v_data in data.groupby(['ID']):
        # print(v_data['Time gap with the preceeding vehicle in seconds'].mean(), v_data['DrivingStyle'].iloc[0])
        driving_style = v_data['DrivingStyle'].iloc[0]
        mean_time_gap = v_data['Speed of the vehicle (kph)'].max() # - v_data['Speed of the preceding vehicle'].mean()
        if driving_style == 1:
            driving_style1.append(mean_time_gap)
        elif driving_style == 2:
            driving_style2.append(mean_time_gap)
        elif driving_style == 3:
            driving_style3.append(mean_time_gap)
    plt.scatter(np.zeros(len(driving_style1)), driving_style1, label='Driving Style1')
    plt.scatter(np.zeros(len(driving_style2)) + 1, driving_style2, label='Driving Style2')
    plt.scatter(np.zeros(len(driving_style3)) + 2, driving_style3, label='Driving Style3')
    plt.legend()
    plt.show()


def plot_corr(data):
    corr = data.corr()
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, cmap='Blues')
    plt.show()


def drop_columns(data):
    print(data.columns)
    data = data.drop(['weight of vehicle in kg', 'Number of axles', 'ID of the preceding vehicle',
                      'Weight of the preceding vehicle'], axis=1)
    return data


if __name__ == '__main__':
    data = get_data()
    data = drop_columns(data)
    plot_corr(data)