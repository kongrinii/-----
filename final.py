"""
피로그래밍 19기 코딩테스트
작성일: 2023.06.09
작성자: 오경린

1부터 30까지 랜덤으로 13장의 카드를 뽑아서 덱에 넣고 4명의 참가자들이 뒤에서부터 뽑으며 
최댓값을 뽑은 사람이 최댓값-최소값만큼 점수를 얻는 프로그램. 
"""

import random
from collections import deque


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.round_wins = 0
        self.last_round_score = 0
        self.is_selected = False

    def __str__(self) -> str:
        return f"{self.name}"

    def update_score(self, score_difference):
        self.score += score_difference


class Game:
    def __init__(self):
        self.players = []  # 유저들의 목록
        self.deck = []  # 카드 무작위 생성
        self.my_player = ""

    def start_game(self):
        name_list = ["박신빈", "윤정원", "임담희", "김용현"]
        n = int(input('1, 2, 3, 4 중 한 숫자 선택: '))
        for i in range(len(name_list)):
            if i == n - 1:
                my_player = Player(name_list[i])
                my_player.is_selected = True
                self.players.append(my_player)
            else:
                self.players.append(Player(name_list[i]))

        number = list(range(1, 14))
        card = []
        for j in range(30):
            temp = random.choice(number)
            card.append(temp)

        self.deck = deque(card)

    def set_play_order(self, round_num):
        if round_num == 1:
            self.players.sort(key=lambda player: player.name)  # 사전 순서로 이름을 오름차순 정렬
        else:
            self.players.sort(key=lambda player: player.score)  # 점수를 기준으로 오름차순 정렬

    def play_round(self):
        play_order = ", ".join(map(str, self.players))
        print(f"게임은 {play_order} 순으로 진행됩니다.\n")

        random.shuffle(self.deck)

        print("===========플레이어가 뽑은 카드============")
        players_cards = {}  # 플레이어가 뽑은 카드 저장

        for player in self.players:
            selected_card = self.deck.pop()

            player.last_round_score = player.score

            players_cards[player.name] = selected_card  # 각 플레이어가 어떤 카드를 뽑았는지 추적
            print(">> {0} (현재 점수: {1})".format(player.name, player.score))
            print(">> 뽑은 카드: {0}\n".format(selected_card))

        # 모두 같은 카드를 뽑았을 경우
        if len(set(players_cards.values())) == 1:
            max_card = 0
            print("모두 같은 카드를 뽑아 0점을 획득하셨습니다")
        # 그렇지 않았을 때에는 최댓값 - 최솟값 만큼 가장 큰 카드를 뽑은 사람이 점수를 획득한다
        else:
            max_card = max(players_cards.values())  # 플레이어들이 뽑은 카드 중 가장 큰 값
            winning_players = [player for player, card in players_cards.items() if card == max_card]
            min_card = min(players_cards.values())
            score_difference = max_card - min_card
            for player in winning_players:
                player_obj = next(p for p in self.players if p.name == player)
                player_obj.update_score(score_difference)  # 점수 갱신
                player_obj.round_wins += 1  # 승리 횟수 증가
                print(">>>> 축하합니다. {0}님이 {1} 점을 얻었습니다 \\^_^/ <<<<".format(player, score_difference))

    def play_game(self):
        for round_num in range(1, 5):
            self.set_play_order(round_num)

            print("===========================")
            print(f"     ROUND {round_num} - START")
            print("===========================")
            self.play_round()

            print("===========================")
            print(f"     ROUND {round_num} - END")
            print("===========================")

            for order, player in enumerate(self.players, 1):
                print(f" {order}. {player} : {player.score}점")

            if round_num > 1:
                for player in self.players:
                    player.last_round_score = player.score  # 이전 라운드의 점수를 저장

    def game_result(self):
        # 점수 순으로 결과 출력
        print("=============================")
        print("     게임 순위 - 점수")
        print("=============================")
        self.players.sort(key=lambda player: (player.score, player.name), reverse=True)
        for rank, player in enumerate(self.players, 1):
            if player.is_selected:
                print(f"{rank}등 -*{player}* : {player.score}점")
            else:
                print(f"{rank}등 - {player} : {player.score}점")
        print()

        # 승리 횟수 순으로 결과 출력
        print("=============================")
        print("     게임 순위 - 승리 횟수")
        print("=============================")
        self.players.sort(key=lambda player: (player.round_wins, player.name), reverse=True)
        for rank, player in enumerate(self.players, 1):
            if player.is_selected:
                print(f"{rank}등 -*{player}* : {player.round_wins}회")
            else:
                print(f"{rank}등 - {player} : {player.round_wins}회")
        print()

    def game(self):
        self.start_game()
        self.play_game()
        self.game_result()


if __name__ == "__main__":
    game = Game()
    game.game()