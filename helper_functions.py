from click import FileError


def responding_comment(user_to_check, ratio_stats_list):
    attempts = ratio_stats_list["attempted_ratios"]
    success = ratio_stats_list["successful_ratios"]
    likes_for = ratio_stats_list["total_likes_for"]
    likes_against = ratio_stats_list["total_likes_against"]

    success_percent = round(calculate_success_percent(attempts, success), 2)

    return f"@{user_to_check}'s Ratio Stats:\nAttempted Ratio's: {attempts}\nSuccessful Ratio's: {success}\nTotal Likes For: {likes_for}\nTotal Likes Against: {likes_against}\nSuccess Percentage: {success_percent}%"


def calculate_success_percent(num1, num2):
    if num1 > num2:
        return (num2 / num1) * 100
    else:
        return (num1 / num2) * 100


def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, "r")
    last_seen_id = int(float(file_read.readline().strip()))
    file_read.close()
    return last_seen_id


def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, "w")
    file_write.write(str(last_seen_id))
    file_write.close()
    return
