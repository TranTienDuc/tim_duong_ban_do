import streamlit as st
import streamlit.components.v1 as components

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np
from search import *


romania_map = UndirectedGraph(dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    Drobeta=dict(Mehadia=75),
    Eforie=dict(Hirsova=86),
    Fagaras=dict(Sibiu=99),
    Hirsova=dict(Urziceni=98),
    Iasi=dict(Vaslui=92, Neamt=87),
    Lugoj=dict(Timisoara=111, Mehadia=70),
    Oradea=dict(Zerind=71, Sibiu=151),
    Pitesti=dict(Rimnicu=97),
    Rimnicu=dict(Sibiu=80),
    Urziceni=dict(Vaslui=142)))

romania_map.locations = dict(
    Arad=(91, 492), Bucharest=(400, 327), Craiova=(253, 288),
    Drobeta=(165, 299), Eforie=(562, 293), Fagaras=(305, 449),
    Giurgiu=(375, 270), Hirsova=(534, 350), Iasi=(473, 506),
    Lugoj=(165, 379), Mehadia=(168, 339), Neamt=(406, 537),
    Oradea=(131, 571), Pitesti=(320, 368), Rimnicu=(233, 410),
    Sibiu=(207, 457), Timisoara=(94, 410), Urziceni=(456, 350),
    Vaslui=(509, 444), Zerind=(108, 531))

city_name = dict(
    Arad=(-35, 0), Bucharest=(0, 15), Craiova=(-20, 15),
    Drobeta=(-50, 0), Eforie=(0, 15), Fagaras=(10, 0),
    Giurgiu=(10, 0), Hirsova=(10, 0), Iasi=(10, 0),
    Lugoj=(10, 0), Mehadia=(10, 0), Neamt=(10, -5),
    Oradea=(-50, 0), Pitesti=(-5, 20), Rimnicu=(10, -5),
    Sibiu=(0, -20), Timisoara=(-60, 0), Urziceni=(0, 15),
    Vaslui=(10, 0), Zerind=(-50, 0))

map_locations = romania_map.locations
graph_dict = romania_map.graph_dict

lst_city = []
for city in city_name:
    lst_city.append(city)

xmin = 91
xmax = 562
ymin = 270
ymax = 570

def ve_ban_do():
    fig, ax = plt.subplots()
    ax.axis([xmin-70, xmax+70, ymin-70, ymax+70])

    for key in graph_dict:
        city = graph_dict[key]
        x0 = map_locations[key][0]
        y0 = map_locations[key][1]

        diem, = ax.plot(x0, y0, 'rs')

        dx = city_name[key][0]
        dy = city_name[key][1]
        ten = ax.text(x0+dx,y0-dy,key,fontsize = 6)

        for neighbor in city:
            x1 = map_locations[neighbor][0]
            y1 = map_locations[neighbor][1]
            doan_thang, = ax.plot([x0, x1], [y0, y1], 'b')
    return fig


if "flag_anim" not in st.session_state:
    st.session_state["flag_anim"] = False
if st.session_state["flag_anim"] == False:
    if "flag_ve_ban_do" not in st.session_state:
        st.session_state["flag_ve_ban_do"] = True
        fig = ve_ban_do()
        st.session_state['fig'] = fig
        st.pyplot(fig)
        print(st.session_state["flag_ve_ban_do"])
        print('Vẽ bản đồ lần đầu')
    else:
        if st.session_state["flag_ve_ban_do"] == False:
            st.session_state["flag_ve_ban_do"] = True
            fig = ve_ban_do()
            st.session_state['fig'] = fig
            st.pyplot(fig)
        else:
            print('Đã vẽ bản đồ')
            st.pyplot(st.session_state['fig'])
    lst_city = []
    for city in city_name:
        lst_city.append(city)

    start_city = st.selectbox('Bạn chọn thành phố bắt đầu:', lst_city)
    dest_city = st.selectbox('Bạn chọn thành phố đích:', lst_city)

    st.session_state['start_city'] = start_city
    st.session_state['dest_city']  = dest_city


    if st.button('Direction'):
        romania_problem = GraphProblem(start_city, dest_city, romania_map)
        c = astar_search(romania_problem)
        lst_path = c.path()
        print('Con duong tim thay: ')

        for data in lst_path:
            city = data.state 
            print(city, end = ' ')
        print()
        path_locations = {}
        for data in lst_path:
            city = data.state
            path_locations[city] = map_locations[city]
        print(path_locations)

        lst_path_location_x = []
        lst_path_location_y = []

        for city in path_locations:
            lst_path_location_x.append(path_locations[city][0])
            lst_path_location_y.append(path_locations[city][1])

        print(lst_path_location_x)
        print(lst_path_location_y)


        fig, ax = plt.subplots()
        ax.axis([xmin-70, xmax+70, ymin-70, ymax+70])

        for key in graph_dict:
            city = graph_dict[key]
            x0 = map_locations[key][0]
            y0 = map_locations[key][1]

            diem, = ax.plot(x0, y0, 'rs')

            dx = city_name[key][0]
            dy = city_name[key][1]
            ten = ax.text(x0+dx,y0-dy,key, fontsize = 6)

            for neighbor in city:
                x1 = map_locations[neighbor][0]
                y1 = map_locations[neighbor][1]
                doan_thang, = ax.plot([x0, x1], [y0, y1], 'b')

            path_tim_thay, = ax.plot(lst_path_location_x, lst_path_location_y, 'g')
        print('Đã gán fig có hướng dẫn')
        st.session_state['fig'] = fig
        st.rerun()

    if st.button('Run'):
        start_city = st.session_state['start_city']
        dest_city = st.session_state['dest_city']

        romania_problem = GraphProblem(start_city, dest_city, romania_map)
        c = astar_search(romania_problem)
        lst_path = c.path()
        print('Con duong tim thay: ')

        for data in lst_path:
            city = data.state 
            print(city, end = ' ')
        print()
        path_locations = {}
        for data in lst_path:
            city = data.state
            path_locations[city] = map_locations[city]
        print(path_locations)

        lst_path_location_x = []
        lst_path_location_y = []

        for city in path_locations:
            lst_path_location_x.append(path_locations[city][0])
            lst_path_location_y.append(path_locations[city][1])

        print(lst_path_location_x)
        print(lst_path_location_y)


        fig, ax = plt.subplots()

        dem = 0

        lst_doan_thang = []
        for key in graph_dict:
            city = graph_dict[key]
            x0 = map_locations[key][0]
            y0 = map_locations[key][1]

            diem, = ax.plot(x0, y0, 'rs')
            lst_doan_thang.append(diem)

            dx = city_name[key][0]
            dy = city_name[key][1]
            ten = ax.text(x0+dx,y0-dy,key)
            lst_doan_thang.append(ten)

            for neighbor in city:
                x1 = map_locations[neighbor][0]
                y1 = map_locations[neighbor][1]
                doan_thang, = ax.plot([x0, x1], [y0, y1], 'b')
                lst_doan_thang.append(doan_thang)
                dem = dem + 1

            path_tim_thay, = ax.plot(lst_path_location_x, lst_path_location_y, 'g')
            lst_doan_thang.append(path_tim_thay)

        print('Dem: ', dem)

        N = 11
        d = 100
        lst_vi_tri_x = []
        lst_vi_tri_y = []

        L = len(lst_path_location_x)
        for i in range(0,L-1):
            x1 = lst_path_location_x[i]
            y1 = lst_path_location_y[i]
            x2 = lst_path_location_x[i+1]
            y2 = lst_path_location_y[i+1]
            
            d0 = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            N0 = int(N*d0/d)
            dt = 1/(N0-1)
            for j in range(0, N0):
                t = j*dt
                x = x1 + (x2-x1)*t
                y = y1 + (y2-y1)*t
                lst_vi_tri_x.append(x)
                lst_vi_tri_y.append(y)

        red_circle, = ax.plot([],[],"ro",markersize = 10)

        FRAME = len(lst_vi_tri_x)

        def init():
            ax.axis([xmin-70, xmax+70, ymin-70, ymax+70])
            # Trả về nhiều đoạn thẳng và đoạn thẳng tìm được
            return lst_doan_thang, red_circle

        def animate(i):
            red_circle.set_data(lst_vi_tri_x[i], lst_vi_tri_y[i])
            return lst_doan_thang, red_circle 

        anim = FuncAnimation(fig, animate, frames=FRAME, interval=100, init_func=init, repeat=False)

        st.session_state["flag_anim"] = True
        st.session_state['anim'] = anim
        st.rerun()

else:
    if st.session_state["flag_anim"] == True:
        components.html(st.session_state["anim"].to_jshtml(), height = 550)
        _, _, col3, _, _ = st.columns(5)
        if col3.button('Reset'):
            st.session_state["flag_anim"] = False
            st.session_state["flag_ve_ban_do"] = False
            st.rerun()

