# from connect_raspi import send_command, get_image
# from time import sleep
# from enhanced_processing import crop_and_enhance_image


# # Example usage
# if __name__ == "__main__":
#     imageNumber="Idared_good"
#     image=get_image("take_image test_image_FGS580.jpg", expect_image=True, save_as=f"{imageNumber}_FGS580.jpg") # FGS580
#     print(image)
#     send_command("move_servo 1")
#     sleep(2)
#     crop_and_enhance_image(image)
#     image=get_image("take_image test_image_FGUV.jpg", expect_image=True, save_as = f"{imageNumber}_FGUV.jpg")
#     send_command("move_servo 1")
#     sleep(2)
#     crop_and_enhance_image(image)
#     image=get_image("take_image test_image_FGL850.jpg", expect_image=True, save_as = f"{imageNumber}_FGL850.jpg")
#     send_command("move_servo 1")
#     sleep(2)
#     crop_and_enhance_image(image)
#     image=get_image("take_image test_image_FG37.jpg", expect_image=True, save_as = f"{imageNumber}_FG37.jpg")
#     send_command("move_servo 1")
#     sleep(2)
#     image=get_image("move_servo 1")
#     sleep(2)
#     image=get_image("take_image test_image_FG1000.jpg", expect_image=True, save_as =f"{imageNumber}_FG1000.jpg")
#     send_command("move_servo 1")
#     sleep(2)
#     crop_and_enhance_image(image)

from connect_raspi import send_command, get_image
from time import sleep, monotonic
from enhanced_processing import crop_and_enhance_image

def process_with_interval(cmd, save_as, interval_s, skip):
    """
    Runs get_image(cmd), does any post‐processing, 
    and ensures the next run starts interval_s seconds after this one began.
    """
    start = monotonic()
    image= []
    if not skip:
        image = get_image(cmd, expect_image=True, save_as=save_as)
        crop_and_enhance_image(image)
    # time spent so far
    elapsed = monotonic() - start
    # sleep only if there’s time left
    to_sleep = interval_s - elapsed
    if to_sleep > 0:
        sleep(to_sleep)
    return image

if __name__ == "__main__":
    imageNumber = "Idared_good"
    interval = 1.35  # seconds, for example
    
    # list of (command, filename suffix) pairs
    jobs = [
        ("take_image test_image_FGS580.jpg", "_FGS580.jpg",False),
        ("take_image test_image_FGUV.jpg",   "_FGUV.jpg", False),
        ("take_image test_image_FGL850.jpg", "_FGL850.jpg",False),
        ("take_image test_image_FG37.jpg",   "_FG37.jpg",False),
        ("take_image test_image_FG37.jpg",   "_FG37.jpg", True),
        ("take_image test_image_FG1000.jpg", "_FG1000.jpg",False),
    ]
    
    for cmd, suffix , skip in jobs:
        # take picture + process, maintaining interval
        image = process_with_interval(cmd, f"{imageNumber}{suffix}", interval,skip)
        send_command("move_servo 1")  # can be before or after, as needed
