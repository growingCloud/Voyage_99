# Chapter12_38. 일정 재구성 (357p)
# 난이도 : ★★
# Leet code Num. : 332

# [from, to]로 구성된 항공권 목록을 이용해 JFK 에서 출발하는 여행 일정을 구성하라.
# 여러 일정이 있는 경우 사전 어휘 순(Lexical Order)으로 방문한다.
# 예제 1.
# 입력 >> [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
# 출력 >> ["JFK", "MUC", "LHR", "SFO", "SJC"]
# 예제 2.
# 입력 >> [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
# 출력 >> ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]