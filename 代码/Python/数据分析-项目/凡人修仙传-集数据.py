import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 导入，view是播放量，like是点赞，coin是投币数，share是收藏，reply是评论
df_ep = pd.read_csv('bilibili_ep_info.csv')

df_ep['点赞率'] = df_ep['like']/df_ep['view']*100
df_ep['投币率'] = df_ep['coin']/df_ep['view']*100
df_ep['收藏率'] = df_ep['share']/df_ep['view']*100
df_ep['播放留存率'] = None
df_ep['点赞留存率'] = None
df_ep['投币留存率'] = None
df_ep['收藏留存率'] = None
for i in range(1, len(df_ep), 2):
    df_ep.loc[i, '播放留存率'] = round(df_ep.loc[i, 'view'] / df_ep.loc[i-1, 'view'] * 100, 2)
    df_ep.loc[i, '点赞留存率'] = round(df_ep.loc[i, 'like'] / df_ep.loc[i-1, 'like'] * 100, 2)
    df_ep.loc[i, '投币留存率'] = round(df_ep.loc[i, 'coin'] / df_ep.loc[i-1, 'coin'] * 100, 2)
    df_ep.loc[i, '收藏留存率'] = round(df_ep.loc[i, 'share'] / df_ep.loc[i-1, 'share'] * 100, 2)

summary_df = df_ep[[
    'title',
    'view',
    '点赞率',
    '投币率',
    '收藏率',
    '播放留存率',
    '点赞留存率',
    '投币留存率',
    '收藏留存率'
]].copy()

summary_df = summary_df.rename(columns={
    'title': '集数',
    'view': '播放量'
})

print("\n===== 汇总表 =====")
print(summary_df)

# 只保留有留存率的第2集
retention_df = summary_df[summary_df['播放留存率'].notna()].copy()

plt.figure(figsize=(12, 6))

x = range(len(retention_df))
width = 0.2

plt.bar([i - 1.5*width for i in x], retention_df['播放留存率'], width=width, label='播放留存率')
plt.bar([i - 0.5*width for i in x], retention_df['点赞留存率'], width=width, label='点赞留存率')
plt.bar([i + 0.5*width for i in x], retention_df['投币留存率'], width=width, label='投币留存率')
plt.bar([i + 1.5*width for i in x], retention_df['收藏留存率'], width=width, label='收藏留存率')

plt.title('凡人修仙传各篇章留存率对比')
plt.ylabel('留存率(%)')
plt.xticks(x, retention_df['集数'], rotation=30)

plt.legend()
plt.tight_layout()

plt.show()

