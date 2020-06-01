import sys
import numpy as np
import matplotlib.pyplot as plt

from pydmps.dmp_discrete import DMPs_discrete as dmp_discrete

from utils import MouseTracker


def plot_traj(trajectories):
    plt.figure("trajectories")
    
    for i in range(len(trajectories)):
        trajectory = trajectories[i]
        idx = trajectory.shape[1]*100 + 11
        if i == 0:
            color = 'r--'
        elif i==1:
            color = 'g'
        else:
            color = 'b'
        for k in range(trajectory.shape[1]):
            plt.subplot(idx)
            idx += 1
            plt.plot(trajectory[:,k], color)
    plt.show() 

def plot_path(trajectory, true_points, custom_start = None, custom_goal = None):

    # ----- interactive mode on
    plt.ion()

    # ----- position trajectory for plotting
    pos_trajectory = trajectory['pos_traj']

    plt.scatter(true_points[:,0],true_points[:,1], label = "Original Path", color = 'y')

    if custom_start is not None:
        plt.scatter(custom_start[0], custom_start[1], label = "Custom start", color = 'r')

    if custom_goal is not None:
        plt.scatter(custom_goal[0], custom_goal[1], label = "Custom goal", color = 'g')

    plt.axes().set_aspect('equal', 'datalim')
    
    i = 0

    # ----- find the resultant velocity for updating the graph at the scaled speed
    vel_square = np.square(trajectory['vel_traj'])
    resultant_vel = np.sqrt(vel_square[:,0]+vel_square[:,1])*1000

    skip_step = int(0.01*pos_trajectory.shape[0]) # ----- steps to skip so that plot update is not too slow
    stop = False
    while i < (pos_trajectory.shape[0]):
        try:
            plt.plot(pos_trajectory[:i,0],pos_trajectory[:i,1], label = "New path", color = 'b')

            pause = 0.001/resultant_vel[i] if resultant_vel[i] > 0.01 else 0.001/0.01
            plt.pause(pause)
            plt.draw()

            if i < 1:
                plt.legend()

            i += skip_step

        except KeyboardInterrupt:
            stop = True
            break

def train_dmp(trajectory):
    # discrete_dmp_config['dof'] = 2
    dmp = dmp_discrete(n_dmps=2, n_bfs=500, ay=np.ones(2)*100.0)
    y_track = []
    dy_track = []
    ddy_track = []
    dmp.imitate_path(y_des=trajectory, plot=False)

    return dmp

def test_dmp(dmp, custom_start = None, custom_goal = None):
    
    if custom_start is not None:
        dmp.y = custom_start
    if custom_goal is not None:
        dmp.goal = custom_goal

    y_track, dy_track, ddy_track = dmp.rollout(tau = 1)

    test_traj = {
    'pos_traj': y_track,
    'vel_traj':dy_track,
    'acc_traj':ddy_track
    }

    
    return test_traj

if __name__ == '__main__':

    mt = MouseTracker(window_dim = [1000, 1000])

    # ----- record trajectory using mouse
    print "\nDraw trajectory ... "
    trajectory = mt.record_mousehold_path(record_interval = 0.001, close_on_mousebutton_up = True, verbose = False, inverted = True, keep_window_alive = True)

    # ----- get custom start and end points for the dmp using mouse clicks
    print "\nClick custom start and end points"
    strt_end = mt.get_mouse_click_coords(num_clicks = 2, inverted = True, keep_window_alive = True, verbose = False)
    # strt_end = None

    # print (trajectory)
    # print (strt_end)

    if trajectory is not None:
        dmp = train_dmp(trajectory.T)


        # ----- the trajectory after modifying the start and goal, speed etc.
        test_traj = test_dmp(dmp, custom_start = strt_end[0,:] if strt_end is not None else None, custom_goal = strt_end[1,:] if strt_end is not None else None)

        # ----- plotting the 2d paths (actual and modified)
        plot_path(test_traj, trajectory, custom_start = strt_end[0,:] if strt_end is not None else None, custom_goal = strt_end[1,:] if strt_end is not None else None)

    else:
        print "No data in trajectory!\n"