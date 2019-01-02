# Kristina Kaypaghian and Tina Bao
# Lab02 Write Up

# 4.1

cd my-imaginary-repo
touch my_second_file
git add my_second_file
git commit
git push

# 4.2

Tina and I developed on the VM on one computer.
When we made large changes/developments, we did so using Sublime on the VM, then pushed to the remote repo, and pulled onto the Pi.
When we wanted to make small changes just to test out/debug something quickly, we used nano on the Pi.

It would be beneficial to understand how to navigate nano or another text-based editor, so as not to lose time just holding down the arrow keys to get to where we want to in the code when we want to change just one small thing in a specific place.

# 4.3

In the grovepi file, in the ultrasonic_read() function, there is a delay of 60 ms.
This delay is intentionally made to be longer than the firmware delay of 50ms.

The Pi also uses the Inter-Integrated Circuit (i2c) communication protocol.