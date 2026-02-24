import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1. 09번 결과 데이터 로드
try:
    rules = pd.read_csv('./data/09_association_rules_result.csv')
except FileNotFoundError:
    print("오류: 09번 결과 파일이 없습니다. 먼저 09_product_association.py를 실행하세요.")
    exit()

# 2. 데이터 정제 (frozenset 형태의 문자열 처리)
rules['antecedents'] = rules['antecedents'].apply(lambda x: list(eval(x))[0])
rules['consequents'] = rules['consequents'].apply(lambda x: list(eval(x))[0])

# 3. 네트워크 그래프 객체 생성
G = nx.DiGraph()

# 4. 노드와 에지(연결선) 추가
for _, row in rules.iterrows():
    G.add_edge(row['antecedents'], row['consequents'], weight=row['lift'])

# 5. 시각화 설정
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, k=0.8) # 노드 배치 알고리즘

# 노드(상품 카테고리) 그리기
nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightgreen', alpha=0.9)
# 에지(연관성) 그리기 - Lift 값에 따라 선 굵기 조절
nx.draw_networkx_edges(G, pos, width=[d['weight']*2 for (u, v, d) in G.edges(data=True)], 
                       edge_color='gray', arrowsize=20)
# 라벨(카테고리명) 그리기
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

plt.title("Brazil E-commerce Product Association Network", pad=20)
plt.axis('off')

# 6. 결과 저장 및 출력
plt.tight_layout()
plt.savefig('./data/reports/10_product_network.png')
print("--- [시각화 완료: ./data/reports/10_product_network.png 저장됨] ---")
plt.show()