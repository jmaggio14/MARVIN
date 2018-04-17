#
# marvin (c) by Jeffrey Maggio, Hunter Mellema, Joseph Bartelmo
#
# marvin is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
#
#


#Timer.py
def test__Timer():
    """tests Marvin's timer object
    input::
        None

    returns::
        ret (bool):
            boolean indicating whether or not the test was passed
    """
    print("TESTING MARVIN TIMER...")
    import marvin
    import time
    marvin.init()
    test_timer = marvin.Timer()
    #testing time property
    print("testing the time property...")
    time.sleep(0.5)
    timer_time = test_timer.time
    print("this should be close to 0.5 seconds: {}".format(timer_time))

    #testing lap test_timer
    print("the next couple printouts should all be close to 1.0 second...")
    #reset lap
    test_timer.lap
    for i in range(3):
        time.sleep(1.0)
        print('test lap time',test_timer.lap)


    #testing the countdown timer
    print("testing the test_timer countdown...")
    countdown_valid = True
    ref_time = time.time()
    test_timer.countdown = 10
    while countdown_valid:
        ground_truth = 10 - (time.time() - ref_time)
        countdown_time = test_timer.countdown
        print("ground_truth:{0} | countdown_time:{1}".format(
                                                        ground_truth,
                                                        countdown_time))
        countdown_valid = (ground_truth >= 0) and (countdown_time >= 0)



# END
