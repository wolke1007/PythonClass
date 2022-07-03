# 1A2B
import random


def user_input_answer() -> list:
    # user_list -> correct -> return list with numbers
    # user_list -> wrong -> return empty list
    try:
        user_list = list(map(int, input("請輸入4個整數：")))
    except:
        print("只能輸入整數")
        return []

    set_list = set(user_list)
    if len(user_list) != 4:
        print("只能固定輸入4個數字")
        return []
    elif len(user_list) > len(set_list):
        print("請勿輸入重複數字")
        return []
    else:
        return user_list


def game_logic(user_list: list, ans_list: list) -> tuple:  # (int A, int B)
    """
    return 1, 2  # 1A2B
    """
    a = b = n = 0
    # [1,2,3,4]
    # a -> ans A
    # b -> ans B
    # n -> index
    for i in user_list:
        # i -> number in user_list
        if user_list[n] == ans_list[n]:
            a += 1
        else:
            if i in ans_list:
                b += 1
        n += 1  # index increase no matter result
    print(str(a), "A", str(b), "B")
    return a, b

def main():  # flow
    ans_list = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=4)
    print(ans_list)
    endless_switch = True  # config
    counter = 10  # config
    game_mode = "endless" if endless_switch is True else counter

    while game_mode:
        user_list = user_input_answer()
        if not user_list:
            continue
        ans_tuple = game_logic(user_list, ans_list)  # A, B
        if ans_tuple == (4, 0):
            print("正確答案：", user_list)
            break
        counter -= 1
    print("遊戲結束!")


if __name__ == "__main__":
    main()
