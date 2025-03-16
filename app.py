import streamlit as st
import pandas as pd
import numpy as np
# Реальные средние температуры (примерные данные) для городов по сезонам
seasonal_temperatures = {
    "New York": {"winter": 0, "spring": 10, "summer": 25, "autumn": 15},
    "London": {"winter": 5, "spring": 11, "summer": 18, "autumn": 12},
    "Paris": {"winter": 4, "spring": 12, "summer": 20, "autumn": 13},
    "Tokyo": {"winter": 6, "spring": 15, "summer": 27, "autumn": 18},
    "Moscow": {"winter": -10, "spring": 5, "summer": 18, "autumn": 8},
    "Sydney": {"winter": 12, "spring": 18, "summer": 25, "autumn": 20},
    "Berlin": {"winter": 0, "spring": 10, "summer": 20, "autumn": 11},
    "Beijing": {"winter": -2, "spring": 13, "summer": 27, "autumn": 16},
    "Rio de Janeiro": {"winter": 20, "spring": 25, "summer": 30, "autumn": 25},
    "Dubai": {"winter": 20, "spring": 30, "summer": 40, "autumn": 30},
    "Los Angeles": {"winter": 15, "spring": 18, "summer": 25, "autumn": 20},
    "Singapore": {"winter": 27, "spring": 28, "summer": 28, "autumn": 27},
    "Mumbai": {"winter": 25, "spring": 30, "summer": 35, "autumn": 30},
    "Cairo": {"winter": 15, "spring": 25, "summer": 35, "autumn": 25},
    "Mexico City": {"winter": 12, "spring": 18, "summer": 20, "autumn": 15},
}

# Сопоставление месяцев с сезонами
month_to_season = {12: "winter", 1: "winter", 2: "winter",
                   3: "spring", 4: "spring", 5: "spring",
                   6: "summer", 7: "summer", 8: "summer",
                   9: "autumn", 10: "autumn", 11: "autumn"}

# Генерация данных о температуре
def generate_realistic_temperature_data(cities, num_years=10):
    dates = pd.date_range(start="2010-01-01", periods=365 * num_years, freq="D")
    data = []

    for city in cities:
        for date in dates:
            season = month_to_season[date.month]
            mean_temp = seasonal_temperatures[city][season]
            # Добавляем случайное отклонение
            temperature = np.random.normal(loc=mean_temp, scale=5)
            data.append({"city": city, "timestamp": date, "temperature": temperature})

    df = pd.DataFrame(data)
    df['season'] = df['timestamp'].dt.month.map(lambda x: month_to_season[x])
    return df

# Функция для расчета скользящего среднего
def calculate_rolling_mean(df):
    df['rolling_mean'] = df.groupby('city')['temperature'].rolling(window=30, min_periods=1).mean().reset_index(0, drop=True)
    return df
    
# Функция для расчета средней температуры и стандартного отклонения для каждого сезона и города
def calculate_seasonal_stats(df):
    stats = df.groupby(['city', 'season']).agg(
        avg_temp=('temperature', 'mean'),
        std_temp=('temperature', 'std')
    ).reset_index()
    return stats


# Функция для выявления аномалий
def detect_anomalies(df):
    df['anomaly'] = ((df['temperature'] > df['avg_temp'] + 2 * df['std_temp']) | 
                     (df['temperature'] < df['avg_temp'] - 2 * df['std_temp']), 'Anomaly', 'Normal')
    return df

# Кнопка для создания и отображения DataFrame
if st.button('Создать DataFrame'):
    st.session_state.data = generate_realistic_temperature_data(list(seasonal_temperatures.keys()))
    st.dataframe(st.session_state.data)

# Кнопка для расчета скользящего среднего
if st.button('Вычислить скользящее среднее'):
        st.session_state.rolling_mean_data = calculate_rolling_mean(st.session_state.data)
        st.dataframe(st.session_state.rolling_mean_data)
    
# Кнопка для расчета средней температуры и стандартного отклонения
if st.button('Рассчитать среднюю температуру и стандартное отклонение'):
    st.session_state.stats = calculate_seasonal_stats(st.session_state.data)
    st.session_state.data=st.session_state.data.merge(st.session_state.stats, on=['city', 'season']) #это делаем для дальнейшего поиска аномалий
    st.dataframe(st.session_state.stats)

# Кнопка для выявления аномалий
if st.button('Выявить аномалии'):
        st.session_state.anomaly_data = detect_anomalies(st.session_state.data)
        st.dataframe(st.session_state.anomaly_data)
