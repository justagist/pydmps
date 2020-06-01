''' 
MouseTracker class
    @author: JustaGist (saifksidhik@gmail.com)
    @file: mousetracker.py

demo USAGE: python mousetracker.py 
'''

import pygame
import time
import logging
import numpy as np

class MouseTracker:
    '''
        Mouse tracker Class: 1. Track the coordinates of mouse point when the mouse button is held. Used to record the trajectory of the mouse.
                             2. Track the coordinates of mouse points when the mouse button is clicked
    '''

    def __init__(self, window_dim = [1000, 600]):
        """
            Mouse tracker Class: 1. Track the coordinates of mouse point when the mouse button is held. Used to record the trajectory of the mouse.
                                 2. Track the coordinates of mouse points when the mouse button is clicked

            :type window_dim: [int, int]
            :arg window_dim: Pixel dimensions (width x height) of the visualised window
        """

        self._init = False

        # ----- pygame window dimensions
        self._width = window_dim[0]
        self._height = window_dim[1]

    # ===== FUNCTION 1 =====
    def record_mousehold_path(self, record_interval = 0.01, verbose = True, save_to_file = None, close_on_mousebutton_up = False, inverted = False, keep_window_alive = False):
        """
            Records the pixel coordinates of the mouse if mousebutton 1 is held. Origin is at left-top corner.
            
            :param record_interval: delay in the record loop (inverse of loop rate)
            :type record_interval: float
            :param verbose: print the coordinates in console
            :type verbose: bool
            :param save_to_file: if "path/to/file" as string is given, will save the values to the given file
            :type save_to_file: string
            :param close_on_mousebutton_up: if set to True, the recording will stop as soon as the mouse button is released
            :type close_on_mousebutton_up: bool
            :param inverted: if set to True, coordinates will be recorded such that origin is at left bottom corner
            :type inverted: bool
            :param keep_window_alive: if set to True, the pygame window will not be closed after data collection.
            :type keep_window_alive: bool
        """

        self._check_and_initialise_window(caption = "MouseTraj Tracker")

        running = True

        hold_coords = []

        while running:
            try:
                for event in pygame.event.get():
                    if (event.type == pygame.MOUSEBUTTONUP and close_on_mousebutton_up) or event.type == pygame.QUIT:
                        running = False

                if pygame.mouse.get_pressed() == (1,0,0):

                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    
                    self._screen.fill((255,255,255),((mouseX-1,mouseY-1),(3,3))) # ----- draw the mouse traectory in white
                    pygame.display.update()
                    
                    if inverted:
                        mouseY = self._height - mouseY

                    hold_coords.append((mouseX, mouseY))

                    if verbose:
                        print (mouseX, mouseY)

                time.sleep(record_interval)
            except KeyboardInterrupt:
                break

        if not keep_window_alive:
            self._close_window()

        if len(hold_coords) < 1:
            print ("No trajectory recorded!\n")
            return None

        coords = np.asarray(hold_coords) 

        if save_to_file is not None:
            np.savetxt(save_to_file, coords, delimiter=",")
            print ("\nSaved mouse coordinates to ", save_to_file, "\n")

        return coords

    # ===== FUNCTION 2 =====
    def get_mouse_click_coords(self, num_clicks = None, verbose = True, inverted = False, keep_window_alive = False, save_to_file = None):
        """
            Records the pixel coordinates of the mouse when mousebutton 1 is clicked. Origin is at left-top corner.
            
            :param num_clicks: number of clicks to capture. If set to None, all the clicks till the window is closed will be recorded.
            :type num_clicks: int
            :param verbose: print the coordinates in console
            :type verbose: bool
            :param save_to_file: if "path/to/file" as string is given, will save the values to the given file
            :type save_to_file: string
            :param inverted: if set to True, coordinates will be recorded such that origin is at left bottom corner
            :type inverted: bool
            :param keep_window_alive: if set to True, the pygame window will not be closed after data collection.
            :type keep_window_alive: bool
        """

        self._check_and_initialise_window(caption = "MouseClick Tracker")

        counter = 0

        click_coords = []

        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        
                        (mouseX, mouseY) = pygame.mouse.get_pos()
                        
                        self._screen.fill((155,20,30),((mouseX-1,mouseY-1),(3,3))) # ----- mark the mouse click in red
                        pygame.display.update()

                        if inverted:
                            mouseY = self._height - mouseY
                        
                        click_coords.append((mouseX, mouseY))
                        counter += 1

                        if (num_clicks is not None and counter >= num_clicks):
                            running = False

                        if verbose:
                            print (mouseX, mouseY)

            except KeyboardInterrupt:
                break

        count = "\nRecorded %d clicks"%counter if counter > 0 else "No clicks recorded!"

        print (count)

        if not keep_window_alive:
            self._close_window()

        if counter == 0:
            return None

        coords = np.asarray(click_coords)

        if save_to_file is not None:
            np.savetxt(save_to_file, coords, delimiter=",")
            print ("\nSaved mouse coordinates to ", save_to_file, "\n")

        return coords


    def _check_and_initialise_window(self, caption = None):
        '''
            If another instance of pygame is not running, this function creates a window with the given caption
        '''

        if not self._init:

            self._screen = pygame.display.set_mode((self._width, self._height))
            pygame.display.set_caption(caption)

            self._init = True

        else:
            logging.info("MouseUtils Msg: Another pygame instance running! Using existing screen...")

    def _close_window(self):

        print ("\nClosing Pygame Window...\n")
        pygame.quit()

## ======================== ##
#         TEST CODE          #
## ======================== ##
if __name__ == '__main__':
    
    MouseTracker(window_dim = [1000, 600]).record_mousehold_path(record_interval = 0.1, close_on_mousebutton_up = True)