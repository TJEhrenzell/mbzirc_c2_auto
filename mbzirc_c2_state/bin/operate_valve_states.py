""" operate_valve_states.py - Version 1.0 - Created 2016-11-10

    State machine classes for positioning and operating the valve.

    State Classes
        MoveToValveReady -
        IDValve
        MoveToValve
        MoveToOperate
        RotateValve

    Alan Lattimer (alattimer at jensenhughes dot com)


    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.5

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:

    http://www.gnu.org/licenses/gpl.html

"""

import rospy
import smach
import subprocess

class MoveToValveReady(smach.State):
    """Moves the arm in front of valve for detection

    Outcomes
    --------
        atValveReady : at the ready position

    """

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['atValveReady',
                                       'moveStuck',
                                       'moveFailed'],
                             input_keys=['move_counter_in'],
                             output_keys=['move_counter_out'])

    def execute(self, userdata):
        max_retries = 0

        prc = subprocess.Popen("rosrun mbzirc_grasping move_arm_param.py", shell=True)
        prc.wait()

        move_state = rospy.get_param('move_arm_status')

        # Preset the out move counter to 0, override if necessary
        userdata.move_counter_out = 0

        if move_state == 'success':
            return 'atValveReady'

        else:
            if userdata.move_counter_in < max_retries:
                userdata.move_counter_out = userdata.move_counter_in + 1
                return 'moveStuck'

            else:
                return 'moveFailed'




class IDValve(smach.State):
    """Identifies the center of the valve

    Outcomes
    --------
        valveFound : found the valve
        valveNotFound : could not locate the valve

    """

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['valveFound',
                                       'valveNotFound'])

    def execute(self, userdata):
        prc = subprocess.Popen("rosrun mbzirc_c2_auto idvalve.py", shell=True)
        prc.wait()

        return rospy.get_param('smach_state')



class MoveToValve(smach.State):
    """Move to the valve to prepare for video servo

    Outcomes
    --------
        atValve : at the valve ready to servo in

    """

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['atValve',
                                       'moveStuck',
                                       'moveFailed'],
                             input_keys=['move_counter_in'],
                             output_keys=['move_counter_out'])

    def execute(self, userdata):
        max_retries = 0

        prc = subprocess.Popen("rosrun mbzirc_grasping move_arm_param.py", shell=True)
        prc.wait()

        move_state = rospy.get_param('move_arm_status')

        # Preset the out move counter to 0, override if necessary
        userdata.move_counter_out = 0

        if move_state == 'success':
            return 'atValve'

        else:
            if userdata.move_counter_in < max_retries:
                userdata.move_counter_out = userdata.move_counter_in + 1
                return 'moveStuck'

            else:
                return 'moveFailed'



class MoveToOperate(smach.State):
    """Servo in to valve and place wrench on valve

    Outcomes
    --------
        wrenchFell : wrench fell off the gripper
        wrenchOnValve : at the ready position

    """

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['wrenchFell',
                                       'wrenchOnValve'])

    def execute(self, userdata):
        prc = subprocess.Popen("rosrun mbzirc_c2_auto move2op.py", shell=True)
        prc.wait()

        return rospy.get_param('smach_state')


class RotateValve(smach.State):
    """Rotate the valve one full turn

    Outcomes
    --------
        wrenchFell : wrench fell out of the gripper
        cantTurnValve : valve stuck
        turnedValve : able to turn the valve

    """

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['wrenchFell',
                                       'cantTurnValve',
                                       'turnedValve'])

    def execute(self, userdata):
        prc = subprocess.Popen("rosrun mbzirc_c2_auto rotate.py", shell=True)
        prc.wait()

        return rospy.get_param('smach_state')


