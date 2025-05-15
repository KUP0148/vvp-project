from planetary2d.animator import Animator
from planetary2d.bodies_system import SystemOfBodies
from planetary2d.data import load_json_data


# DICT = {"body1": {"position": [-56., -114.], "velocity": [-19., -10.], "mass": 743.}, "body2": {"position": [114., -181.], "velocity": [-12., 67.], "mass": 295.}, "body3": {"position": [-266., 976.], "velocity": [10., -15.], "mass": 343.}}
# DICT = {"body1": {"position": [-56., -114.], "velocity": [0., 0.], "mass": 743e14}, "body2": {"position": [114., -181.], "velocity": [0., 0.], "mass": 295e14}, "body3": {"position": [-266., 976.], "velocity": [0., 0.], "mass": 343e14}}
# DICT = {"Sun": {"position": [0., 0.], "velocity": [0., 0.], "mass": 400e14},
        # "mercur": {"position": [0., 100.], "velocity": [-150., 0.], "mass": 400e14},
        # "venus": {"position": [0., -100.], "velocity": [150., 0.], "mass": 400e14}}
# DICT = {"body1": {"position": [0., 0.], "velocity": [0., 0.], "mass": 7e11},
#         "body2": {"position": [0., 10.], "velocity": [0., 0.], "mass": 5e11}}
print("Construct SystemOfBodies")
# x = SystemOfBodies(DICT, base_interval=0.005)
# x = SystemOfBodies(DICT, base_interval=0.01)
x = SystemOfBodies(load_json_data("./asgmt/data/planets.json"), base_interval=86_400)

def show_positions(x: SystemOfBodies):
    # print(x.b_num)
    # print(x.labels)
    print(x.pos)
    # print(x.vel)
    # print(x.mass)
    print(x.acc)
    # print(x.limit)
    # print(x.hist)
    # print(x.Δt)


# print("before:")
# show_positions(x)
# xiter = x.__iter__()
# print("after:")
# xiter.__next__()
# show_positions(x)
# print("after2:")
# xiter.__next__()
# show_positions(x)

print("Construct Animator")
# AN = Animator(x, 1000, no_units=True, )
AN = Animator(x, 100000, no_units=True, frame_rate=10000, no_show=True)
print("animate()")
AN.animate()
print("save_animation()")
AN.save_animation("./zzz.gif", 'gif')
