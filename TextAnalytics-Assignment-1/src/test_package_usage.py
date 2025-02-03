from python_tutorial.hello_world import SayOnce, SayNTimes

print("Top-level call module")
sayOnce_sensitive = SayOnce(case_sensitive = True)
sayNTime_insensitive = SayNTimes(N_times = 3, case_sensitive = False)

sayOnce_sensitive.say("Hello CS-5293 guys!")
sayNTime_insensitive.say("Hello CS-5293 students!")