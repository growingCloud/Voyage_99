# Chapter11_28. 해시맵 디자인 (291p)
# 난이도 : ★
# Leet code Num. : 706

# 다음의 기능을 제공하는 해시맵을 디자인하라
# - put(key, value) : 키, 값을 해시맵에 삽입한다. 만약 이미 존재하는 키라면 업데이트한다.
# - get(key) :  키에 해당하는 값을 조회한다. 만약 키가 존재하지 않는다면 -1을 리턴한다.
# - remove(key) : 키에 해당하는 키, 값을 해시맵에서 삭제한다


# MyHashMap hashMap = new MyHashMap();
# hashMap.put(1, 1);
# hashMap.put(1, 2);
# hashMap.get(1);       // 1을 리턴한다
# hashMap.get(3);       // -1을 리턴한다 (키가 존재하지 않음)
# hashMap.put(2, 1);    // 값을 업데이트한다
# hashMap.get(2);       // 1을 리턴한다
# hashMap.remove(2);    // 키 2에 해당하는 키, 값을 삭제한다
# hashMap.get(2);       // -1을 리턴한다 (키가 삭제되어 존재하지 않음)