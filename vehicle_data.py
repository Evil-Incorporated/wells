import pandas as pd


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
    data = one_hot(data, dummy_columns=['Lane of the road', 'Road Condition', 'Precipitation',
                                        'Precipitation intensity', 'Day time'])
    # print(len(data.index))
    # print(len(weather.index))
    # data = data.set_index(['ID', 'Date time']).join(weather.set_index(['ID', 'Date time']), how='left').reset_index()
    return data

if __name__ == '__main__':
    data = get_data()
    print(data.columns)