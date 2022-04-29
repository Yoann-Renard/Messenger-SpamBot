#### ╔╣█╠╗╚╝╔╣█╠╗ ####
if __name__ == "__main__":
    try:
        #CloseFirstTab()
        user_or_group_to_spam = input("User or group to spam: ")
        message_to_spam = input("Message to spam: ")
        seconds_inter = int(input("Interval: "))
        from src.src import *
        fb = Facebook()
        fb.connection()
        fb.sendMessage(user_or_group_to_spam, message_to_spam, True)
        print(f"Spammer set with a {seconds_inter}s delay.")
        print(f"Message: {message_to_spam} sent to {user_or_group_to_spam}.")
        def spam():
            driver.find_element_by_css_selector(
                'div[aria-label="Écrire un message"]').send_keys(message_to_spam + '\n')
            print(f"Message: {message_to_spam} sent to {user_or_group_to_spam}.")
        time.sleep(seconds_inter)
        inter = setInterval(seconds_inter, spam)
    except KeyboardInterrupt:
        print("\nBye.")
        exit(0)
    except ValueError:
        print("Interval must be a number.")
        exit(1)
    